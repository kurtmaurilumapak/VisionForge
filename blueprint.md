# VisionForge Blueprint

## 1. Overview

VisionForge is a responsive, web-based image viewing application. It provides users with a simple interface to upload and view images directly in the browser. The application features a real-time preview of the uploaded image. The front-end is built with Vue.js and Vuetify.

## 2. How to Run the Application

This project is a Vue.js frontend application. The development environment is managed by a `.idx/dev.nix` file, which automatically installs all necessary dependencies.

**You do not need to run `npm install` manually.**

### 2.1. Frontend (Vue.js)

The frontend web server is configured to start automatically when your workspace launches. You can access it through the **Previews** panel in your IDE.

1.  Open the **Previews** panel.
2.  You will see a preview named `web`.
3.  Click on it to open the VisionForge application in a new tab.

## 3. Project Features & Design

### 3.1. Layout & Style
*   **Theme:** High-contrast, OLED black theme for a minimalist and focused user experience. The global theme is set to `'dark'` in the Vuetify plugin.
*   **Primary Background:** `black` for all layout and component backgrounds.
*   **Layout:** A seamless, integrated design.
    *   The **Control Panel** is fully integrated into the navigation drawer. It is borderless and shares the same background, appearing as part of the sidebar, not a separate card.
    *   The **Main Content** area is a single, border-outlined card.
*   **Header:** A main application bar with:
    *   The title "VisionForge".
    *   An outlined "Upload" button and an outlined "Export" dropdown menu for high visibility.
*   **Controls:** All input controls (`v-select`, `v-text-field`, etc.) use a consistent, compact `solo-filled` and `flat` style for a minimal footprint.

### 3.2. Responsiveness
*   **Large Screens (lg and up):**
    *   The `ControlPanel` is visible on the left, seamlessly integrated into the permanent navigation drawer.
    *   The `ImageDisplay` shows the original and processed images side-by-side.
*   **Medium & Small Screens (md and down):**
    *   The `ControlPanel` is hidden by default in a temporary navigation drawer.
    *   A burger icon in the header toggles the drawer.
    *   The "Original" and "Processed" images stack vertically.

### 3.3. Core Components
*   **`App.vue`**: Orchestrates the responsive layout and global components.
*   **`ControlPanel.vue`**: Contains all image manipulation controls, organized into a clean accordion-style menu using Vuetify's `v-expansion-panels`. Each category (Color, Transform, etc.) can be expanded or collapsed. This component is styled to be borderless and fully integrated into its parent navigation drawer.
*   **`FileUpload.vue`**: A full-width, welcoming prompt for users to upload their first image.
*   **`ImageDisplay.vue`**: A responsive component for side-by-side image comparison.

### 3.4. State Management
*   **`useControls.js`**: A Vue composable for managing the state of all image processing controls.
