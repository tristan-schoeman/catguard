
import cv2

class ROIMotionDetector:
    def __init__(self, roi_floor_px=160, min_contour_area=1000):
        self.roi_floor_px = roi_floor_px
        self.min_contour_area = min_contour_area
        self.bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=32, detectShadows=True)

    def detect(self, frame):
        h, w = frame.shape[:2]
        roi = frame[h - self.roi_floor_px:h, 0:w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        mask = self.bg.apply(gray)
        mask = cv2.medianBlur(mask, 5)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_contour_area:
                continue
            x, y, cw, ch = cv2.boundingRect(c)
            detections.append((x, y + (h - self.roi_floor_px), cw, ch, area))
        return detections, mask
