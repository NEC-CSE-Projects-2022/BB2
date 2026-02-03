🔥 Real-Time Fire & Smoke Detection System (YOLOv5 + Flask + Twilio + Email)

This project detects fire in real-time using a camera feed.  
If fire is detected consistently, it will:

- Trigger an Email Alert with the detected frame.
- Trigger a Phone Call Alert using Twilio
- Stream the live processed video through a Flask Web Server (`/video` route).

📁 Project Folder Structure

Your project folder must look like this:

project-folder/
│
├── web_server.py 
├── firesmoke_model_cleaned.pt
├── requirements.txt
├── README.md
├── index.html 
└── yolov5/ 

⚠️ Important:
The yolov5 folder must be in the same directory as web_server.py, and must include `models/` and `utils/`.

🔧 Installation (Windows 10/11)

Open CMD inside your project folder and run:

pip install flask opencv-python torch torchvision torchaudio numpy twilio
If you have GPU + CUDA, install PyTorch from official site:
https://pytorch.org/get-started/locally/

📨 Email Setup (Gmail)
Go to:
https://myaccount.google.com/security

Enable:
✅ 2-Step Verification
✅ App Passwords → Generate → Copy password

Replace these in the code:
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "yourGeneratedAppPassword"
TO_EMAIL = "receiver_email@gmail.com"

📞 Twilio Setup
Create account at https://www.twilio.com/

Get:
account_sid
auth_token
twilio_from (Your Twilio Number)
twilio_to (Phone number to call)
Replace in code.

🎥 Run the Application
In CMD (inside project folder):
python web_server.py 
If everything is correct, the server starts at:

http://localhost:5000/video     → Live video stream
http://localhost:5000/status    → JSON status
http://localhost:5000/health    → Backend health check

🧪 Fire Detection Logic (Important)
Parameter	Meaning
FIRE_PERSIST_FRAMES = 8	Fire must appear for 8 frames continuously
ALERT_COOLDOWN_SEC = 10	Time gap between alerts
FIRE_CLASS_ID = 0	Class index for fire in your model

✅ If Camera Not Opening / Lag Fix
Change:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
Try replacing 0 with 1 or 2.

✅ Stopping the App
Press:
CTRL + C
Close terminal. Done.

💡 Notes
Keep lighting decent for better detection.
False positives? Reduce CONFIDENCE_THRESHOLD like 0.50 → 0.65.
For live CCTV/IP camera feed use stream URL instead of 0.

❤️ Credits
Made by Team BB2 ( Gunda Yaswanth, Garikapati Ranjith Kumar, Chilaka Bala Muneendra, Bellamkonda Tarun. )
YOLOv5 by Ultralytics