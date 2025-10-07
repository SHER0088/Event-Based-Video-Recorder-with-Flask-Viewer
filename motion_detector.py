import cv2

def detect_motion(prev_frame, curr_frame, threshold=25):
    prev_small = cv2.resize(prev_frame, (320, 240))
    curr_small = cv2.resize(curr_frame, (320, 240))

    diff = cv2.absdiff(prev_small, curr_small)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    motion_score = cv2.countNonZero(thresh)
    return motion_score > 3000