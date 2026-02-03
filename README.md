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
👉 **[Home Fire Detection Dataset](https://drive.google.com/drive/folders/13dkctv-aNRD-d4EIRivHUMr0S1B2Y_W2)**

**Dataset Details:**
This project uses a large-scale fire detection dataset hosted on Google Drive due to its size. The dataset is organized into three main subsets: Train Dataset for model training, Validation Dataset for hyperparameter tuning and performance improvement, and Test Dataset for final evaluation.  

The dataset is based on the original **Home Fire Dataset** created by the authors of the research paper that inspired this project and can be accessed here: https://github.com/PengBo0/Home-fire-dataset.

---


## Dependencies Used
Python, Google Colab, YOLOv5, PyTorch, OpenCV (cv2), NumPy, Pandas, Matplotlib, Seaborn, Glob, OS, Flask, Torch, SMTP (smtplib), EmailMessage, Twilio Client, Threading, DetectMultiBackend, Non-Max Suppression, Scale Coords.

---

## EDA & Preprocessing
* Mounted Google Drive in Colab and imported required libraries for data handling and visualization.
* Reviewed the dataset by counting images and labels across train, validation, and test folders.
* Checked for missing label files and ensured every image had a corresponding annotation.
* Converted YOLO label files into a structured format to better understand the data.
* Identified the classes (fire, smoke) and analyzed their distribution.
* Examined bounding box sizes, positions, and counts to understand object patterns.
* Verified image resolutions and collected shape details to maintain consistency.
* Detected and removed corrupted or unreadable images.
* Validated annotation formats and value ranges to prevent training errors.
* Converted all PNG images to JPG for uniformity.
* Completed data cleaning and verification to ensure the dataset was ready for accurate model training.

---

## Model Training Info
The model was developed using YOLOv5s enhanced with custom modules (PBCA, SPD, CBPS, RepNCSPELAN4) to improve early fire and smoke detection. Training was performed on Google Colab with GPU support using a dataset of 3,900 images divided into training, validation, and testing sets.

Before training, the dataset was carefully prepared by checking missing labels, validating annotations, removing corrupted images, standardizing image formats, and analyzing bounding box distributions to ensure data quality. After configuring the custom architecture (`yolov5s_custom.yaml`), the model was trained using the firesmoke dataset configuration.

Post-training, the model was validated and tested to measure performance using metrics such as Precision, Recall, and mAP. Evaluation plots like the confusion matrix and PR curves were reviewed to confirm detection accuracy and generalization. The best-performing weights were then exported and cleaned, resulting in a finalized `.pt` model ready for deployment in a real-time fire detection system with alert capabilities.

---

## Model Testing / Evaluation
The model was tested after training to ensure it performs accurately in real-world conditions. Validation was conducted to measure key metrics such as Precision, Recall, and mAP, and evaluation plots like the confusion matrix and PR curve were generated to analyze detection quality. The model was further tested on a separate test dataset to verify its ability to generalize to new images. After confirming stable performance, the best model weights were selected and exported as a cleaned `.pt` file. Finally, the system was tested using live camera input to confirm reliable real-time fire detection and proper alert triggering through email and call notifications.

---

## Results
The YOLO-HF model was successfully trained on 3,900 images and evaluated using standard metrics such as Precision, Recall, F1-score, and mAP. The results showed strong detection accuracy with fewer false alarms and missed detections, proving the model’s reliability for early fire and smoke identification.

Compared to the baseline YOLOv5s and other recent detection models, YOLO-HF delivered better overall performance while maintaining a lightweight design suitable for real-time use. Threshold tuning further reduced false positives without affecting detection sensitivity, making the system more stable in practical environments.

Validation plots such as the confusion matrix and Precision–Recall curve confirmed that the model can accurately localize fire and smoke across different conditions. Testing on unseen data demonstrated good generalization capability.

The trained model was then deployed into a real-time monitoring system that captures live video, detects fire instantly, and sends alerts through email with an attached image along with an automated call. The final system operates smoothly on a local setup, confirming its readiness for real-world safety applications.

---

## Limitations & Future Work
**Limitations:**

* The model was trained on a limited dataset, so performance may vary in highly different environments.
* Detection accuracy can reduce in low-light conditions, dense smoke, or when reflections are present.
* The system currently uses only RGB camera input, which may affect robustness compared to thermal or multi-sensor solutions.
* Testing was mainly focused on controlled scenarios, so large-scale real-world validation is still needed.

**Future Work:**

* Train and evaluate the model on larger and more diverse datasets to improve reliability.
* Integrate additional sensors such as thermal cameras or IoT devices for better detection in poor visibility.
* Optimize the model using compression techniques so it can run efficiently on edge devices.
* Expand the system for wider applications such as industrial safety and wildfire monitoring.
* Further improve the model to detect very small flames faster and reduce false alerts.

---

## Deployment Info
*
The trained YOLO-HF model was saved as a `.pt` file and deployed on a local system for real-time fire and smoke detection using a live camera. When fire is detected, the system automatically sends an email with the captured image and makes a call to alert the owner, enabling quick response and improving safety.*
---
