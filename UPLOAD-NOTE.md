# Files missing from the public repository

Copy this directory's contents into the root of `slavasolodkiy/quantum`.
The existing `README.md` and `LICENSE` should remain.

This package contains:
- `poe.py` — runner, exhaustive proof and certificates (API request shape corrected to match the successful live Atlas contract)
- `atlas_real_run.py` — exact guarded runner used for the recorded job
- `render.py` — HTML renderer
- `proof-of-exit.html` — generated self-contained report
- `results/poe-emu-real.json` — parsed real run
- `evidence/` — credential-free request, completed status and raw result

No API key is included.
