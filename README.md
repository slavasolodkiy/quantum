<!-- ============================================================
     PROOF OF EXIT · README
     Teenage-Engineering × Nothing × acid-glitch aesthetic
     ============================================================ -->

<div align="center">

<pre>
██████╗ ██████╗  ██████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝
██████╔╝██████╔╝██║   ██║█████╗  █████╗
██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██╔══╝
██║     ██║  ██║╚██████╔╝██║     ██║      ███████╗██╗  ██╗██╗████████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝╚═╝
</pre>

# `PROOF OF EXIT`

**When two doors are not two chances.**
A real Moth Atlas `graph-v1` job · an exhaustive finite proof · an honest mismatch — and zero claims the evidence can't carry.

<img src="https://img.shields.io/badge/ENGINE-graph--v1-c8ff00?style=for-the-badge&labelColor=0b0d11&color=c8ff00&logoColor=000000" alt="engine">
<img src="https://img.shields.io/badge/MODE-emu%20%2F%20aer-35f2ff?style=for-the-badge&labelColor=0b0d11" alt="mode">
<img src="https://img.shields.io/badge/STATUS-completed-00e676?style=for-the-badge&labelColor=0b0d11" alt="status">
<img src="https://img.shields.io/badge/SHOTS-4096-ff2d9a?style=for-the-badge&labelColor=0b0d11" alt="shots">
<img src="https://img.shields.io/badge/MOTH%20HACK-2026-orange?style=for-the-badge&labelColor=0b0d11" alt="moth hack">
<img src="https://img.shields.io/badge/FQxI-challenge%20%2311-9b7bff?style=for-the-badge&labelColor=0b0d11" alt="fqxi">

</div>

---

## ▚ THE THREE NUMBERS

| READOUT | VALUE | WHAT IT ACTUALLY IS |
|---|---|---|
| `01 · INDEPENDENT-DOOR INTUITION` | **75.0%** | Two doors × ½ each — valid *only if* the doors are independent. An assumption, not a visual fact. |
| `02 · BALANCED TARGET PREDICTION` | **50.0%** | Ideal dependent model: bridge doors move together; the correlation is balanced. |
| `03 · OBSERVED ATLAS EMULATION` | **100.0%** | All 4,096 shots returned `0000000000000000` — a world with a certified exit path. |

The gap between row 02 and row 03 is not a bug to hide. **It is the result.**

## ▚ THE EXPERIMENT IN ONE BREATH

A 4×4 maze is a 16-bit world; a corridor opens when adjacent rooms agree. We asked the
**Moth Atlas Quantum Graph Engine** (`graph-v1`, mode `emu`, backend `aer`) to sample 4,096
shots of a 16-qubit state whose measured edges should match requested Pauli expectations —
including **ZZ = 0 on the two bridge edges** `(3,7)` and `(10,14)`. The completed job returned
the all-zero world in every shot. Tomography reported **ZZ = 1**. Requested ≠ observed.

A dependency-free exhaustive proof checks all **65,536** sixteen-bit worlds: exactly **4**
satisfy the ideal non-bridge equality constraints, and **none** has exactly one open bridge —
so when the constraints hold, the bridge doors agree. The all-zero world satisfies them.

```
        ┌──────────────────────┐         ┌──────────────────────────┐
        │  MOTH ATLAS ENGINE   │  JSON   │   CLASSICAL VERIFIER     │
        │  graph-v1 · emu/aer  ├────────►│  dependency-free Python  │
        │  role: samples the   │         │  role: explains what the │
        │  16-node network     │         │  sample means            │
        └──────────────────────┘         └──────────────────────────┘
              engine proposes ──────►  classical logic disposes
```

## ▚ QUICKSTART

```bash
# 1 · mock run — no API key, deterministic fixture
python3 poe.py --mode mock

# 2 · real Atlas run (key lives only in your terminal session)
export MOTH_API_KEY="..."
python3 poe.py --mode emu --shots 4096

# 3 · render the evidence page
python3 render.py results/poe-emu-*.json --out proof-of-exit.html
```

`poe.py` refuses to proceed if the finite theorem does not prove first — the classical
certificate runs before and after any Atlas call.

## ▚ EVIDENCE LEDGER

| ARTIFACT | FILE | STATUS |
|---|---|---|
| Credential-free request | `evidence/atlas-request.json` | preserved |
| Completed job status | `evidence/atlas-status.json` | `completed` |
| Full raw Atlas result | `evidence/atlas-raw-result.json` | unedited |
| Exhaustive proof | `poe.py → theorem_proved()` | **proved** (`2^16` worlds) |
| Demo | [captioned](https://www.solodkiy.cv/proof-of-exit.html) | [X](https://x.com/NansenID/status/2105722251702063540) [play]((https://quantum-curious-kids.lovable.app) |

Job ID `a03509aa-4b7b-4a0a-bc16-c35d3f14514f` · submitted `2026-10-01T15:44:00Z` ·
completed `2026-10-01T15:44:02Z` · path certificate `0-1-2-3-7-11-15`.

## ▚ HONEST LIMITATIONS — READ BEFORE SHARING

> - Emulation only: `mode emu`, backend `aer`. **No physical QPU, no quantum advantage claimed.**
> - The requested zero bridge correlations (ZZ=0) were **not realized**; returned tomography shows ZZ=1. The cause of the target/output mismatch is **openly unresolved**.
> - The intended 50% balanced-bridge target is therefore **not validated** by this run.
> - The finite theorem is conditional: it holds when the non-bridge equality constraints hold. The all-zero returned world satisfies them; bitstring endianness cannot change this run's certificate because every returned bit is zero.

## ▚ PROJECT LAYOUT

```
├── poe.py            # Atlas runner + exhaustive proof + path certificates
├── render.py         # evidence page generator (proof-of-exit.html)
├── evidence/         # raw, unedited Atlas request / status / result JSON
└── proof-of-exit.html  # interactive specimen report (self-contained)
```

## ▚ Tested by:

- **Slava Solodkiy** — [solodkiy.cv/tech](https://www.solodkiy.cv/tech.html) · [my olares lab](https://www.solodkiy.cv/olares.html) · 
- Built for **Moth Hack 2026** · guest challenge **FQxI #11** — *Atlas samples. Logic explains.*

<div align="center">

`ATLAS SAMPLES · LOGIC EXPLAINS · EVIDENCE, NOT HYPE`

</div>
