#!/usr/bin/env python3
"""Proof of Exit: Atlas graph worlds + deterministic proof/certificates.

The Atlas API contract in this file is a baseline derived from the project notes.
Before a real run, verify the endpoint and JSON fields against the live Atlas docs.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable


N, C, START, EXIT = 16, 4, 0, 15
COIN_DOORS = {(3, 7), (10, 14)}
DOORS = [
    (0, 1), (1, 2), (2, 3), (3, 7), (7, 11), (11, 15),
    (0, 4), (4, 8), (8, 9), (9, 13), (13, 14), (10, 14),
    (10, 11), (2, 6), (5, 6), (5, 9), (12, 13),
]
DEFAULT_API = "https://api.mothquantum.com/api/v1"


def http_json(url: str, body: dict[str, Any] | None = None, key: str | None = None, timeout: int = 60) -> Any:
    headers = {"Content-Type": "application/json", "User-Agent": "proof-of-exit/0.2"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(
        url,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"HTTP {exc.code} from {url}: {payload}") from exc


def walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def is_bitstring(value: Any) -> bool:
    return isinstance(value, str) and len(value) == N and set(value) <= {"0", "1"}


def extract_worlds(result: Any, shots: int) -> dict[str, float]:
    worlds: dict[str, float] = {}
    for node in walk(result):
        if not isinstance(node, dict):
            continue
        bits = next((v for v in node.values() if is_bitstring(v)), None)
        if bits and ("probability" in node or "count" in node):
            value = node.get("probability")
            if value is None:
                value = node.get("count", 0) / shots
            worlds[bits] = float(value)

        numeric = {k: v for k, v in node.items() if is_bitstring(k) and isinstance(v, (int, float))}
        if numeric:
            total = float(sum(numeric.values()))
            for bits_key, value in numeric.items():
                worlds.setdefault(bits_key, float(value) / shots if total > 1.001 else float(value))
    return worlds


def theorem_proved() -> tuple[bool, float, str]:
    """Dependency-free exhaustive proof over all 2^16 bit worlds.

    We accept only worlds satisfying every ideal non-coin corridor equality, then
    check whether exactly one apparent escape door can be open. If no such world
    exists, the correlation theorem is proved for this finite model.
    """
    started = time.perf_counter()
    satisfying = 0
    counterexample = None
    for value in range(1 << N):
        bits = tuple((value >> i) & 1 for i in range(N))
        if not all(bits[u] == bits[v] for u, v in DOORS if (u, v) not in COIN_DOORS):
            continue
        satisfying += 1
        left_open = bits[3] == bits[7]
        right_open = bits[10] == bits[14]
        if left_open != right_open:
            counterexample = bits
            break
    proved = counterexample is None
    method = f"exhaustive finite proof: checked 2^{N} worlds; {satisfying} satisfy ideal constraints"
    return proved, (time.perf_counter() - started) * 1000, method


def certificate(bits: str) -> tuple[bool, str]:
    graph: dict[int, list[int]] = collections.defaultdict(list)
    for u, v in DOORS:
        if bits[u] == bits[v]:
            graph[u].append(v)
            graph[v].append(u)

    previous: dict[int, int | None] = {START: None}
    queue = collections.deque([START])
    while queue:
        current = queue.popleft()
        for nxt in graph[current]:
            if nxt not in previous:
                previous[nxt] = current
                queue.append(nxt)

    if EXIT not in previous:
        return False, "sealed{" + ",".join(map(str, sorted(previous))) + "}"

    path: list[int] = []
    node: int | None = EXIT
    while node is not None:
        path.append(node)
        node = previous[node]
    return True, "path " + "-".join(map(str, reversed(path)))


def maze_ascii(bits: str) -> str:
    rows: list[str] = []
    for row in range(4):
        line = ""
        below = ""
        for col in range(4):
            index = row * C + col
            line += "S" if index == START else "E" if index == EXIT else "o"
            if col < 3:
                line += "---" if (index, index + 1) in DOORS and bits[index] == bits[index + 1] else "   "
            below += ("|" if (index, index + 4) in DOORS and bits[index] == bits[index + 4] else " ") + "   "
        rows.append(line)
        if row < 3:
            rows.append(below.rstrip())
    return "\n".join(rows)


def mock_result(shots: int) -> dict[str, Any]:
    # Two independent correlated blocks. This is only a deterministic development fixture,
    # not an Atlas or quantum result.
    block = {7, 10, 11, 15}
    counts: collections.Counter[str] = collections.Counter()
    for _ in range(shots):
        x, y = random.getrandbits(1), random.getrandbits(1)
        counts["".join(str(y if i in block else x) for i in range(N))] += 1
    return {"counts": dict(counts)}


def run_atlas(api: str, key: str, mode: str, shots: int, poll_seconds: int = 3) -> tuple[Any, str, str]:
    operations = [
        {
            "type": "relationship",
            "qubits": [u, v],
            "paulis": {"ZZ": 0.0 if (u, v) in COIN_DOORS else 1.0},
        }
        for u, v in DOORS
    ]
    params = {
        "num_qubits": N,
        "coupling_map": [list(edge) for edge in DOORS],
        "operations": operations,
        "shots": shots,
    }
    # Atlas expects execution mode at the top level, not inside params.
    created = http_json(
        f"{api}/engines/graph-v1/process",
        {"mode": mode, "params": params},
        key,
    )
    job_id = created.get("job_id")
    if not job_id:
        raise RuntimeError(f"Atlas response contained no job_id: {created}")

    while True:
        status = http_json(f"{api}/jobs/{job_id}/status", key=key)
        state = status.get("status")
        print(f"Atlas job {job_id}: {state}", flush=True)
        if state in {"completed", "failed", "cancelled"}:
            break
        time.sleep(poll_seconds)
    if state != "completed":
        raise RuntimeError(json.dumps(status, indent=2))

    result_payload = http_json(f"{api}/jobs/{job_id}/result", key=key)
    return result_payload.get("result", result_payload), job_id, json.dumps(status)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "emu", "qpu"], default="mock")
    parser.add_argument("--shots", type=int, default=4096)
    parser.add_argument("--api", default=os.environ.get("MOTH_API_BASE", DEFAULT_API))
    parser.add_argument("--out", default="results")
    args = parser.parse_args()

    proved, proof_ms, proof_method = theorem_proved()
    if not proved:
        raise RuntimeError("The deterministic theorem did not prove; stop before Atlas run.")

    key = os.environ.get("MOTH_API_KEY", "")
    if args.mode == "mock":
        raw = mock_result(args.shots)
        source = "MOCK development fixture — not Atlas"
        job_id = "mock"
        status = "mock"
    else:
        if not key:
            raise SystemExit("MOTH_API_KEY is required for an Atlas run. Enter it only in the local terminal session.")
        raw, job_id, status = run_atlas(args.api, key, args.mode, args.shots)
        source = f"Atlas graph-v1 {args.mode} job {job_id}"

    worlds = extract_worlds(raw, args.shots)
    if not worlds:
        raise RuntimeError("No 16-bit worlds were found in the response. Preserve the raw response and update only the parser.")

    mass = sum(worlds.values()) or 1.0
    p_exit = 0.0
    rows: list[dict[str, Any]] = []
    for bits, probability in sorted(worlds.items(), key=lambda item: -item[1]):
        reachable, cert = certificate(bits)
        p_exit += probability * int(reachable)
        rows.append({
            "bits": bits,
            "probability": probability,
            "exit": reachable,
            "certificate": cert,
            "maze": maze_ascii(bits),
        })

    report = {
        "title": "Proof of Exit",
        "source": source,
        "job_id": job_id,
        "mode": args.mode,
        "shots": args.shots,
        "theorem_proved": proved,
        "proof_ms": proof_ms,
        "proof_method": proof_method,
        "p_exit_measured": p_exit / mass,
        "p_exit_independent_intuition": 0.75,
        "p_exit_ideal_theorem": 0.50,
        "probability_mass_parsed": mass,
        "worlds": rows,
        "atlas_status": status,
        "raw": raw,
    }
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"poe-{args.mode}-{time.strftime('%Y%m%d-%H%M%S')}.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"PROOF OF EXIT | {source} | shots {args.shots}")
    print(f"Correlation theorem: PROVED ({proof_ms:.1f} ms; {proof_method})")
    print(f"P(exit): measured {report['p_exit_measured']:.3f} | independent intuition 0.750 | ideal theorem 0.500")
    print(f"saved {output}")


if __name__ == "__main__":
    main()
