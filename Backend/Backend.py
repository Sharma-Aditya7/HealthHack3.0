from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from collections import Counter
import numpy as np
from ultralytics import YOLO
import tempfile
import traceback
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import requests
import logging
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure CORS to allow requests from Netlify domain
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://safebrains.netlify.app",
            "http://localhost:3000",
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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

# Create a temporary directory for processing
TEMP_DIR = tempfile.mkdtemp()

# Global model variable
model = None

def load_model():
    try:
        # Configure Cloudinary
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        api_key = os.getenv('CLOUDINARY_API_KEY')
        api_secret = os.getenv('CLOUDINARY_API_SECRET')
        
        if not all([cloud_name, api_key, api_secret]):
            raise ValueError("Missing Cloudinary credentials in environment variables")
            
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        logger.info("Cloudinary configured successfully")
        
        # Use the direct URL for the model file
        model_url = "https://res.cloudinary.com/dhtta5hni/raw/upload/v1743272767/best_ohckbc.pt"
        model_path = os.path.join(TEMP_DIR, 'best.pt')
        
        logger.info(f"Downloading model from: {model_url}")
        
        # Download the model file with timeout and retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(model_url, timeout=30)
                response.raise_for_status()
                with open(model_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Model downloaded successfully to {model_path}")
                break
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
        
        # Load the model with the new security requirements
        logger.info("Loading YOLO model...")
        
        # Load the model directly with YOLO
        model = YOLO(model_path)
        
        # Verify model loaded successfully
        if model is None:
            raise ValueError("Failed to load YOLO model")
            
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

@app.before_request
def before_request():
    # Log the request details
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Origin: {request.headers.get('Origin')}")

@app.after_request
def after_request(response):
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.before_first_request
def initialize_model():
    global model
    try:
        model = load_model()
        logger.info("Model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        # Don't raise the exception here, let the application start
        # The upload endpoint will handle the case when model is None

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

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        if model is None:
            return jsonify({
                'error': 'Model not initialized. Please check the server logs for details.',
                'details': 'The YOLO model could not be loaded. This might be because the model file could not be downloaded.'
            }), 503
            
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}_{file.filename}"
            
            # Upload original image to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file,
                public_id=f"original_images/{unique_filename}",
                resource_type="auto"
            )
            original_url = upload_result['secure_url']
            
            # Process the image with YOLO
            results = model.predict(original_url)
            
            # Save the processed image temporarily
            processed_filename = f"processed_{unique_filename}"
            processed_path = os.path.join(TEMP_DIR, processed_filename)
            results[0].save(processed_path)
            
            # Upload processed image to Cloudinary
            processed_upload = cloudinary.uploader.upload(
                processed_path,
                public_id=f"processed_images/{processed_filename}",
                resource_type="auto"
            )
            processed_url = processed_upload['secure_url']
            
            # Clean up temporary files
            os.remove(processed_path)
            
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'original_image': original_url,
                'processed_image': processed_url
            })
            
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'cloudinary_configured': bool(os.getenv('CLOUDINARY_CLOUD_NAME')),
        'model_exists': bool(model)
    })

@app.route('/api/processed_images/<filename>', methods=['GET'])
def get_processed_image(filename):
    """Serve processed images."""
    return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)