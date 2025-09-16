# CatGuard 🐱🔕

A humane, DIY cat-scratch deterrent system that combines **computer vision**, **audio analysis**, and **control logic** to keep curious cats from shredding your door at night.

- **Detect**: Cat presence at the door via a floor-level region of interest (ROI) in the camera feed  
- **Listen**: Scratch-like sounds using microphone spectral features  
- **Deter**: Play a deterrent sound (doorbell) or pulse a small water sprayer  
- **Control**: Cooldowns, night-only scheduling, and rate-limiting for safe/humane use

---

## 🚀 Quick Start

### Requirements
- Python 3.10+
- Dependencies in `requirements.txt`:
  ```bash
  pip install -r requirements.txt
