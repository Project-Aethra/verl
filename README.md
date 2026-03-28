# verl — Shared VeRL RL Training Infrastructure for MagnonOS

Shared VeRL RL training infrastructure for MagnonOS. This directory is the local mirror of
[magnon-aethra/verl](https://github.com/magnon-aethra/verl) and provides the canonical flox
environment definition used across all MagnonOS projects that perform RLHF or GRPO fine-tuning.

---

## Mirrors

| Mirror repo | Purpose |
|---|---|
| [magnon-aethra/verl](https://github.com/magnon-aethra/verl) | Core VeRL library (upstream: volcengine/verl) |
| [magnon-aethra/verl-recipe](https://github.com/magnon-aethra/verl-recipe) | MagnonOS training recipes (GRPO, PPO, DPO configs) |
| [magnon-aethra/verl-agent](https://github.com/magnon-aethra/verl-agent) | Agent-environment rollout interface for VeRL |
| [magnon-aethra/verl-tool](https://github.com/magnon-aethra/verl-tool) | Tool-use reward functions and reward router bridges |

---

## Project-Specific Extensions

Each MagnonOS project that consumes VeRL maintains its own extension package on top of this shared base:

| Project | Extension location | Domain |
|---|---|---|
| Project-Volterra | `Project-Volterra/volterra-sdk/verl/` | EDA reward: cocotb simulation pass/fail, DRC clean signal |
| Project-Infera | `Project-Infera/infera-mono/verl/` | Proof reward: Lean 4 proof discharge outcome |
| Project-Metic | `Project-Metic/project-metic-mono/verl/` | Compiler reward: binary verification certificate issued |
| Project-Lightcone | `Project-Lightcone/lightcone-mono/verl/` | Series B drill reward: scenario completion score |
| Project-Moirae | `Project-Moirae/moirae-mono/verl/` | Workflow step reward: Moirae step executor outcome |
| Project-Mouseion | `Project-Mouseion/mouseion-mono/verl/` | Provenance reward: W3C PROV lineage completeness |

---

## Activate

```bash
cd /path/to/your/project
flox activate --dir /path/to/Project-Aethra/verl
```

Or, if your project imports this environment via `.flox/env/manifest.toml`:

```toml
[include]
environments = [
  { remote = "magnon/aethra-verl" },
]
```

Then simply:

```bash
flox activate
```

---

## Usage: GRPO Fine-Tuning via veringen-verl-service

The `veringen-verl-service` API exposes a REST interface for submitting GRPO fine-tuning jobs
against VeriGen (RTL generation model) using Volterra EDA reward signals.

### Submit a GRPO job

```bash
curl -X POST http://veringen-verl-service:8560/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_type": "grpo",
    "base_model": "magnon-aethra/verigen-7b",
    "recipe": "grpo_eda_reward_v1",
    "reward_router": "http://verl-reward-router:8561",
    "dataset": "magnon-aethra/eda-grpo-prompts-r104",
    "training": {
      "max_steps": 500,
      "rollout_n": 8,
      "kl_coeff": 0.05,
      "learning_rate": 1e-6
    },
    "reward_config": {
      "eda_reward_weight": 0.7,
      "format_reward_weight": 0.3,
      "cocotb_timeout_s": 120
    },
    "ray_address": "ray://ray-cluster:10001"
  }'
```

### Check job status

```bash
curl http://veringen-verl-service:8560/api/v1/jobs/{job_id}
```

### Environment variable overrides for production

```bash
export VERL_MOCK="false"
export MAGNON_VERL_REWARD_ROUTER="http://verl-reward-router:8561"
export RAY_ADDRESS="ray://ray-cluster:10001"
export CUDA_VISIBLE_DEVICES="0,1,2,3"
flox activate
```

---

## Development

```bash
# Install VeRL and companion packages from mirrors
pip install git+https://github.com/magnon-aethra/verl.git
pip install git+https://github.com/magnon-aethra/verl-agent.git
pip install git+https://github.com/magnon-aethra/verl-tool.git
pip install git+https://github.com/magnon-aethra/verl-recipe.git

# Run tests
pytest tests/ -v
```

---

## Integration Points

- **Reward router:** `verl-reward-router` service routes reward requests to per-project reward
  functions; set `MAGNON_VERL_REWARD_ROUTER` to its URL in production.
- **Ray cluster:** distributed rollout and training use the Ray cluster at `RAY_ADDRESS`.
- **Wandb:** training metrics are logged to the `magnon-verl` W&B project when `VERL_MOCK=false`.
- **Mouseion:** trained model checkpoints and reward histories are registered as Mouseion assets
  via `magnon-aethra/verl-tool`.
