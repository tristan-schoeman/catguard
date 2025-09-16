
# CatGuard 🐱🔕

Humane, DIY cat-scratch deterrent using **vision**, **audio**, and **controls**.  
Runs on a Raspberry Pi or any small Linux/Windows PC.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt

# Add a sound file:
# assets/doorbell.wav

python -m src.main
```
Edit `config.yaml` to tune thresholds, schedule, and deterrent mode.

## Notes
- Start with `deterrent: "sound"`; only use water as last resort.
- Rate-limiter and night-only schedule are enabled by default.
