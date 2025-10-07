import cv2
import time
import threading
from datetime import datetime
from buffer import VideoBuffer
from recorder import save_clip
from motion_detector import detect_motion

# Configuration
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30
PRE_EVENT_DURATION = 15
POST_EVENT_DURATION = 15

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

# Initialize buffer
buffer = VideoBuffer(maxlength=FPS * PRE_EVENT_DURATION)

# Read first frame
ret, prev_frame = cap.read()
if not ret:
    print("❌ Failed to read initial frame")
    cap.release()
    exit()

print("✅ Webcam started. Press 'q' to quit.")
last_event_time = 0
active_event = {"start": None, "end": None}

def handle_motion_event(pre_event, cap, active_event):
    active_event["start"] = datetime.now()
    post_event = []
    for _ in range(FPS * POST_EVENT_DURATION):
        ret, post_frame = cap.read()
        if not ret:
            break
        post_event.append(post_frame)
    active_event["end"] = datetime.now()
    save_clip(pre_event, post_event, "motion_event", fps=FPS,
              start_time=active_event["start"], end_time=active_event["end"])
    active_event["start"] = None
    active_event["end"] = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    buffer.add_frame(frame)

# Overlay timestamps if active
    if active_event["start"]:
        cv2.putText(frame, f"Start: {active_event['start'].strftime('%H:%M:%S')}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if active_event["end"]:
        cv2.putText(frame, f"End: {active_event['end'].strftime('%H:%M:%S')}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Live Feed", frame)

    current_time = time.time()
    if detect_motion(prev_frame, frame) and current_time - last_event_time > 5:
        last_event_time = current_time
        print("[EVENT DETECTED] Motion detected")
        pre_event = buffer.get_buffer()
        threading.Thread(target=handle_motion_event,
                         args=(pre_event.copy(), cap, active_event)).start()

    prev_frame = frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()