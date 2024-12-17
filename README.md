# Sign Language Detection

This repository provides a **Flask web application** that uses a **YOLOv5-small** model to detect six essential sign language gestures:

- **Hello**
- **Yes**
- **No**
- **I love you**
- **Please**
- **Thanks**

The model processes images uploaded via the web app and returns the prediction results.

---

## How It Works

1. The **YOLOv5-small** model is trained locally on images of six specific sign language gestures.
2. Once the model reaches the desired accuracy, the best-performing weights are pushed to an **S3 bucket** for storage.
3. Users upload an image through the Flask web interface, which is passed to the model for detection.
4. The model processes the input and predicts the relevant gesture, displaying the result on the web app.

---

## Requirements

### 1. Minimum Hardware Requirement
- **At least 8GB of VRAM** is required for training the YOLOv5 model.
- Insufficient VRAM will result in **memory errors** during the training process.

### 2. Clone YOLOv5 Repository
To ensure proper training and model operation, clone the official YOLOv5 repository into your local system:

```bash
# Clone YOLOv5 repository
git clone https://github.com/ultralytics/yolov5.git
```

---

## Training Your Own Dataset
If you want to train the model on your personalized sign language gestures, follow these steps:

### Step 1: Collect Images
Run the `image_collector.py` script to collect images using your webcam:

```bash
python image_collector.py
```

This will save webcam snapshots of your gestures into a designated directory.

### Step 2: Annotate Images
Manually annotate the collected images using tools like **LabelImg** or other annotation tools. Save the annotations in **YOLO format**.

### Step 3: Train the Model
Use the provided **Jupyter Notebook** to train the model on your annotated images. The steps are outlined clearly within the notebook.

1. Load the annotated dataset.
2. Configure the YOLOv5 training parameters.
3. Train the model and evaluate its performance.

### Step 4: Push the Best Model (Optional)
Once the training is complete, you can push the best-performing weights to an **S3 bucket** for storage.

---

## Running the Flask Web Application

To run the web app for sign language detection:

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:

   ```bash
   python app.py
   ```

3. Open a browser and navigate to `http://127.0.0.1:5000/` to use the web interface.

4. Upload an image to see the prediction results.

---

## Summary
- **Model**: YOLOv5-small
- **Purpose**: Detect six essential sign language gestures.
- **Training**: Clone YOLOv5, ensure 8GB VRAM, and follow notebook steps.
- **Web App**: Flask-based interface for uploading images and viewing results.
- **Customization**: Collect and train your own images using `image_collector.py` and manual annotation.

---

Happy detecting! 👋

