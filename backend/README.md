# VisionForge Backend API

FastAPI backend service for VisionForge image processing application.

## Features

- **Image Processing**: OpenCV-based image manipulation
- **Real-time Processing**: Process images with various controls
- **CORS Support**: Configured for frontend communication
- **Multiple Formats**: Support for various image formats
- **RESTful API**: Clean API endpoints for image processing

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Install Python dependencies:
```bash
npm run backend:install
# or
cd backend && pip install -r requirements.txt
```

2. Start the backend server:
```bash
npm run backend
# or
cd backend && python start.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Image Processing
- `POST /process-image` - Process uploaded image file
- `POST /process-image-base64` - Process base64 encoded image

## Supported Operations

### Color Operations
- Grayscale conversion
- Color space conversion (RGB, HSV, LAB, YCrCb)

### Transform Operations
- Rotation
- Translation
- Scaling with various interpolation methods
- Cropping

### Filter Operations
- Blur (Gaussian, Median, Bilateral, Box)
- Sharpening

### Edge Detection
- Canny edge detection
- Sobel edge detection

### Bitwise Operations
- NOT, AND, OR, XOR operations
- Mask-based operations

### Adaptive Thresholding
- Mean and Gaussian adaptive thresholding
- Configurable block size and C parameter

### Morphological Operations
- Kernel-based operations
- Configurable iterations

### Color Boost
- Saturation adjustment
- Hue shifting
- RGB channel gains
- Contrast and brightness

### Drawing Operations
- Rectangles, circles, lines, text
- Color picker support
- Configurable thickness

## Configuration

Edit `config.py` to modify:
- Host and port settings
- CORS origins
- API metadata

## Development

The backend runs in reload mode by default for development. Changes to Python files will automatically restart the server.

## Production

For production deployment:
1. Set `RELOAD=false` in environment variables
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins
4. Set up proper logging and monitoring



