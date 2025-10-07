import cv2
import os
import json
from datetime import datetime

def save_clip(pre_event, post_event, event_type, fps=30, start_time=None, end_time=None):
    from datetime import datetime
    import os
    import json

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"clips/{event_type}_{timestamp}.avi"

    if not os.path.exists("clips"):
        os.makedirs("clips")

    height, width = pre_event[0].shape[:2]
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

    for frame in pre_event + post_event:
        out.write(frame)
    out.release()

    metadata = {
        "event_type": event_type,
        "timestamp": timestamp,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else None,
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None,
        "filename": filename,
        "gps": {"lat": 28.4595, "lon": 77.0266}
    }

    with open("metadata.json", "a") as f:
        f.write(json.dumps(metadata) + "\n")

    print(f"✅ Saved clip: {filename}")