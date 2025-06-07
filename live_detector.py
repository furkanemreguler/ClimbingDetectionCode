import cv2, torch, time
import numpy as np
from collections import deque, defaultdict
from queue import Queue
from threading import Thread
from ultralytics import YOLO
from datetime import datetime, timedelta
import climbing_client
# from alert_utils import init_db, send_email_alert, store_event_to_db

# ─ CONFIG ─
VIDEO_PATH = 0  # or a path to a video file
FPS = 15.0
QUEUE_SIZE = 1
WINDOW = 15
BENT_THRESHOLD = 5
KNEE_MIN, KNEE_MAX = 45, 130
CONF_THRESH = 0.30
MODEL_PATH = "yolov8m-pose.pt"
MAX_FRAME_ID = 1_000_000

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 YOLO model loading on ➜ {device}")
model = YOLO(MODEL_PATH).to(device)

# ─ SHARED STATE ─
frame_queue: Queue = Queue(maxsize=QUEUE_SIZE)
stop_flag: bool = False
window_buffers = defaultdict(lambda: deque(maxlen=WINDOW))
cooldowns = defaultdict(lambda: datetime.min)

# ─ FUNCTIONS ─
def calculate_angle(a, b, c):
    ab, cb = np.array(a) - np.array(b), np.array(c) - np.array(b)
    cosang = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
    cosang = np.clip(cosang, -1.0, 1.0)
    return np.degrees(np.arccos(cosang))

def producer():
    global stop_flag
    cap = cv2.VideoCapture(VIDEO_PATH, cv2.CAP_AVFOUNDATION) 
    if not cap.isOpened():
        print("❌ Could not open video or camera.")
        stop_flag = True
        cap.release()
        return

    print("🎥 Producer started.")
    frame_idx = 0
    frame_period = 1.0 / FPS
    next_frame_time = time.perf_counter()

    while not stop_flag:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx = (frame_idx + 1) % MAX_FRAME_ID
        frame_queue.put((frame_idx, frame, time.perf_counter()))

        next_frame_time += frame_period
        sleep_dur = next_frame_time - time.perf_counter()
        if sleep_dur > 0:
            time.sleep(sleep_dur)

    cap.release()
    print("🎥 Producer finished.")
    frame_queue.put(None)

def consumer():
    global stop_flag
    print("🧠 Consumer started.")
    while True:
        item = frame_queue.get()
        if item is None:
            break

        frame_idx, frame, t_capture = item
        t0 = time.perf_counter()
        results = model.track(frame, persist=True, conf=0.5, classes=[0], verbose=False)
        infer_time = time.perf_counter() - t0

        boxes, kpts = results[0].boxes, results[0].keypoints
        if boxes is not None and kpts is not None:
            for box, kp in zip(boxes, kpts):
                pid = int(box.id[0]) if box.id is not None else -1
                kparr = kp.data[0].cpu().numpy()
                window_buffers[pid].append((frame_idx, t_capture, kparr))

                buf = window_buffers[pid]
                if len(buf) == WINDOW:
                    bent_cnt = 0
                    for _, _, kps in buf:
                        lh, lk, la = kps[11], kps[13], kps[15]
                        rh, rk, ra = kps[12], kps[14], kps[16]

                        l_ok = all(p[2] > CONF_THRESH for p in [lh, lk, la])
                        r_ok = all(p[2] > CONF_THRESH for p in [rh, rk, ra])

                        left_angle = calculate_angle(lh[:2], lk[:2], la[:2]) if l_ok else None
                        right_angle = calculate_angle(rh[:2], rk[:2], ra[:2]) if r_ok else None

                        if (left_angle and KNEE_MIN <= left_angle <= KNEE_MAX) or \
                           (right_angle and KNEE_MIN <= right_angle <= KNEE_MAX):
                            bent_cnt += 1

                    now = datetime.now()
                    if bent_cnt >= BENT_THRESHOLD and now > cooldowns[pid]:
                        cooldowns[pid] = now + timedelta(seconds=10)

                        t_first = buf[0][1]
                        latency = time.perf_counter() - t_first
                        middle_index = len(buf) // 2
                        frame_id = buf[middle_index][0]

                        print(f"🚀 CLIMBING DETECTED | id={pid:<3} "
                              f"frame {frame_id:<5} "
                              f"| latency={latency*1000:6.1f} ms "
                              f"(infer {infer_time*1000:5.1f} ms)")

                        event = {
                            "id": pid,
                            "frame": frame_id,
                            "latency_ms": round(latency * 1000, 1),
                            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
                        }

                        climbing_client.send_climbing_alert(event)
                        # send_email_alert(event)
                        # store_event_to_db(event)

        frame_queue.task_done()

    print("🧠 Consumer finished.")
    stop_flag = True

# ─ MAIN ─
if __name__ == "__main__":
    # init_db()
    prod = Thread(target=producer, daemon=True)
    cons = Thread(target=consumer, daemon=True)
    prod.start(); cons.start()
    prod.join(); cons.join()
    print("✅ Live pipeline completed.")
