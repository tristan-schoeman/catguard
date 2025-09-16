
import cv2, time, yaml, datetime as dt, os
from src.vision.motion_detector import ROIMotionDetector
from src.audio.scratch_detector import ScratchDetector, AudioConfig
from src.control.sound_player import SoundPlayer
from src.control.water_turret import WaterTurret
from src.utils.state import RateLimiter

def within_night_window(night_only, start, end):
    if not night_only:
        return True
    now = dt.datetime.now().time()
    s = dt.datetime.strptime(start, "%H:%M").time()
    e = dt.datetime.strptime(end, "%H:%M").time()
    if s < e:
        return s <= now <= e
    else:
        return now >= s or now <= e

def load_cfg(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    cfg = load_cfg()
    cap = cv2.VideoCapture(cfg.get("camera_index", 0))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.get("frame_width", 640))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.get("frame_height", 480))

    md = ROIMotionDetector(cfg["roi_floor_px"], cfg["min_contour_area"])

    sd = None
    audio_iter = None
    if cfg.get("use_audio", True):
        sd = ScratchDetector(AudioConfig(
            sample_rate=cfg["audio_sample_rate"],
            block_s=cfg["audio_block_s"],
            highband_hz=cfg["scratch_highband_hz"],
            energy_ratio=cfg["scratch_energy_ratio"],
            min_blocks=cfg["scratch_min_blocks"],
        ))
        audio_iter = sd.stream_generator()

    deterrent = cfg.get("deterrent","sound")
    sound = SoundPlayer(cfg["sound_file"])
    turret = WaterTurret(simulate=True)
    limiter = RateLimiter(cfg["cooldown_s"], cfg["max_triggers_per_hour"])

    print("[CatGuard] Running. Press 'q' to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("[CatGuard] Camera read failed.")
            break

        dets, mask = md.detect(frame)
        presence = len(dets) > 0

        scratching = False
        ratio = 0.0
        if audio_iter:
            try:
                block = next(audio_iter)
                scratching, ratio = sd.is_scratching(block)
            except Exception as e:
                print(f"[Audio] {e}")

        # UI overlays
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, h - cfg["roi_floor_px"]), (w, h), (0, 255, 0), 2)
        for (x, y, cw, ch, area) in dets:
            cv2.rectangle(frame, (x, y), (x+cw, y+ch), (255, 0, 0), 2)
        cv2.putText(frame, f"Presence: {presence} Scratch: {scratching} ({ratio:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.imshow("CatGuard", frame)
        cv2.imshow("ROI Mask", mask)

        if presence and scratching and within_night_window(cfg["night_only"], cfg["night_start"], cfg["night_end"]):
            if limiter.allow():
                stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                print(f"[Deterrent] Trigger @ {stamp}")
                if deterrent == "sound":
                    sound.play()
                else:
                    turret.pulse(ms=300)
            else:
                print("[Deterrent] Rate-limited.")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    turret.cleanup()

if __name__ == "__main__":
    main()
