
try:
    import RPi.GPIO as GPIO
    ON_PI = True
except Exception:
    ON_PI = False

class WaterTurret:
    def __init__(self, pump_pin=18, simulate=True):
        self.pump_pin = pump_pin
        self.simulate = simulate or (not ON_PI)
        if not self.simulate:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pump_pin, GPIO.OUT, initial=GPIO.LOW)

    def pulse(self, ms=300):
        if self.simulate:
            print(f"[WaterTurret] SIM PULSE {ms} ms")
            return True
        try:
            GPIO.output(self.pump_pin, GPIO.HIGH)
            import time; time.sleep(ms / 1000.0)
            GPIO.output(self.pump_pin, GPIO.LOW)
            return True
        except Exception as e:
            print(f"[WaterTurret] Error: {e}")
            return False

    def cleanup(self):
        if not self.simulate:
            GPIO.cleanup()
