# VisionForge Desktop App

This is the desktop version of VisionForge built with Electron.

## Development

To run the app in development mode (with hot reload):

```bash
npm run electron:dev
```

This will:
1. Start the Vite development server
2. Wait for it to be ready
3. Launch the Electron app

## Production

To build and run the production version:

```bash
# Build the Vue app
npm run build

# Run the Electron app
npm run electron
```

## Building Distributables

To create installable packages for different platforms:

```bash
# Build for current platform
npm run electron:dist

# Build for all platforms (requires platform-specific tools)
npm run electron:build
```

## Features

- **Native File Dialog**: Use File > Open Image or Ctrl+O to open images
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Native Menu**: Full application menu with standard shortcuts
- **Secure**: Uses context isolation and preload scripts for security

## File Structure

```
electron/
├── main.js          # Main Electron process
├── preload.js       # Preload script for secure IPC
└── package.json     # Electron-specific package config
```

## Scripts

- `npm run electron` - Run the built app
- `npm run electron:dev` - Run in development mode with hot reload
- `npm run electron:build` - Build distributables
- `npm run electron:dist` - Build for current platform only



