# Examples

The examples in this repository are intentionally lightweight and
teaching-oriented.

- `end_to_end_walkthrough.py` is the canonical composed workflow example. It
  uses umbrella imports, a real packaged problem, a managed llama.cpp workflow
  agent, canonical experiment artifact export, and event-table validation.
- `basic_usage.py` remains the smallest possible import-surface smoke example.

Run locally with:

```bash
make run-example
make examples-test
```

`make run-example` uses a managed `llama.cpp` runtime. Install
`llama-cpp-python` first, and optionally set `LLAMA_CPP_MODEL` to point at a
specific local GGUF file.
`make examples-test` skips the live walkthrough unless `RUN_LIVE_EXAMPLE=1`.
