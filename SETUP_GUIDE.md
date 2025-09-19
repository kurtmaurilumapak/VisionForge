# VisionForge Setup Guide

Complete setup guide for VisionForge desktop application with FastAPI backend.

## Prerequisites

### 1. Node.js and npm
- Download and install Node.js from [nodejs.org](https://nodejs.org/)
- Verify installation: `node --version` and `npm --version`

### 2. Python 3.8+
- Download and install Python from [python.org](https://www.python.org/)
- **Important**: Check "Add Python to PATH" during installation
- Verify installation: `python --version` and `pip --version`

### 3. Git (Optional)
- Download from [git-scm.com](https://git-scm.com/)

## Installation Steps

### 1. Install Frontend Dependencies
```bash
# Install Node.js dependencies
npm install
```

### 2. Install Backend Dependencies
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Check if all dependencies are installed
npm list
cd backend && pip list
```

## Running the Application

### Development Mode (Frontend + Backend)
```bash
# Start both frontend and backend
npm run dev:full
```

### Electron App (Full Desktop App)
```bash
# Start frontend, backend, and Electron
npm run electron:full
```

### Individual Services
```bash
# Frontend only
npm run dev

# Backend only
npm run backend

# Electron only (after building)
npm run build
npm run electron
```

## Project Structure

```
VisionForge/
├── src/                    # Vue.js frontend
│   ├── components/         # Vue components
│   ├── composables/        # Vue composables
│   ├── services/           # API services
│   └── ...
├── backend/                # FastAPI backend
│   ├── models/             # Pydantic models
│   ├── services/           # Image processing
│   ├── main.py            # FastAPI app
│   └── requirements.txt   # Python dependencies
├── electron/               # Electron main process
└── package.json           # Node.js dependencies
```

## API Endpoints

The backend provides these endpoints:

- `GET /` - API information
- `GET /health` - Health check
- `POST /process-image` - Process uploaded image
- `POST /process-image-base64` - Process base64 image

## Troubleshooting

### Python Not Found
- Ensure Python is installed and added to PATH
- Try `python3` instead of `python`
- On Windows, try `py` command

### Port Already in Use
- Kill existing processes: `taskkill /f /im node.exe`
- Change ports in `vite.config.js` and `backend/config.py`

### CORS Issues
- Ensure backend is running on port 8000
- Check CORS origins in `backend/config.py`

### Electron Issues
- Ensure all dependencies are installed
- Try running `npm run build` first

## Features

### Frontend Controls
- **Color**: Grayscale, color space conversion
- **Transform**: Rotation, translation, scaling, cropping
- **Filters**: Blur, sharpening
- **Edges**: Canny, Sobel edge detection
- **Bitwise**: NOT, AND, OR, XOR operations
- **Adaptive Threshold**: Mean/Gaussian thresholding
- **Morphology**: Kernel operations
- **Color Boost**: Saturation, hue, RGB gains
- **Draw**: Shapes and text with color picker

### Backend Processing
- OpenCV-based image processing
- Real-time image manipulation
- Support for multiple image formats
- RESTful API with FastAPI
- CORS-enabled for frontend communication

## Development

### Hot Reload
- Frontend: Automatic with Vite
- Backend: Automatic with uvicorn reload
- Electron: Manual restart required

### Adding New Controls
1. Add to `src/composables/useControls.js`
2. Add UI to `src/components/ControlPanel.vue`
3. Implement processing in `backend/services/image_processor.py`
4. Add API endpoint if needed

## Production Deployment

### Backend
1. Set `RELOAD=false` in environment
2. Use production WSGI server (Gunicorn)
3. Configure proper CORS origins
4. Set up logging and monitoring

### Electron
1. Run `npm run electron:build`
2. Distribute generated packages
3. Test on target platforms

## Support

If you encounter issues:
1. Check this setup guide
2. Verify all prerequisites are installed
3. Check console logs for errors
4. Ensure all services are running on correct ports



