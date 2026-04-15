# accel-sparse-attention

Accelerated Sparse Attention Retrieval — AccelForge models for the
LongSight architecture (MICRO '25, Quinn et al.).

## Repository layout

| File / directory | Purpose |
|---|---|
| `archs/longsight.yaml` | LongSight architecture (GPU + CXL-attached DReX) |
| `archs/traditional.yaml` | Baseline traditional accelerator |
| `archs/both.yaml` | Combined architecture template |
| `prob.yaml` | Full workload (dense + sparse attention) |
| `prob_dense.yaml` | Dense-only attention workload |
| `prob_sparse.yaml` | Sparse-only attention workload |
| `map.yaml` | LongSight pipeline mapping (dense ‖ sparse) |
| `map_dense.yaml` | Dense-only mapping |
| `map_sparse.yaml` | Sparse-only mapping |
| `map_traditional_sparse.yaml` | Traditional architecture mapping for the full workload |
| `impl.ipynb` | Jupyter notebook with energy/latency benchmarks |
| `longsight.pdf` | Reference paper |

## Quick start

```bash
docker compose up
```

Open the Jupyter URL printed in the terminal and run `impl.ipynb`.
