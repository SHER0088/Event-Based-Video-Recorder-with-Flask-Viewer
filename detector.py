import random
import time

def simulate_event():
    time.sleep(random.randint(10, 30))  # Simulate delay
    event_type = random.choice(["drowsiness", "phone_usage", "lane_departure"])
    print(f"[EVENT DETECTED] Type: {event_type}")
    return event_type