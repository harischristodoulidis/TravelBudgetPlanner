# Worker

A simple background worker that logs a heartbeat every 5 seconds.

## Run

```bash
python worker/worker.py
```

The worker runs until manually stopped with `Ctrl+C`.

## Output

```
2026-05-22 10:00:00,000 [INFO] Worker started
2026-05-22 10:00:00,001 [INFO] Worker heartbeat at 2026-05-22T10:00:00.001234
2026-05-22 10:00:05,002 [INFO] Worker heartbeat at 2026-05-22T10:00:05.002345
...
```

## Run alongside the API

Open two terminals from the `backend/` directory:

```bash
# Terminal 1 — API
uvicorn service.main:app --reload

# Terminal 2 — Worker
python worker/worker.py
```
