
<template>
  <div class="pa-4 fill-height d-flex flex-column w-100">
    <h2 class="text-h6 d-flex align-center mb-4">
      Controls
      <v-spacer></v-spacer>
      <v-btn small variant="tonal" color="primary" @click="resetAll">Reset All</v-btn>
    </h2>

    <div class="control-panels-container flex-grow-1">
      <v-expansion-panels v-model="panel" variant="accordion" multiple>
        
        <!-- COLOR PANEL -->
        <v-expansion-panel value="color" title="Color" bg-color="grey-darken-4">
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
        <v-expansion-panel value="transform" title="Transform" bg-color="grey-darken-4">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label>Rotate</v-label>
              <v-slider v-model="controlState.rotate" :min="-180" :max="180" :step="0.1" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label>Translate X</v-label>
              <v-slider v-model="controlState.translateX" :min="-200" :max="200" :step="0.1" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label>Translate Y</v-label>
              <v-slider v-model="controlState.translateY" :min="-200" :max="200" :step="0.1" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label>Scale</v-label>
              <v-slider v-model="controlState.scale" :min="0.1" :max="3.0" :step="0.01" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label>Interpolation</v-label>
              <v-select v-model="controlState.scaleInterpolation" :items="['nearest', 'linear', 'cubic', 'area', 'lanczos']" variant="solo-filled" flat density="compact" class="mt-2"></v-select>
            </div>
            
            <v-divider class="my-4"></v-divider>

            <div class="control-group">
              <v-label class="text-subtitle-1 mb-2">Crop</v-label>
              <v-row dense>
                <v-col cols="6"><v-text-field v-model.number="controlState.crop.x" label="X" type="number" variant="solo-filled" flat density="compact" hide-details></v-text-field></v-col>
                <v-col cols="6"><v-text-field v-model.number="controlState.crop.y" label="Y" type="number" variant="solo-filled" flat density="compact" hide-details></v-text-field></v-col>
                <v-col cols="6" class="mt-2"><v-text-field v-model.number="controlState.crop.w" label="Width" type="number" variant="solo-filled" flat density="compact" hide-details></v-text-field></v-col>
                <v-col cols="6" class="mt-2"><v-text-field v-model.number="controlState.crop.h" label="Height" type="number" variant="solo-filled" flat density="compact" hide-details></v-text-field></v-col>
              </v-row>
            </div>

            <div class="control-group">
              <v-label class="mt-2">Aspect Lock</v-label>
              <v-select v-model="controlState.cropAspect" :items="['None', '1:1', '4:3', '16:9']" variant="solo-filled" flat density="compact" class="mt-2"></v-select>
            </div>

          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- FILTERS PANEL -->
        <v-expansion-panel value="filters" title="Filters" bg-color="grey-darken-4">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Blur Method</v-label>
              <v-select v-model="controlState.blur.method" :items="['gaussian', 'median', 'bilateral', 'box']" variant="solo-filled" flat density="compact" class="mt-2"></v-select>
            </div>
            <div class="control-group">
              <v-label>Kernel Size</v-label>
              <v-slider v-model="controlState.blur.ksize" :min="3" :max="31" :step="2" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <v-divider class="my-4"></v-divider>
            <div class="control-group">
              <v-label class="text-subtitle-1">Sharpen Strength</v-label>
              <v-slider v-model="controlState.sharpenStrength" :min="0" :max="2" :step="0.1" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- EDGES PANEL -->
        <v-expansion-panel value="edges" title="Edges" bg-color="grey-darken-4">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Edge Detection</v-label>
              <v-select v-model="controlState.edges.method" :items="['None', 'Canny', 'Sobel']" variant="solo-filled" flat density="compact" class="mt-2"></v-select>
            </div>
            <div v-if="controlState.edges.method === 'Canny'">
              <v-slider v-model="controlState.edges.canny_t1" :min="0" :max="255" label="T1" thumb-label color="primary" class="mt-2"></v-slider>
              <v-slider v-model="controlState.edges.canny_t2" :min="0" :max="255" label="T2" thumb-label color="primary" class="mt-2"></v-slider>
              <v-checkbox v-model="controlState.edges.link_canny_t2" label="Link T2 = 2 * T1"></v-checkbox>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

         <!-- DRAW PANEL -->
        <v-expansion-panel value="draw" title="Draw" bg-color="grey-darken-4">
            <v-expansion-panel-text>
                 <div class="d-flex ga-2 mb-4">
                    <v-btn @click="addDrawItem('rect')" size="small" variant="tonal">Rect</v-btn>
                    <v-btn @click="addDrawItem('circle')" size="small" variant="tonal">Circle</v-btn>
                    <v-btn @click="addDrawItem('line')" size="small" variant="tonal">Line</v-btn>
                    <v-btn @click="addDrawItem('text')" size="small" variant="tonal">Text</v-btn>
                </div>

                <v-card v-for="(item, index) in controlState.drawItems" :key="index" class="mb-4" color="grey-darken-3">
                    <v-card-title class="d-flex align-center text-subtitle-2 pa-2">
                        <span class="text-capitalize">{{ item.type }}</span>
                        <v-spacer></v-spacer>
                        <v-btn icon size="x-small" variant="text" @click="removeDrawItem(index)"><v-icon>mdi-close</v-icon></v-btn>
                    </v-card-title>
                    <v-card-text class="pa-2">
                        <!-- Rectangle Controls -->
                        <v-row v-if="item.type === 'rect'" dense>
                            <v-col><v-text-field v-model.number="item.xywh[0]" label="X" type="number" density="compact" hide-details></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[1]" label="Y" type="number" density="compact" hide-details></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[2]" label="W" type="number" density="compact" hide-details></v-text-field></v-col>
                            <v-col><v-text-field v-model.number="item.xywh[3]" label="H" type="number" density="compact" hide-details></v-text-field></v-col>
                        </v-row>
                         <!-- Text Controls -->
                        <div v-if="item.type === 'text'">
                            <v-text-field v-model="item.text" label="Text" density="compact" hide-details class="mb-2"></v-text-field>
                             <v-row dense>
                                <v-col><v-text-field v-model.number="item.xy[0]" label="X" type="number" density="compact" hide-details></v-text-field></v-col>
                                <v-col><v-text-field v-model.number="item.xy[1]" label="Y" type="number" density="compact" hide-details></v-text-field></v-col>
                                <v-col><v-text-field v-model.number="item.scale" label="Scale" type="number" step="0.1" density="compact" hide-details></v-text-field></v-col>
                            </v-row>
                        </div>
                         <!-- Shared Controls -->
                        <v-slider v-model="item.thickness" label="Thickness" :min="1" :max="10" thumb-label color="primary" class="mt-2"></v-slider>

                    </v-card-text>
                </v-card>
            </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- OPERATIONS PANEL -->
        <v-expansion-panel value="operations" title="Operations" bg-color="grey-darken-4">
          <v-expansion-panel-text>
            <div class="control-group">
              <v-label class="text-subtitle-1">Brightness</v-label>
              <v-slider v-model="controlState.brightness" :min="-100" :max="100" thumb-label color="primary" class="mt-2"></v-slider>
            </div>
            <div class="control-group">
              <v-label class="text-subtitle-1">Blend with Original</v-label>
              <v-slider v-model="controlState.blendAlpha" :min="0" :max="1" :step="0.01" label="Alpha" thumb-label color="primary" class="mt-2"></v-slider>
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


// By default, open the 'color' and 'transform' panels
const panel = ref(['color', 'transform', 'draw']);

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
</style>
