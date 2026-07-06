# verl — CLAUDE.md

Magnon mirror of the verl (Volcano Engine Reinforcement Learning) library.
Part of MagnonOS Project-Aethra.

## Purpose

Magnon's private mirror of the [volcengine/verl](https://github.com/volcengine/verl) flexible,
efficient RL training library for LLMs. Used by Project-Aethra and Project-Infera for RLHF,
RLAIF, and theorem-proving RL training pipelines (e.g., kimina-prover-rl).

Reference paper: HybridFlow (EuroSys 2025). Upstream: ByteDance Seed team.

## Tech stack

- Python · PyTorch
- Ray (distributed training)
- vLLM / SGLang inference backends
- FastAPI (service endpoints)

## Dev commands

```bash
pip install -e .
# Or, to include dev dependencies:
pip install -e '.[dev]'
# See docs/ and upstream README for full setup

# Run development server
python -m <module>

# Run with Docker
docker-compose up
```

## Testing

```bash
pytest
```

## Key conventions

- This is a **mirror** — do not make Magnon-specific changes on the main branch.
- Magnon training configs and experiment scripts go in `Project-Infera/kimina-prover-rl` or `Project-Aethra/rlhf-*-service`.
- Upstream contributions go to volcengine/verl.

## What NOT to do

- Never commit model checkpoints, training data, or API credentials.
- Never push Magnon-specific training configs to this mirror.
- Never use `ubuntu-latest` CI runners — always `magnon-enterprise-runners`.

## CI

All GitHub Actions workflow jobs use `runs-on: magnon-enterprise-runners`.
