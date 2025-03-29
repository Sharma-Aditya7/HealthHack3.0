from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from collections import Counter
import numpy as np
from ultralytics import YOLO
import tempfile
import traceback

app = Flask(__name__)
CORS(app)

# Use local directories for file storage
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PROCESSED_IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processed_images')

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_IMAGES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_IMAGES_FOLDER'] = PROCESSED_IMAGES_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load your YOLOv8 model
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'best.pt')
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

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
        max_probability = float(round(np.max(probabilities) * 100, 2))  # Convert to Python float
        # Determine risk level based on probability
        if max_probability >= 70.0:
            risk_level = "High"
        elif max_probability >= 40.0:
            risk_level = "Medium"
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

    # Return the result with Python native types
    result = {
        "tumor_type": str(tumor_type),  # Ensure string type
        "risk_level": str(risk_level),  # Ensure string type
        "probability": float(max_probability),  # Convert to Python float
        "processed_image_path": processed_image_name  # Return just the filename
    }
    return result

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle multiple file uploads and process them to provide a single result."""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    if len(request.files) == 0:
        return jsonify({"error": "No files part"}), 400

    tumor_types = []
    risk_levels = []
    probabilities = []
    processed_images = []

    try:
        for key, file in request.files.items():
            if file.filename == '':
                return jsonify({"error": "One of the selected files is empty"}), 400
            
            if not allowed_file(file.filename):
                return jsonify({"error": f"Unsupported file format for {file.filename}. Allowed formats: jpg, jpeg, png"}), 400
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(f"File saved at: {file_path}")
            
            try:
                result = process_file(file_path)
                tumor_types.append(result["tumor_type"])
                risk_levels.append(result["risk_level"])
                probabilities.append(float(result["probability"]))  # Ensure float type
                processed_images.append(result["processed_image_path"])  # Store just the filename
                print(f"Processed image saved at: {result['processed_image_path']}")
            except Exception as e:
                print(f"Error processing file: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                return jsonify({"error": f"Failed to process the file {file.filename}: {str(e)}"}), 500

        # Aggregate results
        final_tumor_type = Counter(tumor_types).most_common(1)[0][0]
        final_risk_level = Counter(risk_levels).most_common(1)[0][0]
        max_probability = float(max(probabilities))  # Ensure float type

        final_result = {
            "tumor_type": str(final_tumor_type),  # Ensure string type
            "risk_level": str(final_risk_level),  # Ensure string type
            "probability": float(max_probability),  # Ensure float type
            "processed_images": processed_images  # List of filenames
        }
        print(f"Final result: {final_result}")
        return jsonify(final_result)
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/processed_images/<filename>', methods=['GET'])
def get_processed_image(filename):
    """Serve processed images."""
    return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)

# For local development
if __name__ == '__main__':
    app.run(debug=True)