from flask import Flask, Response, jsonify, make_response
import cv2, torch, numpy as np, sys, time
from threading import Thread
from twilio.rest import Client
from email.message import EmailMessage
import smtplib

# -----------------------------
# YOLOv5 imports
# -----------------------------
sys.path.append('./yolov5')
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_coords

# -----------------------------
# Model setup
# -----------------------------
torch.set_grad_enabled(False)
device = torch.device('cpu')
model = DetectMultiBackend('firesmoke_model_cleaned.pt', device=device)
stride, names = model.stride, model.names
model.eval()

# -----------------------------
# Email / Twilio
# -----------------------------
EMAIL_ADDRESS = "*********@gmail.com"
EMAIL_PASSWORD = "***********"
TO_EMAIL = "*********@gmail.com"

account_sid = "**********"
auth_token = "**********"
twilio_from = "**********"
twilio_to = "**********"
flow_sid = "**********"

def send_email_alert(image_path):
    try:
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        msg = EmailMessage()
        msg['Subject'] = "🔥 FIRE DETECTED — Immediate Attention Required!"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL

        msg.set_content(f"""
🔥 FIRE ALERT DETECTED!

🕒 Exact Time: {current_time}
📍 Location: Your monitoring system (set your site/building address if fixed)

⚠️ What to do NOW:
1) Confirm fire visually & stay calm.
2) Switch off main power if safe.
3) Evacuate everyone immediately.
4) Do NOT use elevators.
5) Keep exits clear and assist others.

📞 Helpline (India):
• Fire & Rescue: 101
• National Emergency: 112
• Ambulance: 108

📸 The detected frame is attached for reference.
""")

        with open(image_path, "rb") as f:
            msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename="fire.jpg")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent")
    except Exception as e:
        print("❌ Email Error:", e)

def trigger_twilio_call():
    try:
        client = Client(account_sid, auth_token)
        # Old Block
        # execution = client.studio.flows(flow_sid).executions.create(
        #     to=twilio_to,
        #     from_=twilio_from
        # )
        # New Block
        call = client.calls.create(
            to=twilio_to,
            from_=twilio_from,
            twiml="""
        <Response>
        <Say voice="alice">Emergency Alert. Fire detected at your location. Please take action immediately.</Say>
        </Response>
        """
        )
        print("✅ Twilio Call Triggered:", call.sid)
    except Exception as e:
        print("❌ Twilio Error:", e)

def send_alerts(color_frame):
    cv2.imwrite("output.jpg", color_frame)
    Thread(target=send_email_alert, args=("output.jpg",), daemon=True).start()
    Thread(target=trigger_twilio_call, daemon=True).start()

# -----------------------------
# Video capture (low-lag)
# -----------------------------
def open_camera():
    cap_ = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap_.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap_.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap_.set(cv2.CAP_PROP_FPS,          30)
    cap_.set(cv2.CAP_PROP_BUFFERSIZE,   1)  # keep buffer tiny if supported
    return cap_

cap = open_camera()

# -----------------------------
# Detection / throttling params
# -----------------------------
CONFIDENCE_THRESHOLD = 0.45
IOU_THRESHOLD        = 0.45
FIRE_CLASS_ID        = 0            # your model's 'fire' index
FIRE_PERSIST_FRAMES  = 8            # must see fire this many frames in a row
ALERT_COOLDOWN_SEC   = 10
STREAM_FPS_TARGET    = 15           # throttle stream to reduce lag
JPEG_QUALITY         = 70

# -----------------------------
# State (shared)
# -----------------------------
fire_detected = False
fire_frames = 0
fire_detection_count = 0
last_alert_time = 0.0
alert_triggered = False
backend_online = True

SECS_PER_FRAME = 1.0 / STREAM_FPS_TARGET

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

def annotate_and_detect(color_frame):
    """
    - Flip horizontally (so text is readable).
    - Run detection on a grayscale version (3-channel)
    - Draw boxes/label on the COLOR frame.
    """
    global fire_detected, fire_frames, alert_triggered, last_alert_time, fire_detection_count

    # Flip for user-facing stream (and alert snapshot)
    color_frame = cv2.flip(color_frame, 1)

    # ---- Inference on grayscale (as requested) ----
    resized = cv2.resize(color_frame, (640, 640))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    bw_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)  # model expects 3 channels
    img_tensor = torch.from_numpy(bw_3ch).to(device).permute(2, 0, 1).float().div(255.0).unsqueeze(0)

    with torch.no_grad():
        pred = model(img_tensor)
        pred = non_max_suppression(pred, conf_thres=CONFIDENCE_THRESHOLD, iou_thres=IOU_THRESHOLD)

    # ---- Parse detections & draw on color_frame ----
    current_fire = False
    det = pred[0]
    if det is not None and len(det):
        det[:, :4] = scale_coords(img_tensor.shape[2:], det[:, :4], color_frame.shape).round()
        for *xyxy, conf, cls in det:
            cls_id = int(cls.item())
            if cls_id == FIRE_CLASS_ID:
                current_fire = True
                x1, y1, x2, y2 = [int(a.item()) for a in xyxy]
                label = f"FIRE {conf:.2f}"

                # Red bbox + solid label bg
                cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(color_frame, (x1, y1 - th - 10), (x1 + tw + 8, y1), (0, 0, 255), -1)
                cv2.putText(color_frame, label, (x1 + 4, y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # ---- Update counters ----
    if current_fire:
        fire_frames += 1
    else:
        fire_frames = 0
        alert_triggered = False

    fire_detected = current_fire

    # ---- Trigger alerts with cooldown ----
    if current_fire and fire_frames >= FIRE_PERSIST_FRAMES and not alert_triggered:
        now = time.time()
        if now - last_alert_time >= ALERT_COOLDOWN_SEC:
            fire_detection_count += 1
            last_alert_time = now
            alert_triggered = True
            Thread(target=send_alerts, args=(color_frame.copy(),), daemon=True).start()

    return color_frame

def mjpeg_generator():
    """
    MJPEG stream generator with FPS throttling, low-lag behavior,
    and auto-reconnect camera if it fails.
    """
    global backend_online, cap
    last_sent = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            backend_online = False
            # try to reopen camera
            try:
                cap.release()
            except Exception:
                pass
            time.sleep(1.0)
            cap = open_camera()
            continue

        backend_online = True

        # throttle to target FPS
        now = time.time()
        if now - last_sent < (1.0 / STREAM_FPS_TARGET):
            continue

        # annotate & detect
        annotated = annotate_and_detect(frame)

        # encode JPEG (smaller size -> less lag)
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        ok2, buffer = cv2.imencode('.jpg', annotated, encode_params)
        if not ok2:
            continue

        frame_bytes = buffer.tobytes()
        last_sent = now

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')

@app.after_request
def add_headers(resp):
    # allow opening index.html from file:// origin
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp

@app.route('/video')
def video():
    return Response(mjpeg_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    # seen seconds = consecutive frames / stream fps (approx)
    return jsonify({
        "online": backend_online,
        "fire": bool(fire_detected),
        "seen_frames": int(fire_frames),
        "seen_seconds": round(fire_frames * SECS_PER_FRAME, 1),
        "alerts": int(fire_detection_count)
    })

@app.route('/health')
def health():
    code = 200 if backend_online else 503
    return make_response(("OK" if backend_online else "OFFLINE"), code)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    finally:
        try:
            cap.release()
        except Exception:
            pass
