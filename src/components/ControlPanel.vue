
<template>
  <div class="pa-4 fill-height d-flex flex-column w-100">
    <h2 class="text-h6 d-flex align-center mb-4">
      Controls
      <v-spacer></v-spacer>
              <v-btn small variant="tonal" color="primary" @click="handleResetAll">Reset All</v-btn>
    </h2>

    <div class="control-panels-container flex-grow-1 overlay-scrollbar">
      <v-expansion-panels v-model="panel" variant="accordion" multiple class="control-panels">
        
        <!-- COLOR PANEL -->
        <v-expansion-panel value="color" title="Color" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Grayscale Amount</v-label>
                      <v-slider v-model="controlState.grayscaleAmount" :min="0" :max="1" :step="0.01" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label class="text-subtitle-1">Color Space</v-label>
                      <v-select v-model="controlState.colorSpace" :items="['RGB', 'HSV', 'LAB', 'YCrCb']" variant="solo-filled" flat density="compact" class="mt-2"></v-select>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- TRANSFORM PANEL -->
        <v-expansion-panel value="transform" title="Transform" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label>Rotate</v-label>
                      <v-slider v-model="controlState.rotate" :min="-180" :max="180" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <div class="control-group">
              <v-label>Translate X</v-label>
                      <v-slider v-model="controlState.translateX" :min="-200" :max="200" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <div class="control-group">
              <v-label>Translate Y</v-label>
                      <v-slider v-model="controlState.translateY" :min="-200" :max="200" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <div class="control-group">
              <v-label>Scale</v-label>
                      <v-slider v-model="controlState.scale" :min="0.1" :max="3.0" :step="0.01" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <div class="control-group">
              <v-label>Interpolation</v-label>
                      <v-select v-model="controlState.scaleInterpolation" :items="['nearest', 'linear', 'cubic', 'area', 'lanczos']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
            </div>
            
            <v-divider class="my-4"></v-divider>

            <div class="control-group">
              <v-label class="text-subtitle-1 mb-2">Crop</v-label>
                      <v-switch 
                        v-model="isCropActive" 
                        label="Enable Crop Tool" 
                        color="primary" 
                        class="mt-2"
                        @update:model-value="onCropToggle"
                      ></v-switch>
              
              <div v-if="isCropActive" class="mt-4">
                <v-alert type="info" variant="tonal" density="compact" class="mb-3">
                  Click and drag on the image to create a crop area
                </v-alert>
                
              <v-row dense>
                          <v-col cols="6"><v-text-field v-model.number="controlState.crop.x" label="X (%)" type="number" :min="0" :max="100" :step="0.1" variant="solo-filled" flat density="compact" hide-details ></v-text-field></v-col>
                          <v-col cols="6"><v-text-field v-model.number="controlState.crop.y" label="Y (%)" type="number" :min="0" :max="100" :step="0.1" variant="solo-filled" flat density="compact" hide-details ></v-text-field></v-col>
                          <v-col cols="6" class="mt-2"><v-text-field v-model.number="controlState.crop.w" label="Width (%)" type="number" :min="1" :max="100" :step="0.1" variant="solo-filled" flat density="compact" hide-details ></v-text-field></v-col>
                          <v-col cols="6" class="mt-2"><v-text-field v-model.number="controlState.crop.h" label="Height (%)" type="number" :min="1" :max="100" :step="0.1" variant="solo-filled" flat density="compact" hide-details ></v-text-field></v-col>
              </v-row>

            <div class="control-group">
              <v-label class="mt-2">Aspect Lock</v-label>
                  <v-select v-model="controlState.cropAspect" :items="['None', '1:1', '4:3', '16:9']" variant="solo-filled" flat density="compact" class="mt-2"  @update:model-value="applyAspectRatio"></v-select>
                </div>
                
                        <v-btn 
                          @click="resetCrop" 
                          size="small" 
                          variant="outlined" 
                          color="primary" 
                          class="mt-2"
                        >
                          Reset Crop
                        </v-btn>
              </div>
            </div>

          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- FILTERS PANEL -->
        <v-expansion-panel value="filters" title="Filters" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Blur Method</v-label>
                      <v-select v-model="controlState.blur.method" :items="['gaussian', 'median', 'bilateral', 'box']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
            </div>
            <div class="control-group">
              <v-label>Kernel Size</v-label>
                      <v-slider v-model="controlState.blur.ksize" :min="3" :max="31" :step="2" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <v-divider class="my-4"></v-divider>
            <div class="control-group">
              <v-label class="text-subtitle-1">Sharpen Strength</v-label>
                      <v-slider v-model="controlState.sharpenStrength" :min="0" :max="2" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- EDGES PANEL -->
        <v-expansion-panel value="edges" title="Edges" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Edge Detection</v-label>
                      <v-select v-model="controlState.edges.method" :items="['None', 'Canny', 'Sobel']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
            </div>
            <div v-if="controlState.edges.method === 'Canny'">
                      <v-slider v-model="controlState.edges.canny_t1" :min="0" :max="255" label="T1" thumb-label color="primary" class="mt-2" ></v-slider>
                      <v-slider v-model="controlState.edges.canny_t2" :min="0" :max="255" label="T2" thumb-label color="primary" class="mt-2" ></v-slider>
                      <v-checkbox v-model="controlState.edges.link_canny_t2" label="Link T2 = 2 * T1" ></v-checkbox>
                    </div>
                    <div v-if="controlState.edges.method === 'Sobel'">
                      <v-label class="text-subtitle-1">Kernel Size</v-label>
                      <v-select v-model="controlState.edges.sobel_ksize" :items="[3, 5, 7]" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
                    </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- BITWISE OPERATIONS PANEL -->
        <v-expansion-panel value="bitwise" title="Bitwise Operations" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Operation</v-label>
                      <v-select v-model="controlState.bitwise.operation" :items="['None', 'NOT', 'AND', 'OR', 'XOR']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
                    </div>
                    <div v-if="['AND', 'OR', 'XOR'].includes(controlState.bitwise.operation)">
                      <v-label class="text-subtitle-1">Mask Threshold</v-label>
                      <v-slider v-model="controlState.bitwise.maskThreshold" :min="0" :max="255" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <div v-if="['AND', 'OR', 'XOR'].includes(controlState.bitwise.operation)" class="control-group">
                      <v-label class="text-subtitle-1">Mask Upload (Optional)</v-label>
                      <v-file-input v-model="controlState.bitwise.maskUpload" accept="image/*" variant="solo-filled" flat density="compact" hide-details class="mt-2" ></v-file-input>
                    </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- ADAPTIVE THRESHOLD PANEL -->
        <v-expansion-panel value="adaptive" title="Adaptive Threshold" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Mode</v-label>
                      <v-select v-model="controlState.adaptiveThreshold.mode" :items="['Simple', 'Adaptive']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
                    </div>
                    <div v-if="controlState.adaptiveThreshold.mode === 'Adaptive'">
                      <div class="control-group">
                        <v-label class="text-subtitle-1">Method</v-label>
                        <v-select v-model="controlState.adaptiveThreshold.method" :items="['mean', 'gaussian']" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
                      </div>
                      <div class="control-group">
                        <v-label class="text-subtitle-1">Block Size</v-label>
                        <v-slider v-model="controlState.adaptiveThreshold.blockSize" :min="3" :max="51" :step="2" thumb-label color="primary" class="mt-2" ></v-slider>
                      </div>
                      <div class="control-group">
                        <v-label class="text-subtitle-1">C</v-label>
                        <v-slider v-model="controlState.adaptiveThreshold.c" :min="-20" :max="20" thumb-label color="primary" class="mt-2" ></v-slider>
                      </div>
                    </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

                <!-- MORPHOLOGY PANEL -->
                <v-expansion-panel value="morphology" title="Morphology" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
                  <v-expansion-panel-text>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Operation</v-label>
                      <v-select v-model="controlState.morphology.operation" :items="[
                        { title: 'Erode + Dilate', value: 'erode_dilate' },
                        { title: 'Dilate + Erode', value: 'dilate_erode' },
                        { title: 'Erode Only', value: 'erode' },
                        { title: 'Dilate Only', value: 'dilate' },
                        { title: 'Opening', value: 'open' },
                        { title: 'Closing', value: 'close' },
                        { title: 'Gradient', value: 'gradient' },
                        { title: 'Top Hat', value: 'tophat' },
                        { title: 'Black Hat', value: 'blackhat' }
                      ]" variant="solo-filled" flat density="compact" class="mt-2" ></v-select>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Kernel Size</v-label>
                      <v-slider v-model="controlState.morphology.kernelSize" :min="1" :max="25" :step="2" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Iterations</v-label>
                      <v-slider v-model="controlState.morphology.iterations" :min="1" :max="5" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>

        <!-- COLOR BOOST PANEL -->
        <v-expansion-panel value="colorboost" title="Color Boost" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Saturation</v-label>
                      <v-slider v-model="controlState.colorBoost.saturation" :min="-1" :max="2" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Hue Shift</v-label>
                      <v-slider v-model="controlState.colorBoost.hueShift" :min="-180" :max="180" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Vibrance</v-label>
                      <v-slider v-model="controlState.colorBoost.vibrance" :min="0" :max="2" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <v-divider class="my-4"></v-divider>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">RGB Channel Gains</v-label>
                      <v-slider v-model="controlState.colorBoost.rgbGains.r" :min="0" :max="2" :step="0.1" label="Red" thumb-label color="red" class="mt-2" ></v-slider>
                      <v-slider v-model="controlState.colorBoost.rgbGains.g" :min="0" :max="2" :step="0.1" label="Green" thumb-label color="green" class="mt-2" ></v-slider>
                      <v-slider v-model="controlState.colorBoost.rgbGains.b" :min="0" :max="2" :step="0.1" label="Blue" thumb-label color="blue" class="mt-2" ></v-slider>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Contrast</v-label>
                      <v-slider v-model="controlState.colorBoost.contrast" :min="-1" :max="1" :step="0.1" thumb-label color="primary" class="mt-2" ></v-slider>
                    </div>
                    <div class="control-group">
                      <v-label class="text-subtitle-1">Brightness</v-label>
                      <v-slider v-model="controlState.colorBoost.brightness" :min="-100" :max="100" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

         <!-- DRAW PANEL -->
        <v-expansion-panel value="draw" title="Draw" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
            <v-expansion-panel-text>
                 <div class="d-flex ga-2 mb-4">
                            <v-btn @click="addDrawItem('rect')" size="small" variant="tonal" >Rect</v-btn>
                            <v-btn @click="addDrawItem('circle')" size="small" variant="tonal" >Circle</v-btn>
                            <v-btn @click="addDrawItem('line')" size="small" variant="tonal" >Line</v-btn>
                            <v-btn @click="addDrawItem('text')" size="small" variant="tonal" >Text</v-btn>
                </div>

                <v-card v-for="(item, index) in controlState.drawItems" :key="index" class="mb-4" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
                    <v-card-title class="d-flex align-center text-subtitle-2 pa-2">
                        <span class="text-capitalize">{{ item.type }}</span>
                        <v-spacer></v-spacer>
                        <v-btn icon size="x-small" variant="text" @click="removeDrawItem(index)" ><v-icon>mdi-close</v-icon></v-btn>
                    </v-card-title>
                    <v-card-text class="pa-2">
                        <!-- Rectangle Controls -->
                        <v-row v-if="item.type === 'rect'" dense>
                            <v-col><v-text-field v-model.number="item.xywh[0]" label="X" type="number" density="compact" hide-details ></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[1]" label="Y" type="number" density="compact" hide-details ></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[2]" label="W" type="number" density="compact" hide-details ></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[3]" label="H" type="number" density="compact" hide-details ></v-text-field></v-col>
                        </v-row>
                         <!-- Text Controls -->
                        <div v-if="item.type === 'text'">
                            <v-text-field v-model="item.text" label="Text" density="compact" hide-details class="mb-2" ></v-text-field>
                             <v-row dense>
                                <v-col><v-text-field v-model.number="item.xy[0]" label="X" type="number" density="compact" hide-details ></v-text-field></v-col>
                                <v-col><v-text-field v-model.number="item.xy[1]" label="Y" type="number" density="compact" hide-details ></v-text-field></v-col>
                                <v-col><v-text-field v-model.number="item.scale" label="Scale" type="number" step="0.1" density="compact" hide-details ></v-text-field></v-col>
                            </v-row>
                        </div>
                         <!-- Color Picker -->
                        <div class="control-group">
                            <v-label class="text-subtitle-1">Color</v-label>
                            <v-color-picker 
                                v-model="item.color" 
                                mode="hex" 
                                hide-mode-switch 
                                hide-inputs
                                class="mt-2 color-picker-compact" 
                                width="180"
                                height="120"
>
                            </v-color-picker>
                        </div>
                        
                         <!-- Shared Controls -->
                        <v-slider v-model="item.thickness" label="Thickness" :min="1" :max="10" thumb-label color="primary" class="mt-2" ></v-slider>

                    </v-card-text>
                </v-card>
            </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- OPERATIONS PANEL -->
        <v-expansion-panel value="operations" title="Operations" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Brightness</v-label>
                      <v-slider v-model="controlState.brightness" :min="-100" :max="100" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
            <div class="control-group">
              <v-label class="text-subtitle-1">Blend with Original</v-label>
                      <v-slider v-model="controlState.blendAlpha" :min="0" :max="1" :step="0.01" label="Alpha" thumb-label color="primary" class="mt-2" ></v-slider>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

      </v-expansion-panels>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useControls } from '../composables/useControls.js';

const { controlState, resetAll, addDrawItem, removeDrawItem } = useControls();

// Override resetAll to also reset user interaction flag
const handleResetAll = () => {
  console.log('Resetting all controls...');
  resetAll();
  hasControlsChanged.value = false;
  console.log('Emitting controls-reset event');
  emit('controls-reset');
  
  // Call parent reset method
  setTimeout(() => {
    console.log('Calling parent reset method directly');
    if (window.parentApp) {
      window.parentApp.handleControlsReset();
    }
  }, 50);
};

const emit = defineEmits(['user-interaction', 'controls-reset']);

const markUserInteraction = () => {
  emit('user-interaction');
};

// Track if any control has been changed from its initial state
const hasControlsChanged = ref(false);

// Check if controls are in initial state
const isInitialState = () => {
  const initial = {
    grayscaleAmount: 0,
    colorSpace: 'RGB',
    rotate: 0,
    translateX: 0,
    translateY: 0,
    scale: 1,
    scaleInterpolation: 'linear',
    crop: { x: 0, y: 0, w: 0, h: 0 },
    cropAspect: 'None',
    blur: { method: 'gaussian', ksize: 3 },
    sharpenStrength: 0,
    edges: { method: 'None', canny_t1: 50, canny_t2: 100, link_canny_t2: true, sobel_ksize: 3 },
    bitwise: { operation: 'None', maskThreshold: 128, maskUpload: null },
    adaptiveThreshold: { mode: 'Simple', method: 'mean', blockSize: 11, c: 2 },
    morphology: { kernelSize: 3, iterations: 1, operation: 'erode_dilate' },
    colorBoost: { saturation: 0, hueShift: 0, vibrance: 1, rgbGains: { r: 1, g: 1, b: 1 }, contrast: 0, brightness: 0 },
    drawItems: [],
    brightness: 0,
    blendAlpha: 0,
  };
  
  return JSON.stringify(controlState) === JSON.stringify(initial);
};

// Watch for any changes to control state and mark as user interaction
watch(controlState, () => {
  // Only mark as user interaction if we haven't already done so
  // and if the controls are not in their initial state
  if (!hasControlsChanged.value && !isInitialState()) {
    hasControlsChanged.value = true;
    markUserInteraction();
  }
}, { deep: true });

// Crop functionality
const isCropActive = ref(false);

const onCropToggle = (value) => {
  isCropActive.value = value;
  if (!value) {
    // Reset crop when disabled
    controlState.crop = { x: 0, y: 0, w: 0, h: 0 };
  } else {
    // Set a default crop when enabled
    controlState.crop = { x: 20, y: 20, w: 40, h: 40 };
  }
};

const applyAspectRatio = (aspect) => {
  if (aspect === 'None' || !isCropActive.value) return;
  
  const currentWidth = controlState.crop.w;
  let newHeight = currentWidth;
  
  switch (aspect) {
    case '1:1':
      newHeight = currentWidth;
      break;
    case '4:3':
      newHeight = (currentWidth * 3) / 4;
      break;
    case '16:9':
      newHeight = (currentWidth * 9) / 16;
      break;
  }
  
  // Ensure height doesn't exceed 100%
  if (controlState.crop.y + newHeight > 100) {
    newHeight = 100 - controlState.crop.y;
  }
  
  controlState.crop.h = Math.max(1, Math.min(100, newHeight));
};

const resetCrop = () => {
  controlState.crop = { x: 0, y: 0, w: 0, h: 0 };
};

// Reset controls changed flag when new file is uploaded
const resetControlsChanged = () => {
  hasControlsChanged.value = false;
};

// Expose crop state for parent component
defineExpose({
  isCropActive,
  resetControlsChanged,
  handleResetAll,
  resetAll
});

// By default, open the 'color' and 'transform' panels
const panel = ref(['color', 'transform', 'edges', 'bitwise', 'colorboost']);

// Watchers for linked controls
watch(() => controlState.edges.link_canny_t2, (isLinked) => {
  if (isLinked) {
    controlState.edges.canny_t2 = controlState.edges.canny_t1 * 2;
  }
});
watch(() => controlState.edges.canny_t1, (t1) => {
  if (controlState.edges.link_canny_t2) {
    controlState.edges.canny_t2 = t1 * 2;
  }
});

// Watcher for crop validation
watch(() => controlState.crop, (newCrop) => {
  if (newCrop) {
    // Ensure crop values are non-negative and rounded to 1 decimal place
    if (newCrop.x < 0) newCrop.x = 0;
    if (newCrop.y < 0) newCrop.y = 0;
    if (newCrop.w < 0) newCrop.w = 0;
    if (newCrop.h < 0) newCrop.h = 0;
    
    // Round to 1 decimal place
    newCrop.x = Math.round(newCrop.x * 10) / 10;
    newCrop.y = Math.round(newCrop.y * 10) / 10;
    newCrop.w = Math.round(newCrop.w * 10) / 10;
    newCrop.h = Math.round(newCrop.h * 10) / 10;
  }
}, { deep: true });

</script>

<style scoped>
.control-panels-container {
  overflow-y: auto;
}
.control-group {
  margin-bottom: 1.5rem; /* 24px */
}
.control-group:last-child {
  margin-bottom: 0;
}
.v-btn { text-transform: capitalize; }
.v-slider { 
  position: relative;
  z-index: 100; /* Ensure sliders are interactive inside panels */
}

/* Style the expansion panels for a seamless look */
.v-expansion-panel {
  border-radius: 4px !important;
  margin-bottom: 8px;
}
.v-expansion-panel-title {
  font-weight: 500;
}
.v-expansion-panel-text__wrapper {
  padding: 16px;
}

/* Color picker styling */
.color-picker-compact {
  border-radius: 8px;
  overflow: hidden;
}

        .color-picker-compact .v-color-picker__canvas {
          border-radius: 8px;
        }

        /* Control panels styling */
        .control-panels .v-expansion-panel {
          margin-bottom: 8px;
          border-radius: 8px;
        }

        .control-panels .v-expansion-panel:last-child {
          margin-bottom: 0;
        }

        .control-panels .v-expansion-panel-title {
          background: transparent !important;
        }

        .control-panels .v-expansion-panel-text {
          background: transparent !important;
        }

</style>
