# VisionForge Image Editor

<div align="center">
  <img src="public/appicon.png" alt="VisionForge Logo" width="128" height="128">
  <h3>Professional Image Processing and Editing Application</h3>
  <p>A powerful desktop application built with Vue.js, Electron, and Python OpenCV for advanced image processing and batch operations.</p>
</div>

## 🌟 Features

### 🎨 **Advanced Image Processing**
- **Color Adjustments**: Brightness, Contrast, Saturation, Hue, Temperature, Tint
- **Color Spaces**: RGB, LAB, HSV conversion
- **Filters**: Blur, Sharpen, Noise reduction, Gamma correction
- **Advanced Effects**: Edge detection, Morphological operations, Adaptive thresholding
- **Transformations**: Rotate, Scale, Translate with multiple interpolation methods

### 🖼️ **Interactive Tools**
- **Crop Tool**: Interactive cropping with aspect ratio controls
- **Drawing Tools**: Rectangles, Circles, Lines, Text with customizable colors
- **Real-time Preview**: See changes instantly as you adjust controls

### 📦 **Batch Processing**
- **Multiple Images**: Process hundreds of images simultaneously
- **Consistent Settings**: Apply the same effects to all images
- **Progress Tracking**: Real-time progress monitoring with cancel option
- **Export Options**: Download individual images, ZIP archive, or PDF report

### 🖥️ **Desktop Application**
- **Cross-Platform**: Windows, macOS, and Linux support
- **Native Performance**: Built with Electron for optimal performance
- **Auto Backend**: Python OpenCV backend starts automatically
- **Modern UI**: Clean, intuitive interface with dark theme

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/visionforge-image-editor.git
   cd visionforge-image-editor
   ```

2. **Install dependencies**
   ```bash
   # Install Node.js dependencies
   npm install
   
   # Install Python dependencies
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Run the application**
   ```bash
   # Development mode
   npm run dev:full
   
   # Or run desktop app directly
   npm run electron:start
   ```

## 📖 User Guide

### Getting Started

1. **Launch the Application**
   - The app will start with the backend automatically
   - You'll see the main interface with upload options

2. **Upload Images**
   - Click "Upload Image" for single image processing
   - Select multiple files for batch processing
   - Supported formats: JPG, PNG, BMP, TIFF, WebP

3. **Adjust Controls**
   - Use the sidebar controls to modify your image
   - Changes are applied in real-time
   - Reset controls to return to original image

### Image Processing Controls

#### 🎨 **Color Adjustments**
- **Brightness**: Adjust image brightness (-100 to +100)
- **Contrast**: Enhance or reduce contrast (-100 to +100)
- **Saturation**: Control color intensity (-100 to +100)
- **Hue**: Shift color hues (-180 to +180)
- **Temperature**: Warm or cool the image (-100 to +100)
- **Tint**: Adjust magenta/green balance (-100 to +100)

#### 🔧 **Advanced Filters**
- **Blur**: Gaussian blur with adjustable kernel size
- **Sharpen**: Enhance image details
- **Noise**: Add or reduce image noise
- **Gamma**: Adjust mid-tone brightness
- **Exposure**: Control overall exposure

#### 🌈 **Color Space Conversion**
- **RGB**: Standard red-green-blue color space
- **LAB**: Perceptually uniform color space
- **HSV**: Hue-saturation-value color space

#### 🔍 **Edge Detection**
- **Canny**: Advanced edge detection with dual thresholds
- **Sobel**: Gradient-based edge detection
- **Laplacian**: Second derivative edge detection

#### 🧮 **Morphological Operations**
- **Erosion**: Shrink bright regions
- **Dilation**: Expand bright regions
- **Opening**: Erosion followed by dilation
- **Closing**: Dilation followed by erosion
- **Gradient**: Difference between dilation and erosion

#### ✂️ **Crop Tool**
- **Interactive Selection**: Click and drag to select crop area
- **Aspect Ratios**: Square, 16:9, 4:3, or custom
- **Precise Control**: Adjust position and size with sliders
- **Reset**: Return to full image

### Batch Processing

1. **Upload Multiple Images**
   - Select multiple files when uploading
   - Images will appear in a grid layout

2. **Configure Settings**
   - Adjust controls as desired
   - Settings will be applied to all images

3. **Process Images**
   - Click "Process All" to start batch processing
   - Monitor progress in real-time
   - Cancel processing if needed

4. **Export Results**
   - Download individual processed images
   - Create ZIP archive of all images
   - Generate PDF report with thumbnails

### Export Options

#### 📁 **Single Image Export**
- **PNG**: High-quality lossless format
- **JPG**: Compressed format for smaller file sizes
- **PDF Report**: Professional report with settings

#### 📦 **Batch Export**
- **Download All**: Individual image files
- **ZIP Archive**: Compressed folder of all images
- **PDF Report**: Comprehensive report with thumbnails and settings

## 🛠️ Development

### Project Structure
```
visionforge-image-editor/
├── src/                    # Vue.js frontend
│   ├── components/         # Vue components
│   ├── composables/        # Vue composables
│   ├── services/           # API services
│   └── plugins/            # Vuetify configuration
├── electron/               # Electron main process
│   ├── main.js            # Main Electron process
│   └── preload.js         # Preload script
├── backend/               # Python FastAPI backend
│   ├── main.py            # FastAPI application
│   ├── models/            # Pydantic models
│   └── requirements.txt   # Python dependencies
├── public/                # Static assets
└── dist-electron/         # Built application
```

### Available Scripts

```bash
# Development
npm run dev                 # Start Vue.js dev server
npm run backend            # Start Python backend
npm run dev:full          # Start both frontend and backend

# Electron
npm run electron:start    # Run Electron app
npm run electron:dev      # Run Electron in development mode
npm run electron:build    # Build Electron app
npm run electron:dist     # Create distributable

# Build
npm run build             # Build Vue.js app
npm run preview           # Preview built app
```

### Building for Distribution

1. **Bundle Backend for Machines without Python**
   - Build a standalone backend executable with PyInstaller first (see `backend/README.md`).
   - Place the built file into `backend/dist_backend` (Windows: `visionforge_backend.exe`).
   - The Electron builder is configured to include this in the installer.

2. **Build the Application**
   ```bash
   npm run electron:dist
   ```

3. **Find the Executable**
   - Windows: `dist-electron/win-unpacked/VisionForge Image Editor.exe`
   - macOS: `dist-electron/mac/VisionForge Image Editor.app`
   - Linux: `dist-electron/linux/VisionForge Image Editor.AppImage`

## 🔧 Configuration

### Backend Configuration
The Python backend runs on `http://localhost:8000` by default. You can modify the configuration in `backend/main.py`:

```python
HOST = "0.0.0.0"
PORT = 8000
RELOAD = False  # Set to True for development
```

### Frontend Configuration
The Vue.js frontend runs on `http://localhost:5173` in development mode. Configuration can be modified in `vite.config.js`.

## 🐛 Troubleshooting

### Common Issues

1. **Backend Not Starting**
   - Ensure Python is installed and in PATH
   - Install Python dependencies: `pip install -r backend/requirements.txt`
   - Check if port 8000 is available

2. **Images Not Processing**
   - Verify backend is running
   - Check browser console for errors
   - Ensure image format is supported

3. **Controls Not Working**
   - Refresh the page
   - Check if user interaction is detected
   - Verify control state in browser console

4. **Export Issues**
   - Ensure you have processed images
   - Check browser download permissions
   - Verify file system write permissions

### Debug Mode
Enable debug logging by opening browser console (F12) and checking for error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Vue.js** - Progressive JavaScript framework
- **Electron** - Cross-platform desktop app framework
- **Vuetify** - Material Design component framework
- **FastAPI** - Modern Python web framework
- **OpenCV** - Computer vision library
- **Vite** - Fast build tool

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/visionforge-image-editor/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs

---

<div align="center">
  <p>Made with ❤️ by the VisionForge Team</p>
  <p>⭐ Star this repository if you found it helpful!</p>
</div>