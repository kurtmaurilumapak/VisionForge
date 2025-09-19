
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

  // Draw
  drawItems: [],

  // Operations
  brightness: 0,
  blendAlpha: 0,
});

const controlState = reactive(getInitialState());

export function useControls() {

  const resetAll = () => {
    Object.assign(controlState, getInitialState());
  };

  const addDrawItem = (type) => {
    let newItem;
    switch(type) {
        case 'rect':
            newItem = { type: 'rect', xywh: [10, 10, 50, 50], color: '#FF0000', thickness: 2 };
            break;
        case 'circle':
            newItem = { type: 'circle', xyr: [50, 50, 25], color: '#00FF00', thickness: 2 };
            break;
        case 'line':
            newItem = { type: 'line', xyxy: [10, 10, 100, 100], color: '#0000FF', thickness: 2 };
            break;
        case 'text':
            newItem = { type: 'text', xy: [20, 20], text: 'Hello', scale: 1, color: '#FFFF00', thickness: 2 };
            break;
    }
    controlState.drawItems.push(newItem);
  };

  const removeDrawItem = (index) => {
    controlState.drawItems.splice(index, 1);
  };

  return { controlState, resetAll, addDrawItem, removeDrawItem };
}
