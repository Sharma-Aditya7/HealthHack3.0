from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ultralytics import YOLO
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import tempfile
import shutil
import requests
import logging
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

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

@app.route('/upload', methods=['POST'])
def upload_file():
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)