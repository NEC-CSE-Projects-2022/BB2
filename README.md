# BB2 – YOLO-HF: A Compact System for Fire Detection and Alerting

## Team Info
- 22471A0592 — **Yaswanth Gunda** ( [LinkedIn](https://www.linkedin.com/in/yaswanthgunda0068/) )
_Work Done: Handled most of the project including dataset preparation, model development, training, real-time detection setup, alert system, and full system integration._

- 22471A0589 — **Ranjith Kumar Garikapati** ( [LinkedIn](https://www.linkedin.com/in/ranjith-kumar-704864276/) )
_Work Done: Helped with dataset management, supported training and testing, and assisted in checking the system performance._

- 22471A05A8 — **Bala Muneendra Chilaka** ( [LinkedIn](https://www.linkedin.com/in/chilaka31/) )
_Work Done: Assisted in setting up the environment, configuring YOLOv5, running validations, and integrating the trained model._

- 22471A0576 — **Tarun Bellamkonda** ( [LinkedIn](https://www.linkedin.com/in/tarun-bellamkonda-2383aa31b/) )
_Work Done: Supported project setup, added required files, helped run the system, and assisted during final testing._

---

## Abstract
Fire incidents demand rapid, reliable detection. Existing vision-based methods suffer high false alarms, poor generalization, and high computational costs. YOLO-HF, a compact YOLOv5s variant, integrates four lightweight modules for efficient fire and smoke detection in limited-resource settings. The system’s real-time alert pipeline enables swift response.On 6,500 annotated images, YOLO-HF achieves mAP@0.5 of 0.958, outperforming baselines and reducing false alarms through threshold tuning. YOLO-HF’s novelty is its tailored module combination for fire/smoke cues and deployment-ready alerting, balancing accuracy and speed for practical use.

---

## Paper Reference (Inspiration)
👉 **YOLO-HF: Early Detection of Home Fires Using YOLO
  – Bo Peng And Tae-kook Kim
 ([Paper Link](https://ieeexplore.ieee.org/document/10985749))**

---

## Our Improvement Over Existing Paper
* Trained the model on a carefully prepared dataset with strong validation and testing to improve reliability in real-world situations.
* Converted the research model into a complete working system capable of detecting fire in real time.
* Added an instant alert mechanism that automatically sends an email with a captured image and places a call to the owner.
* Built an end-to-end application with backend and frontend support for continuous monitoring.
* Optimized the deployment so the model can run smoothly on a local system without requiring high-end infrastructure.
* Focused on practical usability by turning a research-based model into a ready-to-use safety solution.


---

## About the Project
**What the project does:**
This project detects fire and smoke at an early stage using a deep learning model based on YOLOv5 with custom modules. It monitors live camera footage and identifies possible fire hazards in real time.

**Why it is useful:**
Early fire detection helps prevent major damage, saves lives, and reduces property loss. The system provides immediate alerts so that quick action can be taken before the fire spreads.

**General project workflow (Input → Processing → Model → Output):**
Live video from a camera is captured as input → the frames are processed and analyzed → the trained YOLO-based model detects fire or smoke → if detected, the system sends an email with an image and triggers a call alert to notify the owner instantly.

---

## Dataset Used
👉 **[Dataset Name](Dataset URL)**

**Dataset Details:**
xxxxxxxxxx

---

## Dependencies Used
xxxxxxxxxx, xxxxxxxxxx, xxxxxxxxxx ...

---

## EDA & Preprocessing
xxxxxxxxxx

---

## Model Training Info
xxxxxxxxxx

---

## Model Testing / Evaluation
xxxxxxxxxx

---

## Results
xxxxxxxxxx

---

## Limitations & Future Work
xxxxxxxxxx

---

## Deployment Info
xxxxxxxxxx

---
