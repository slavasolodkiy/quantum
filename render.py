#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    parser.add_argument("--out", default="proof-of-exit.html")
    args = parser.parse_args()

    data = json.loads(Path(args.result).read_text(encoding="utf-8"))
    worlds = data.get("worlds", [])[:8]
    cards = "\n".join(
        f"""
        <article class='world {'exit' if w['exit'] else 'locked'}'>
          <div><strong>{'EXIT' if w['exit'] else 'LOCKED'}</strong> · p={w['probability']:.3f}</div>
          <pre>{html.escape(w['maze'])}</pre>
          <small>{html.escape(w['certificate'])}</small>
        </article>"""
        for w in worlds
    )
    source = html.escape(str(data.get("source", "")))
    limitations = " ".join(str(item) for item in data.get("limitations", []))
    evidence = "\n".join(
        f"<details><summary>{label}</summary><pre style='overflow:auto'>{html.escape(json.dumps(data[key], indent=2))}</pre></details>"
        for label, key in [("Credential-free request", "request"), ("Completed job status", "status_raw"), ("Full raw Atlas result", "raw")]
        if key in data
    )
    page = f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Proof of Exit</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#0f1115;color:#f6f4ef}}main{{max-width:1050px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(3rem,8vw,7rem);margin:.1em 0}}.tag{{font-size:1.25rem;color:#b8d7ff}}.numbers{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:32px 0}}.n,.world{{background:#181c23;border:1px solid #303640;border-radius:14px;padding:18px}}.n b{{display:block;font-size:2rem}}.worlds{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}pre{{font-size:1.05rem;line-height:1.1}}.exit{{border-color:#4fa46c}}.locked{{border-color:#bd6666}}footer{{margin-top:36px;color:#aaa}}@media(max-width:650px){{.numbers{{grid-template-columns:1fr}}}}
</style></head><body><main>
<p class='tag'>Atlas samples. Logic explains.</p><h1>Proof of Exit</h1>
<p>A 4×4 maze is represented by a 16-bit world. A corridor opens when adjacent rooms agree. Classical reachability checking determines whether an exit exists and emits a certificate for every sampled world.</p>
<div class='numbers'>
<div class='n'><span>Independent-door intuition</span><b>75%</b></div>
<div class='n'><span>Balanced target prediction</span><b>50%</b></div>
<div class='n'><span>Observed Atlas emulation</span><b>{pct(float(data.get('p_exit_measured',0)))}</b></div>
</div>
<h2>Why intuition can fail</h2><p>For two independent doors that each open with probability 50%, the chance that at least one opens is 75%. Under this maze's ideal non-bridge equality constraints, however, the two bridge doors open and close together. A dependency-free exhaustive proof checks all 65,536 possible 16-bit worlds: four satisfy those constraints, and none has exactly one bridge door open. A 50% escape prediction additionally requires a balanced bridge correlation; the equality theorem alone does not prove that probability.</p>
<h2>What the real job returned</h2><p>{html.escape(limitations)}</p>
<h2>Sampled worlds</h2><section class='worlds'>{cards}</section>
<h2>What is quantum here?</h2><p>The completed Atlas graph-v1 job used mode emu and backend aer: quantum-circuit emulation, with no physical QPU. The returned distribution is real Atlas job evidence. The finite proof and path certificates are classical. This demo does not claim quantum advantage or experimental confirmation of the balanced 50% target.</p>
<h2>Reproducibility evidence</h2>{evidence}
<footer>Source: {source}. Job ID: {html.escape(str(data.get('job_id','')))}. Status: {html.escape(str(data.get('atlas_status','')))}. Mode: {html.escape(str(data.get('mode','')))}. Backend: {html.escape(str(data.get('backend','')))}. Shots: {data.get('shots','')}.</footer>
</main></body></html>"""
    Path(args.out).write_text(page, encoding="utf-8")
    print(args.out)

if __name__ == "__main__":
    main()
