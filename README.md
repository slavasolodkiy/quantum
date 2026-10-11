<!-- ============================================================
     PROOF OF EXIT · README
     Teenage-Engineering × Nothing × acid-glitch aesthetic
     Sovereign Agent Lab · design system v2
     ============================================================ -->

<div align="center">

<pre>
┌─────────────────────────────────┐
│  P R O O F   O F   E X I T      │
└─────────────────────────────────┘
</pre>

# `PROOF OF EXIT`

**When two doors are not two chances.**

A real Moth Atlas `graph-v1` job, an exhaustive finite proof, an honest mismatch — and zero claims the evidence cannot carry.

**Role in the Lab:** a parallel curiosity-led exhibit. The same evidence discipline is tested in a different engine; it is not a component of AuthorityClaw.

<img src="https://img.shields.io/badge/ENGINE-graph--v1-c8ff00?style=for-the-badge&labelColor=0b0d11" alt="engine">
<img src="https://img.shields.io/badge/MODE-emu%20%2F%20aer-35f2ff?style=for-the-badge&labelColor=0b0d11" alt="mode">
<img src="https://img.shields.io/badge/STATUS-completed-00e676?style=for-the-badge&labelColor=0b0d11" alt="status">
<img src="https://img.shields.io/badge/SHOTS-4096-ff2d9a?style=for-the-badge&labelColor=0b0d11" alt="shots">
<img src="https://img.shields.io/badge/ROLE-parallel%20curiosity%20exhibit-9b7bff?style=for-the-badge&labelColor=0b0d11" alt="role">

[Interactive evidence page](https://www.solodkiy.cv/proof-of-exit.html) · [Full research trail — Sovereign Agent Lab](https://www.solodkiy.cv/sovereign-agent-lab.html)

</div>

---

## ▚ THE THREE NUMBERS

| READOUT | VALUE | WHAT IT ACTUALLY IS |
|---|---:|---|
| Independent-door intuition | **75.0%** | Two doors × ½ each — valid only if the doors are independent. |
| Balanced target prediction | **50.0%** | Ideal dependent model: bridge doors move together; correlation balanced. |
| Observed Atlas emulation | **100.0%** | All 4,096 shots returned the all-zero world, which has a certified exit path. |

The gap between target and output is not hidden. **It is the invitation to inspect, reproduce and ask the next question.**

## ▚ THE EXPERIMENT IN ONE BREATH

A 4×4 maze is a 16-bit world; a corridor opens when adjacent rooms agree. A Moth Atlas Quantum Graph Engine job (`graph-v1`, mode `emu`, backend `aer`) sampled 4,096 shots of a 16-qubit state whose measured edges were intended to match requested Pauli expectations. The completed job returned the all-zero world in every shot. Tomography reported `ZZ = 1` on the bridge edges; requested zero bridge correlations were not realised.

A dependency-free exhaustive proof checks all **65,536** sixteen-bit worlds: exactly **4** satisfy the ideal non-bridge equality constraints, and **none** has exactly one open bridge. The returned all-zero world satisfies those constraints and contains an exit path.

```text
        ┌──────────────────────┐         ┌──────────────────────────┐
        │  MOTH ATLAS ENGINE   │  JSON   │   CLASSICAL VERIFIER     │
        │  graph-v1 · emu/aer  ├────────►│  dependency-free Python  │
        │  samples the network │         │  explains the sample     │
        └──────────────────────┘         └──────────────────────────┘
              engine proposes ──────►  classical logic disposes
```

## ▚ QUICK START

```bash
# deterministic fixture, no API key
python3 poe.py --mode mock

# real Atlas emulation
export MOTH_API_KEY="..."
python3 poe.py --mode emu --shots 4096

# render the evidence page
python3 render.py results/poe-emu-*.json --out proof-of-exit.html
```

`poe.py` refuses to proceed if the finite theorem does not prove first; the classical certificate runs before and after any Atlas call.

## ▚ HONEST LIMITATIONS

- Emulation only: `mode emu`, backend `aer`. **No physical QPU and no quantum advantage claimed.**
- The requested zero bridge correlations were not realised; the cause remains unresolved.
- The intended 50% balanced-bridge target is not validated by this run.
- The finite theorem is conditional on the stated non-bridge equality constraints.

The value here is not a judicial verdict on the engine. It is a preserved, repeatable curiosity: target, output and mismatch remain visible so someone else can try again.

## ▚ COLOPHON

MIT licence.

<div align="center">

`ATLAS SAMPLES · LOGIC EXPLAINS · TARGET, OUTPUT AND MISMATCH STAY VISIBLE`

</div>
