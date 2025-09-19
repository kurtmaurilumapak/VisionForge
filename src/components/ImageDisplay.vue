
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
        <v-img :src="processedSrc" aspect-ratio="1" class="image-preview" contain></v-img>
      </div>
    </v-col>
  </v-row>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
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

.image-preview {
  border-radius: 8px;
  flex-grow: 1;
  min-height: 0; /* Important for flexbox sizing */
}

h3.text-overline {
  text-align: center;
  margin-bottom: 8px;
  color: #BDBDBD; /* Lighter grey for better visibility */
}
</style>
