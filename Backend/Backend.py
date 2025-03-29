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

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

app = Flask(__name__)
CORS(app)

# Create a temporary directory for processing
TEMP_DIR = tempfile.mkdtemp()

# Load the model from Cloudinary
def load_model():
    try:
        # Download model from Cloudinary
        model_url = cloudinary.CloudinaryImage("models/best").build_url()
        model_path = os.path.join(TEMP_DIR, 'best.pt')
        
        # Download the model file
        import requests
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        
        return YOLO(model_path)
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

# Initialize the model
model = load_model()

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
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
        print(f"Error processing file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)