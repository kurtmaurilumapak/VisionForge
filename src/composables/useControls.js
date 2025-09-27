
import { reactive } from 'vue';

const getInitialState = () => ({
  // Color
  grayscaleAmount: 0,
  colorSpace: 'RGB',

  // Transform
  rotate: 0,
  translateX: 0,
  translateY: 0,
  scale: 1,
  scaleInterpolation: 'linear',
  crop: { x: 0, y: 0, w: 0, h: 0 },
  cropAspect: 'None',

  // Filters
  blur: { method: 'gaussian', ksize: 3 },
  sharpenStrength: 0,

  // Edges
  edges: { method: 'None', canny_t1: 50, canny_t2: 100, link_canny_t2: true, sobel_ksize: 3 },

  // Bitwise Operations
  bitwise: { 
    operation: 'None', 
    maskThreshold: 128, 
    maskUpload: null 
  },

  // Adaptive Threshold
  adaptiveThreshold: { 
    mode: 'Simple', 
    method: 'mean', 
    blockSize: 11, 
    c: 2 
  },

  // Morphology
  morphology: { 
    kernelSize: 3, 
    iterations: 1,
    operation: 'erode_dilate'
  },

  // Color Boost
  colorBoost: { 
    saturation: 0, 
    hueShift: 0, 
    vibrance: 1, 
    rgbGains: { r: 1, g: 1, b: 1 }, 
    contrast: 0, 
    brightness: 0 
  },

  // Draw
  drawItems: [],

  // Operations
  brightness: 0,
  blendAlpha: 0,
});

const controlState = reactive(getInitialState());

export function useControls() {

  const resetAll = () => {
    const initialState = getInitialState();
    // Clear all properties first
    Object.keys(controlState).forEach(key => {
      delete controlState[key];
    });
    // Then assign new values
    Object.assign(controlState, initialState);
  };

  const addDrawItem = (type) => {
    let newItem;
    const defaultColor = '#FF0000'; // Default red color for all shapes
    
    switch(type) {
        case 'rect':
            newItem = { 
              type: 'rect', 
              x: 10, y: 10, w: 50, h: 50,  // Universal positioning
              xywh: [10, 10, 50, 50],       // Legacy compatibility
              color: defaultColor, 
              thickness: 2 
            };
            break;
        case 'circle':
            newItem = { 
              type: 'circle', 
              x: 25, y: 25, w: 50, h: 50,  // Universal positioning (center-based)
              xyr: [50, 50, 25],            // Legacy compatibility
              color: defaultColor, 
              thickness: 2 
            };
            break;
        case 'line':
            newItem = { 
              type: 'line', 
              x: 10, y: 10, w: 90, h: 90,  // Universal positioning (bounding box)
              xyxy: [10, 10, 100, 100],     // Legacy compatibility
              color: defaultColor, 
              thickness: 2 
            };
            break;
        case 'text':
            newItem = { 
              type: 'text', 
              x: 20, y: 20, w: 100, h: 20, // Universal positioning
              xy: [20, 20],                 // Legacy compatibility
              text: 'Hello', 
              scale: 1, 
              color: defaultColor, 
              thickness: 2 
            };
            break;
    }
    controlState.drawItems.push(newItem);
  };

  const removeDrawItem = (index) => {
    controlState.drawItems.splice(index, 1);
  };

  return { controlState, resetAll, addDrawItem, removeDrawItem };
}
