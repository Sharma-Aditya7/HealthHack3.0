# Tumor Detection Backend

This is the backend service for the Tumor Detection application, built with Flask and deployed on Render.

## Features

- Image upload and processing using YOLO model
- Cloud storage using Cloudinary
- RESTful API endpoints
- CORS enabled for frontend integration

## Prerequisites

- Python 3.9 or higher
- Cloudinary account
- Render account

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python Backend.py
```

## Deployment to Render

1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Create a new Web Service
4. Configure the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn Backend:app`
   - Environment Variables:
     - `CLOUDINARY_CLOUD_NAME`
     - `CLOUDINARY_API_KEY`
     - `CLOUDINARY_API_SECRET`

## API Endpoints

- `POST /upload`: Upload and process an image
- `GET /health`: Health check endpoint

## Important Notes

- Make sure to upload your YOLO model file (`best.pt`) to Cloudinary in the `models` folder
- The application uses temporary storage for processing images
- All processed images are stored in Cloudinary 