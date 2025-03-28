from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from collections import Counter
import numpy as np
from ultralytics import YOLO
import tempfile

app = Flask(__name__)
CORS(app)

# Use temporary directories for Vercel
UPLOAD_FOLDER = tempfile.gettempdir()
PROCESSED_IMAGES_FOLDER = tempfile.gettempdir()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_IMAGES_FOLDER'] = PROCESSED_IMAGES_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load your YOLOv8 model
MODEL_PATH = './best.pt'  # Replace with the path to your best.pt file
model = YOLO(MODEL_PATH)

def process_file(file_path):
    """
    Process the uploaded file using the YOLOv8 model and return the result.
    """
    print(f"Processing file: {file_path}")
    
    # Perform inference using the YOLOv8 model
    results = model(file_path)  # This returns a list of Results objects
    
    # Extract information from the results
    result = results[0]  # Assuming only one image was processed
    boxes = result.boxes  # Bounding boxes
    class_ids = boxes.cls.cpu().numpy()  # Class IDs
    probabilities = boxes.conf.cpu().numpy()  # Probabilities (same as confidence scores)
    class_names = [result.names[int(cls_id)] for cls_id in class_ids]  # Class names

    # Check if any detection meets the probability threshold (0.2)
    valid_detections = [prob >= 0.2 for prob in probabilities]
    if any(valid_detections):  # If at least one detection meets the threshold
        most_common_class = Counter(class_names).most_common(1)[0][0]
        max_probability = round(np.max(probabilities) * 100, 2)  # Maximum probability as percentage
        # Determine risk level based on probability
        if max_probability > 30.0:  # Convert percentage back to decimal for comparison
            risk_level = "RISK"
        else:
            risk_level = "Low"
    else:
        most_common_class = "No tumor detected"
        max_probability = 0.0
        risk_level = "Low"

    # Map the predicted class to a label
    tumor_type = most_common_class

    # Save the processed image with bounding boxes
    processed_image_name = os.path.basename(file_path)
    processed_image_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], processed_image_name)
    result.save(processed_image_path)  # Save the processed image with bounding boxes
    print(f"Processed image saved at: {processed_image_path}")  # Debugging log

    # Return the result
    result = {
        "tumor_type": tumor_type,
        "risk_level": risk_level,
        "probability": max_probability,  # Use maximum probability
        "processed_image_path": processed_image_name  # Return only the filename
    }
    return result

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle multiple file uploads and process them to provide a single result."""
    if len(request.files) == 0:
        return jsonify({"error": "No files part"}), 400

    tumor_types = []
    risk_levels = []
    probabilities = []  # Store individual max probabilities
    processed_images = []

    for key, file in request.files.items():
        # Check if a file was selected
        if file.filename == '':
            return jsonify({"error": "One of the selected files is empty"}), 400
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"error": f"Unsupported file format for {file.filename}. Allowed formats: jpg, jpeg, png"}), 400
        # Save the file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved at: {file_path}")
        try:
            # Process the file with the YOLOv8 model
            result = process_file(file_path)
            tumor_types.append(result["tumor_type"])
            risk_levels.append(result["risk_level"])
            probabilities.append(result["probability"])  # Append max probability
            processed_images.append(result["processed_image_path"])  # Append processed image path
            print(f"Processed image saved at: {result['processed_image_path']}")  # Debugging log
        except Exception as e:
            print(f"Error processing file: {e}")  # Log the error
            return jsonify({"error": f"Failed to process the file {file.filename}."}), 500

    # Aggregate results
    final_tumor_type = Counter(tumor_types).most_common(1)[0][0]  # Most common tumor type
    final_risk_level = Counter(risk_levels).most_common(1)[0][0]  # Most common risk level
    max_probability = max(probabilities)  # Use the maximum probability across all files

    # Return a single aggregated result
    final_result = {
        "tumor_type": final_tumor_type,
        "risk_level": final_risk_level,
        "probability": max_probability,  # Return the maximum probability
        "processed_images": processed_images  # Ensure this is a list
    }
    print(f"Final result: {final_result}")  # Debugging log
    return jsonify(final_result)

@app.route('/api/processed_images/<filename>', methods=['GET'])
def get_processed_image(filename):
    """Serve processed images."""
    return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)

# For local development
if __name__ == '__main__':
    app.run(debug=True)