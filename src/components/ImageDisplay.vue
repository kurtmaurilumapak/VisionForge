
<template>
  <v-row class="fill-height ma-0">
    <!-- Original Image -->
    <v-col cols="12" md="6" class="pa-2">
      <div class="image-container">
        <h3 class="text-overline">Original</h3>
        <ImageCrop 
          :image-src="originalSrc" 
          :crop-data="cropData"
          :is-active="isCropActive"
          @update:crop-data="updateCropData"
        />
      </div>
    </v-col>

    <!-- Processed Image -->
    <v-col cols="12" md="6" class="pa-2">
      <div class="image-container">
        <h3 class="text-overline">Processed</h3>
        <div class="image-preview-container">
          <v-img :src="processedSrc" aspect-ratio="1" class="image-preview" contain></v-img>
          <div v-if="isLoading" class="image-loading-overlay">
            <div class="d-flex flex-column align-center justify-center h-100">
              <div class="text-h6 mb-4 text-white">PROCESSING</div>
              <v-progress-circular indeterminate size="48" color="primary"></v-progress-circular>
            </div>
          </div>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script setup>
import { defineProps, defineEmits, computed, ref, watch } from 'vue';
import ImageCrop from './ImageCrop.vue';

const props = defineProps({
  originalSrc: {
    type: String,
    required: true,
  },
  processedSrc: {
    type: String,
    required: true,
  },
  cropData: {
    type: Object,
    required: true,
  },
  isCropActive: {
    type: Boolean,
    default: false,
  },
  isLoading: {
    type: Boolean,
    default: false,
  }
});

const emit = defineEmits(['update:cropData']);

const updateCropData = (newCropData) => {
  emit('update:cropData', newCropData);
};

</script>

<style scoped>
.image-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.image-preview-container {
  position: relative;
  flex-grow: 1;
  min-height: 0; /* Important for flexbox sizing */
}

.image-preview {
  border-radius: 8px;
  width: 100%;
  height: 100%;
}

.image-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  z-index: 10;
}

h3.text-overline {
  text-align: center;
  margin-bottom: 8px;
  color: #BDBDBD; /* Lighter grey for better visibility */
}

</style>
