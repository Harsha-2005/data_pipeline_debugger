# 🔧 OpenEnv — Data Pipeline Debugger

> **A production-grade reinforcement learning environment where AI agents learn to diagnose and repair broken ETL pipelines — featuring curriculum learning, multi-agent cooperation, advanced reward shaping, explainable AI, and a live interactive web dashboard.**

[![OpenEnv](https://img.shields.io/badge/OpenEnv-compliant-blue)](https://openenv.dev)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Tasks](https://img.shields.io/badge/tasks-5%20difficulty%20tiers-orange)](#task-difficulty-tiers)
[![Tests](https://img.shields.io/badge/tests-47%20passed-brightgreen)](#testing)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](#cicd)
[![HF Space](https://img.shields.io/badge/%F0%9F%A4%97%20Space-Live-yellow)](https://huggingface.co/spaces/Harsha-2005/openenv-datapipeline)

---

## 🏆 Meta PyTorch Hackathon × Scaler SST — Grand Finale

| | |
|---|---|
| **Team** | Maddala Hema Narasimha Harsha Pavan · Challa Lakshmi Thrinayanani · Brahmadevuni Gagan Kumar Reddy |
| **Submission** | Phase 1 ✅ · Phase 2 ✅ · Grand Finale 🎯 |
| **Live Space** | [huggingface.co/spaces/Harsha-2005/openenv-datapipeline](https://huggingface.co/spaces/Harsha-2005/openenv-datapipeline) |

---

## 📖 Overview

Every company running data pipelines faces recurring nightmares: columns arrive with the wrong types, records get duplicated during ingestion, null values propagate silently, business constraints get violated, and pipeline stages execute in the wrong order.

**OpenEnv Data Pipeline Debugger** turns this real-world problem into a rigorous reinforcement learning environment. An AI agent observes a broken pipeline, selects repair actions step-by-step, receives shaped rewards for each fix, and is scored on how well it restores data quality — all under a step budget and SLA constraint.

### What Makes It Novel

| Feature | Description |
|---|---|
| **5 Difficulty Tiers** | Easy → Expert with progressively complex bug patterns |
| **Curriculum Learning** | Auto-advances the agent when it masters each tier (score ≥ 0.90 for 3 consecutive episodes) |
| **Multi-Agent Cooperation** | Inspector → Fixer → Validator pipeline via MessageBus |
| **Interactive Web Dashboard** | Live task runner, benchmarks, system docs — all in-browser |
| **Competition Mode** | Side-by-side agent arena with split-screen comparison |
| **Auto-Demo Mode** | Self-running tabbed presentation — no CLI needed |
| **Dynamic Bug Injection** | Procedural generation of pipeline breakages (nulls, duplicates, schema drift, outliers) |
| **Advanced Shaped Rewards** | Novelty bonuses, cascade bonuses, regression penalties, efficiency multipliers |
| **Explainable AI Output** | Per-step reasoning, observation summaries, reward component breakdowns |
| **Benchmark Baselines** | Random, Greedy, and Fixed-Strategy agents for comparison |
| **Comprehensive Analytics** | Auto-generated HTML reports with mastery timelines and efficiency charts |
| **CI/CD Pipeline** | GitHub Actions for lint, test, and server health checks |

---

## 🗂️ Project Structure

```
openenv-datapipeline/
├── app.py                      # FastAPI server — REST API + HTML endpoints
├── dashboard.py                # Interactive Web Dashboard (sidebar nav, runner, benchmarks)
├── demo.py                     # Self-running Auto-Demo Mode for judges
├── compete.py                  # Side-by-side Agent Competition Arena
├── analytics.py                # Training Report generator (Chart.js)
├── bug_injector.py             # Dynamic Data Quality Fault Injection
├── visualize.py                # Reward chart + Replay Dashboard generators
│
├── benchmarks/
│   ├── agents.py               # RandomAgent, GreedyAgent, FixedStrategyAgent
│   └── run_benchmarks.py       # Evaluation runner + HTML export
│
├── env/
│   ├── environment.py          # DataPipelineEnv + StepRecord (Explainable AI)
│   └── models.py               # Pydantic models: Action, Observation, PipelineState
│
├── tasks/
│   ├── definitions.py          # 3 base tasks + TASK_REGISTRY + TASK_INFO
│   └── extra_tasks.py          # VeryHard + Expert tasks
│
├── graders/
│   └── graders.py              # 5 graders + score_pipeline() entry point
│
├── train.py                    # Curriculum training loop + replay + analytics
├── inference.py                # LLM-powered inference + rule-based fallback
├── curriculum.py               # CurriculumManager + AgentSkillProfile
├── multi_agent.py              # Inspector → Fixer → Validator cooperative pipeline
│
├── server/
│   └── app.py                  # Uvicorn entry point
│
├── tests/
│   └── test_env.py             # 49 tests — 47 pass, 2 skip
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
│
├── Makefile                    # One-command setup, test, serve, train, bench
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── openenv.yaml                # OpenEnv environment specification
└── .gitignore
```

---

## 🎯 Task Difficulty Tiers

| Task ID | Difficulty | Max Steps | Rows | Injected Bugs | Best Score |
|---|---|---|---|---|---|
| `task_easy_schema_fix` | 🟢 Easy | 10 | 30 | 5 | 0.900 |
| `task_medium_data_quality` | 🟡 Medium | 20 | 65 | 6 | 0.999 |
| `task_hard_pipeline_orchestration` | 🔴 Hard | 40 | 107 | 13 | 0.981 |
| `task_veryhard_streaming_pipeline` | 🟣 Very Hard | 50 | 160 | 13 | — |
| `task_expert_multi_source_join` | ⚫ Expert | 60 | 212 | 17 | — |

Each task builds on the previous one — the agent must not only fix data quality issues but also manage pipeline orchestration, streaming ingestion, and multi-source joins as difficulty increases.

---

## ⚙️ Action Space (11 Actions)

| Action | Description |
|---|---|
| `inspect` | Observe current pipeline state, null counts, duplicates |
| `cast_column` | Fix type mismatches (e.g., `str → int`, `object → float64`) |
| `drop_nulls` | Remove rows with null values in a specified column |
| `fill_nulls` | Fill nulls with the median or a specified value |
| `drop_duplicates` | Remove duplicate rows from the dataset |
| `filter_outliers` | Remove IQR outliers from a numeric column |
| `rename_column` | Fix column naming violations |
| `reorder_stages` | Fix pipeline stage ordering (Hard+ difficulty only) |
| `apply_business_rule` | Enforce domain rules: `discount_lte_1`, `fraud_score_lte_1`, `currency_3char`, `country_2char` |
| `validate` | Score the current state without ending the episode |
| `submit` | Final submission — ends the episode and returns the score |

---

## 💰 Advanced Reward Function

The reward function is multi-component, encouraging efficient, diverse, and correct repair behaviour:

```python
R(t) = Δprogress(t)
     − 0.02 × step_cost
     − 0.05 × repeat_penalty
     + 0.02 × novelty_bonus
     + 0.03 × cascade_bonus
     − 0.01 × regression_penalty
     + 0.05 × efficiency_bonus
     + 0.10 × score × submit_bonus
```

| Component | Value | Description |
|---|---|---|
| `Δprogress` | variable | Increase in data quality score from this step |
| `step_cost` | −0.02 | Every action has a cost — encourages efficiency |
| `repeat_penalty` | −0.05 | Penalises repeating the same action (except `validate`/`submit`) |
| `novelty_bonus` | +0.02 | Rewards using productive actions not recently tried |
| `cascade_bonus` | +0.03 | Rewards chaining multiple consecutive successful fixes |
| `regression_penalty` | −0.01 | Penalises actions that worsen the pipeline score |
| `efficiency_bonus` | +0.05 | Scales with how few steps were used to reach a high score |
| `submit_bonus` | +0.10 × score | Large reward for submitting a high-quality corrected pipeline |

> Scores are clipped to the open interval `(0.001, 0.999)` per OpenEnv specification.

---

## 🧠 Key Components

### Environment (`env/environment.py`)

`DataPipelineEnv` is the core RL environment. It exposes:
- `reset(task_id, seed)` → returns an `Observation`
- `step(action)` → returns an `Observation` + `StepRecord`

Each `StepRecord` includes full explainability metadata: the agent's reasoning, an observation summary, reward component breakdown, and alternative actions considered.

### Graders (`graders/graders.py`)

Five graders score the pipeline state per task:
- **`grade_easy`** — schema correctness, null rate, duplicate rate
- **`grade_medium`** — extended data quality checks
- **`grade_hard`** — adds stage ordering and business rule enforcement
- **`grade_veryhard`** — streaming-specific latency and throughput metrics
- **`grade_expert`** — multi-source join quality, referential integrity

The unified entry point `score_pipeline(state, task_id)` routes to the correct grader.

### Curriculum Learning (`curriculum.py`)

`CurriculumManager` tracks the agent's `AgentSkillProfile` across episodes. When the agent achieves a score ≥ 0.90 for 3 consecutive episodes, the curriculum automatically advances to the next difficulty tier:

```
Easy → Medium → Hard → VeryHard → Expert
```

### Multi-Agent System (`multi_agent.py`)

A cooperative three-agent pipeline communicates via a shared `MessageBus`:

```
Inspector  →  identifies bug categories and priorities
    ↓
Fixer      →  selects and applies repair actions
    ↓
Validator  →  scores the result and flags regressions
```

### Dynamic Bug Injector (`bug_injector.py`)

`DynamicBugInjector` procedurally generates pipeline faults at configurable severity:
- **Null injection** — random null introduction per column
- **Duplicate injection** — row duplication at variable rates
- **Schema drift** — column type corruption
- **Outlier injection** — extreme value insertion

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- `pip` or `uv`
- (Optional) Docker for containerised deployment
- (Optional) HF Token for LLM-powered inference

### Installation

```bash
git clone https://github.com/Harsha-2005/data_pipeline_debugger
cd data_pipeline_debugger

python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows PowerShell

pip install -r requirements.txt
```

Or using the Makefile:

```bash
make setup
```

### Run Tests

```bash
PYTHONPATH=. python -m pytest tests/test_env.py -v
# Expected: 47 passed, 2 skipped, 0 failed
```

### Start the Server

```bash
PYTHONPATH=. python app.py
```

| Endpoint | URL |
|---|---|
| API Server | `http://localhost:7860` |
| Swagger Docs | `http://localhost:7860/docs` |
| Dashboard | `http://localhost:7860/dashboard` |
| Auto-Demo | `http://localhost:7860/demo` |
| Competition | `http://localhost:7860/compete` |

### Training

```bash
# Quick smoke test (5 steps)
python train.py --steps 5 --task task_easy_schema_fix --replay-every 1 --replay-dir replays/

# Full curriculum training (1000 episodes)
python train.py --curriculum --steps 1000 --replay-dir replays/
```

### Run Benchmarks

```bash
python benchmarks/run_benchmarks.py
```

---

## 🔌 REST API Reference

The live HF Space exposes a fully OpenEnv-compliant HTTP API:

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/tasks` | GET | List all available tasks |
| `/reset` | POST | Reset environment for a task |
| `/step` | POST | Apply an action, receive observation + reward |
| `/state` | GET | Get full internal `PipelineState` |
| `/dashboard` | GET | Interactive web dashboard |
| `/demo` | GET | Self-running auto-demo |
| `/compete` | GET | Multi-agent competition arena |
| `/api/benchmark` | GET | Run baseline benchmark comparison |
| `/docs` | GET | Interactive Swagger API docs |

#### Example Usage

```bash
BASE=https://Harsha-2005-openenv-datapipeline.hf.space

# Health check
curl $BASE/health

# List tasks
curl $BASE/tasks

# Reset environment
curl -X POST $BASE/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_hard_pipeline_orchestration", "seed": 42}'

# Take a step
curl -X POST $BASE/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "inspect"}'

# Submit
curl -X POST $BASE/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "submit"}'
```

---

## 📊 Training Results

```
Total Episodes:         102
Starting Score:         0.629  (Hard task, episode 1)
Best Score:             0.981  (Hard task, episode 69)
Final Average (20 ep):  0.966
Total Improvement:      +0.356

Curriculum Progression:
  Easy   task:  0.82 → 0.90  (advance at episode 18)
  Medium task:  0.85 → 0.95  (advance at episode 41)
  Hard   task:  0.629 → 0.981 (best at episode 69)
```

---

## 🏗️ Architecture Overview

```
Agent (LLM: Qwen2.5-72B via HF Router)
        │
        ▼
DataPipelineEnv  (env/environment.py)
        │  reset()  → Observation
        │  step()   → Observation + StepRecord
        │
        ├── TASK_REGISTRY  (tasks/definitions.py)
        │       └── build_state(seed) → PipelineState
        │
        ├── Action Dispatch (11 handlers)
        │       └── pandas operations on live DataFrame
        │
        ├── Advanced Reward Shaper
        │       └── novelty + cascade + regression + efficiency
        │
        ├── score_pipeline  (graders/graders.py)
        │       └── grade_easy / grade_medium / grade_hard / grade_veryhard / grade_expert
        │
        ├── StepRecord → env.history → generate_replay_html()
        │       └── reasoning + observation_summary + reward_components
        │
        └── Web Endpoints (app.py)
                ├── /dashboard   — Interactive Dashboard
                ├── /demo        — Auto-Demo Mode
                ├── /compete     — Competition Arena
                └── /api/benchmark — Baseline Evaluation
```

---

## 🧪 Testing

```bash
PYTHONPATH=. python -m pytest tests/test_env.py -v
```

| Test Class | Tests | Status |
|---|---|---|
| `TestReset` | 6 | ✅ |
| `TestStep` | 8 | ✅ |
| `TestState` | 4 | ✅ |
| `TestActions` | 7 | ✅ (2 skipped — task-specific columns) |
| `TestGraders` | 6 | ✅ |
| `TestRewardFunction` | 4 | ✅ |
| `TestTaskInfo` | 3 | ✅ |
| `TestHistory` | 7 | ✅ |
| `TestReplayIntegration` | 4 | ✅ |
| **Total** | **49** | **47 passed, 2 skipped** |

---

## ⚙️ CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

- **Matrix**: Python 3.10, 3.11, 3.12
- Compile check all modules
- Full test suite
- Server health check

---

## 🐳 Docker & HF Deployment

```bash
# Build and run locally
docker build -t openenv-datapipeline .
docker run -p 7860:7860 \
  -e HF_TOKEN=hf_xxx \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  openenv-datapipeline

# Deploy to Hugging Face Space
python -c "
from huggingface_hub import HfApi
HfApi().upload_folder(
    folder_path='.',
    repo_id='Harsha-2005/openenv-datapipeline',
    repo_type='space',
    ignore_patterns=['venv/', '__pycache__/', '.git/', '*.pyc', 'replays/', '*.zip']
)
"
```

---

## 📋 Makefile Commands

| Command | Description |
|---|---|
| `make setup` | Install all dependencies |
| `make test` | Run the full test suite |
| `make serve` | Start the environment server on port 7860 |
| `make train` | Run 50-episode curriculum training with replays |
| `make infer` | Run inference on all tasks |
| `make bench` | Run baseline benchmark comparison |
| `make demo` | Generate a sample replay episode |
| `make lint` | Compile-check all Python modules |
| `make clean` | Remove generated files and HTML reports |

---

## 👥 Team

| Name | Role |
|---|---|
| **Maddala Hema Narasimha Harsha Pavan** | Team Lead — Environment Design, Training Loop, Replay Dashboard |
| **Challa Lakshmi Thrinayanani** | Multi-Agent Architecture, Graders |
| **Brahmadevuni Gagan Kumar Reddy** | FastAPI Server, Docker, HF Deployment |

---

## 📄 License

MIT © 2026 OpenEnv Data Pipeline Debugger Team
