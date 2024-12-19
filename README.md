# Dagster Shared

---

<!-- TOC -->
* [Dagster Shared](#dagster-shared)
  * [Brief](#brief)
* [Setup](#setup)
  * [Clone Repo](#clone-repo)
  * [Install `dagster-shared`](#install-dagster-shared)
  * [Dagster](#dagster)
    * [`dagster.yaml`](#dagsteryaml)
    * [`workspace.yaml`](#workspaceyaml)
* [Run Dagster](#run-dagster)
<!-- TOC -->

---

## Brief

> **_Note_**: In progress

# Setup

## Clone Repo

```shell
git clone https://github.com/michimussato/dagster-shared.git
cd dagster-shared
```

## Install `dagster-shared`

```shell
pip install --upgrade pip setuptools setuptools_scm tox
pip install -e .[dagster_dev]
```

## Dagster

### `dagster.yaml`

```shell
mkdir -p /dagster/materializations
cat > /dagster/materializations/dagster.yaml << "EOF"
## https://docs.dagster.io/guides/limiting-concurrency-in-data-pipelines
run_queue:
  max_concurrent_runs: 1
  block_op_concurrency_limited_runs:
    enabled: true
concurrency:
  default_op_concurrency_limit: 1
telemetry:
  enabled: false
#run_monitoring:
#  enabled: true
#  free_slots_after_run_end_seconds: 300
auto_materialize:
  enabled: true
  use_sensors: true
EOF
```

### `workspace.yaml`

```shell
mkdir -p /dagster
cat > /dagster/workspace.yaml << "EOF"
# Refs:
# - https://docs.dagster.io/concepts/code-locations
# - https://dagster.io/blog/dagster-code-locations
load_from:
  - python_module:
      working_directory: src/dagster
      module_name: dagster_shared
      location_name: "Dagster Shared"
EOF
```

# Run Dagster

```shell
DAGSTER_HOME="/dagster/materializations" dagster dev --workspace "/dagster/workspace.yaml"
```
