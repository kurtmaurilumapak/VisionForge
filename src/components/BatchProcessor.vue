<template>
  <div class="fill-height w-100 d-flex flex-column pa-4">
    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-4">
      <h2 class="text-h5">Batch Processing</h2>
      <div class="d-flex ga-2">
        <v-btn 
          v-if="isProcessing"
          variant="outlined" 
          color="error" 
          @click="cancelProcessing"
        >
          <v-icon left>mdi-stop</v-icon>
          Cancel
        </v-btn>
        <v-btn 
          v-if="!hasProcessedImages"
          variant="tonal" 
          color="primary" 
          @click="startBatchProcessing"
          :disabled="!hasImages || isProcessing"
          :loading="isProcessing"
        >
          <v-icon left>mdi-play</v-icon>
          Process All
        </v-btn>
        
        <v-menu v-else>
          <template v-slot:activator="{ props }">
            <v-btn 
              v-bind="props"
              variant="tonal" 
              color="success"
            >
              <v-icon left>mdi-download</v-icon>
              Download Results
              <v-icon right>mdi-menu-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="downloadAll">
              <v-list-item-title>
                <v-icon left>mdi-download</v-icon>
                Download All Images
              </v-list-item-title>
            </v-list-item>
            <v-list-item @click="downloadAsZip">
              <v-list-item-title>
                <v-icon left>mdi-folder-zip</v-icon>
                Download as ZIP
              </v-list-item-title>
            </v-list-item>
            <v-list-item @click="exportBatchPDF">
              <v-list-item-title>
                <v-icon left>mdi-file-pdf-box</v-icon>
                Export as PDF Report
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>

    <!-- Image Grid -->
    <div class="image-grid flex-grow-1">
      <v-card 
        v-for="(image, index) in images" 
        :key="index"
        class="image-card"
        style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.12);"
      >
        <div class="image-preview">
          <img :src="image.preview" :alt="image.name" />
          <div class="image-overlay">
            <v-chip 
              :color="image.status === 'processed' ? 'success' : image.status === 'processing' ? 'warning' : 'default'"
              size="small"
            >
              {{ image.status === 'processed' ? 'Done' : image.status === 'processing' ? 'Processing...' : 'Pending' }}
            </v-chip>
          </div>
        </div>
        <v-card-title class="text-caption pa-2">
          {{ image.name }}
        </v-card-title>
      </v-card>
    </div>

    <!-- Progress Bar -->
    <v-progress-linear 
      v-if="isProcessing"
      :model-value="progress"
      color="primary"
      class="mt-4"
    ></v-progress-linear>

    <!-- Processing Status -->
    <div v-if="isProcessing" class="text-center mt-2">
      <span class="text-body-2">
        Processing {{ currentIndex + 1 }} of {{ images.length }} images
      </span>
    </div>


    <!-- Results Summary -->
    <v-alert 
      v-if="!isProcessing && hasProcessedImages"
      type="success" 
      variant="tonal" 
      class="mt-4"
    >
      <span>Batch processing completed! {{ processedCount }} images processed successfully.</span>
    </v-alert>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import apiService from '../services/api.js';
import jsPDF from 'jspdf';

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  controls: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['processing-complete']);

const isProcessing = ref(false);
const isCancelled = ref(false);
const currentIndex = ref(0);
const progress = ref(0);

const hasImages = computed(() => props.images.length > 0);
const hasProcessedImages = computed(() => props.images.some(img => img.status === 'processed'));
const processedCount = computed(() => props.images.filter(img => img.status === 'processed').length);

const startBatchProcessing = async () => {
  if (!hasImages.value) return;
  
  isProcessing.value = true;
  isCancelled.value = false;
  currentIndex.value = 0;
  progress.value = 0;
  
  // Reset all image statuses
  props.images.forEach(img => {
    img.status = 'pending';
    img.processedData = null;
  });
  
  try {
    for (let i = 0; i < props.images.length; i++) {
      // Check if processing was cancelled
      if (isCancelled.value) {
        console.log('Processing cancelled by user');
        break;
      }
      
      currentIndex.value = i;
      props.images[i].status = 'processing';
      
      try {
        const processedData = await processImage(props.images[i]);
        
        // Check again if cancelled during processing
        if (isCancelled.value) {
          console.log('Processing cancelled during image processing');
          break;
        }
        
        props.images[i].processedData = processedData;
        props.images[i].status = 'processed';
      } catch (error) {
        console.error(`Error processing image ${i + 1}:`, error);
        props.images[i].status = 'error';
      }
      
      progress.value = ((i + 1) / props.images.length) * 100;
    }
    
    if (!isCancelled.value) {
      emit('processing-complete', props.images);
    }
  } finally {
    isProcessing.value = false;
    isCancelled.value = false;
  }
};

const cancelProcessing = () => {
  isCancelled.value = true;
  isProcessing.value = false;
  console.log('Processing cancelled by user');
};

const processImage = async (imageData) => {
  try {
    console.log('Starting API call for image:', imageData.name);
    console.log('Controls being sent:', props.controls);
    
    // Add timeout to prevent hanging
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('API call timeout after 30 seconds')), 30000);
    });
    
    const apiPromise = apiService.processImageBase64(imageData.preview, props.controls);
    const response = await Promise.race([apiPromise, timeoutPromise]);
    
    console.log('API response received:', response);
    
    if (!response || !response.processed_image) {
      throw new Error('Invalid response from API: missing processed_image');
    }
    
    console.log('Image processed successfully:', imageData.name);
    return response.processed_image;
  } catch (error) {
    console.error('Error processing image:', imageData.name, error);
    throw error;
  }
};


const downloadAll = () => {
  const processedImages = props.images.filter(img => img.status === 'processed' && img.processedData);
  
  if (processedImages.length === 0) return;
  
  // Download individual files
  processedImages.forEach((image, index) => {
    const link = document.createElement('a');
    link.href = image.processedData;
    link.download = `processed_${image.name}`;
    link.click();
  });
};

const downloadAsZip = () => {
  // For now, just download all images individually
  // In a real implementation, you'd use a library like JSZip
  downloadAll();
  alert('ZIP download not implemented yet. Downloading individual files instead.');
};

const exportBatchPDF = async () => {
  if (!props.images.length) {
    console.log('No images to process');
    return;
  }
  
  const processedImages = props.images.filter(img => img.status === 'processed' && img.processedData);
  
  if (processedImages.length === 0) {
    alert('No processed images to export');
    return;
  }
  
  console.log('Starting PDF generation with', processedImages.length, 'images');
  console.log('Controls:', props.controls);
  
  try {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    const imgWidth = (pageWidth - 3 * margin) / 2; // 2 images per row
    const imgHeight = 80;
    const imagesPerRow = 2;
    const imagesPerPage = 6; // 3 rows per page
    
    // Header
    doc.setFontSize(22);
    doc.text('VisionForge Batch Processing Report', margin, 20);
    
    doc.setFontSize(12);
    doc.text(`Processed ${processedImages.length} images successfully`, margin, 30);
    doc.text(`Generated on: ${new Date().toLocaleDateString()}`, margin, 40);
    
    // Add controls information
    let currentY = 50;
    const controls = props.controls || {};
    const activeControls = [];
    
    try {
      // Check which controls are active (not at default values)
      if (controls.brightness !== undefined && controls.brightness !== 0) activeControls.push(`Brightness: ${controls.brightness}`);
      if (controls.contrast !== undefined && controls.contrast !== 0) activeControls.push(`Contrast: ${controls.contrast}`);
      if (controls.saturation !== undefined && controls.saturation !== 0) activeControls.push(`Saturation: ${controls.saturation}`);
      if (controls.hue !== undefined && controls.hue !== 0) activeControls.push(`Hue: ${controls.hue}`);
      
      // Blur (object with method and ksize) - only show if explicitly changed from default
      if (controls.blur && controls.blur.method && controls.blur.method !== 'gaussian' && controls.blur.method !== 'None') {
        activeControls.push(`Blur: ${controls.blur.method} (ksize: ${controls.blur.ksize})`);
      } else if (controls.blur && controls.blur.ksize && controls.blur.ksize !== 3) {
        activeControls.push(`Blur: ${controls.blur.method} (ksize: ${controls.blur.ksize})`);
      }
      
      if (controls.sharpen !== undefined && controls.sharpen !== 0) activeControls.push(`Sharpen: ${controls.sharpen}`);
      if (controls.noise !== undefined && controls.noise !== 0) activeControls.push(`Noise: ${controls.noise}`);
      if (controls.gamma !== undefined && controls.gamma !== 1) activeControls.push(`Gamma: ${controls.gamma}`);
      if (controls.exposure !== undefined && controls.exposure !== 0) activeControls.push(`Exposure: ${controls.exposure}`);
      if (controls.vibrance !== undefined && controls.vibrance !== 0) activeControls.push(`Vibrance: ${controls.vibrance}`);
      if (controls.temperature !== undefined && controls.temperature !== 0) activeControls.push(`Temperature: ${controls.temperature}`);
      if (controls.tint !== undefined && controls.tint !== 0) activeControls.push(`Tint: ${controls.tint}`);
      if (controls.shadows !== undefined && controls.shadows !== 0) activeControls.push(`Shadows: ${controls.shadows}`);
      if (controls.highlights !== undefined && controls.highlights !== 0) activeControls.push(`Highlights: ${controls.highlights}`);
      if (controls.whites !== undefined && controls.whites !== 0) activeControls.push(`Whites: ${controls.whites}`);
      if (controls.blacks !== undefined && controls.blacks !== 0) activeControls.push(`Blacks: ${controls.blacks}`);
      
      // Color Space
      if (controls.colorSpace && controls.colorSpace !== 'RGB') {
        activeControls.push(`Color Space: ${controls.colorSpace}`);
      }
      
      // Transform controls
      if (controls.rotate !== undefined && controls.rotate !== 0) activeControls.push(`Rotate: ${controls.rotate}°`);
      if (controls.scale !== undefined && controls.scale !== 1) activeControls.push(`Scale: ${controls.scale}x`);
      if (controls.translateX !== undefined && controls.translateX !== 0) activeControls.push(`Translate X: ${controls.translateX}`);
      if (controls.translateY !== undefined && controls.translateY !== 0) activeControls.push(`Translate Y: ${controls.translateY}`);
      
      // Edge detection - only show if explicitly enabled
      if (controls.edges && controls.edges.enabled && controls.edges.method && controls.edges.method !== 'None') {
        activeControls.push(`Edge Detection: ${controls.edges.method} (ksize: ${controls.edges.sobel_ksize || controls.edges.ksize})`);
      }
      
      // Adaptive threshold - only show if explicitly enabled
      if (controls.adaptiveThreshold && controls.adaptiveThreshold.enabled && controls.adaptiveThreshold.mode && controls.adaptiveThreshold.mode !== 'Simple') {
        activeControls.push(`Adaptive Threshold: ${controls.adaptiveThreshold.method} (blockSize: ${controls.adaptiveThreshold.blockSize}, C: ${controls.adaptiveThreshold.c})`);
      }
      
      // Morphology - only show if explicitly enabled
      if (controls.morphology && controls.morphology.enabled && controls.morphology.operation && controls.morphology.operation !== 'erode_dilate') {
        activeControls.push(`Morphology: ${controls.morphology.operation} (kernel: ${controls.morphology.kernelSize}x${controls.morphology.kernelSize}, iterations: ${controls.morphology.iterations})`);
      }
      
      // Color boost
      if (controls.colorBoost && (controls.colorBoost.saturation !== 0 || controls.colorBoost.hueShift !== 0 || controls.colorBoost.vibrance !== 1 || controls.colorBoost.contrast !== 0 || controls.colorBoost.brightness !== 0)) {
        const boostParts = [];
        if (controls.colorBoost.saturation !== 0) boostParts.push(`Saturation: ${controls.colorBoost.saturation}`);
        if (controls.colorBoost.hueShift !== 0) boostParts.push(`Hue: ${controls.colorBoost.hueShift}`);
        if (controls.colorBoost.vibrance !== 1) boostParts.push(`Vibrance: ${controls.colorBoost.vibrance}`);
        if (controls.colorBoost.contrast !== 0) boostParts.push(`Contrast: ${controls.colorBoost.contrast}`);
        if (controls.colorBoost.brightness !== 0) boostParts.push(`Brightness: ${controls.colorBoost.brightness}`);
        activeControls.push(`Color Boost: ${boostParts.join(', ')}`);
      }
      
      // Bitwise operations - only show if explicitly enabled
      if (controls.bitwise && controls.bitwise.enabled && controls.bitwise.operation && controls.bitwise.operation !== 'None') {
        activeControls.push(`Bitwise: ${controls.bitwise.operation}`);
      }
      
      // Crop - only show if explicitly enabled
      if (controls.crop && controls.crop.enabled && (controls.crop.x !== 0 || controls.crop.y !== 0 || controls.crop.w !== 0 || controls.crop.h !== 0)) {
        activeControls.push(`Crop: ${controls.crop.x}%, ${controls.crop.y}%, ${controls.crop.w}%, ${controls.crop.h}%`);
      }
      
      // Scale interpolation
      if (controls.scaleInterpolation && controls.scaleInterpolation !== 'linear') {
        activeControls.push(`Interpolation: ${controls.scaleInterpolation}`);
      }
      
      // Draw items
      if (controls.drawItems && controls.drawItems.length > 0) {
        activeControls.push(`Draw: ${controls.drawItems.length} items`);
      }
      
      // Grayscale
      if (controls.grayscaleAmount !== undefined && controls.grayscaleAmount !== 0) {
        // Convert from 0-1 range to 0-100% range
        const grayscalePercent = Math.round(controls.grayscaleAmount * 100);
        activeControls.push(`Grayscale: ${grayscalePercent}%`);
      }
    } catch (controlError) {
      console.error('Error processing controls:', controlError);
      activeControls.push('Error reading control settings');
    }
    
    if (activeControls.length > 0) {
      doc.setFontSize(10);
      doc.text('Applied Controls:', margin, currentY);
      currentY += 8;
      
      // Split controls into multiple lines if too long
      let line = '';
      activeControls.forEach((control, index) => {
        const testLine = line + (line ? ', ' : '') + control;
        if (doc.getTextWidth(testLine) > pageWidth - 2 * margin) {
          if (line) {
            doc.text(line, margin, currentY);
            currentY += 6;
            line = control;
          } else {
            // Single control is too long, split it
            doc.text(control, margin, currentY);
            currentY += 6;
          }
        } else {
          line = testLine;
        }
      });
      
      if (line) {
        doc.text(line, margin, currentY);
        currentY += 8;
      }
    } else {
      doc.setFontSize(10);
      doc.text('No controls applied (original images)', margin, currentY);
      currentY += 8;
    }
    
    currentY += 10; // Extra space before images
    
    let currentPage = 0;
    let imagesOnCurrentPage = 0;
    
    // Process images sequentially to avoid race conditions
    for (let i = 0; i < processedImages.length; i++) {
      const image = processedImages[i];
      
      // Check if we need a new page
      if (imagesOnCurrentPage >= imagesPerPage) {
        doc.addPage();
        currentPage++;
        currentY = 20;
        imagesOnCurrentPage = 0;
      }
      
      // Calculate position
      const row = Math.floor(imagesOnCurrentPage / imagesPerRow);
      const col = imagesOnCurrentPage % imagesPerRow;
      const x = margin + col * (imgWidth + margin);
      const y = currentY + row * (imgHeight + 30);
      
      try {
        console.log(`Processing image ${i + 1}/${processedImages.length}: ${image.name}`);
        
        // Validate image data
        if (!image.processedData || typeof image.processedData !== 'string') {
          throw new Error('Invalid image data');
        }
        
        // Load image and add to PDF
        await new Promise((resolve, reject) => {
          const img = new Image();
          img.crossOrigin = 'anonymous';
          
          // Add timeout for image loading
          const timeout = setTimeout(() => {
            reject(new Error(`Image load timeout: ${image.name}`));
          }, 10000);
          
          img.onload = () => {
            clearTimeout(timeout);
            try {
              console.log(`Adding image to PDF: ${image.name}`);
              
              // Add image
              doc.addImage(
                image.processedData, 
                'PNG', 
                x, 
                y, 
                imgWidth, 
                imgHeight
              );
              
              // Add image name
              doc.setFontSize(8);
              doc.text(image.name, x, y + imgHeight + 5);
              
              console.log(`Successfully added image: ${image.name}`);
              resolve();
            } catch (addImageError) {
              console.error(`Error adding image to PDF: ${image.name}`, addImageError);
              reject(addImageError);
            }
          };
          
          img.onerror = (imgError) => {
            clearTimeout(timeout);
            console.error(`Image load error for: ${image.name}`, imgError);
            reject(new Error(`Failed to load image: ${image.name}`));
          };
          
          img.src = image.processedData;
        });
        
        imagesOnCurrentPage++;
        
      } catch (error) {
        console.error(`Error processing image ${image.name}:`, error);
        // Add error text instead of image
        doc.setFontSize(8);
        doc.text(`Error loading: ${image.name}`, x, y + imgHeight / 2);
        imagesOnCurrentPage++;
      }
    }
    
    // Save the PDF
    console.log('Saving PDF...');
    const fileName = `visionforge_batch_report_${new Date().toISOString().split('T')[0]}.pdf`;
    
    try {
      doc.save(fileName);
      console.log('PDF saved successfully:', fileName);
    } catch (saveError) {
      console.error('Error saving PDF:', saveError);
      throw new Error(`Failed to save PDF: ${saveError.message}`);
    }
    
  } catch (error) {
    console.error('Error generating PDF:', error);
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    
    // Show more specific error message
    let errorMessage = 'Error generating PDF report. ';
    if (error.message.includes('timeout')) {
      errorMessage += 'One or more images took too long to load.';
    } else if (error.message.includes('Invalid image data')) {
      errorMessage += 'One or more images have invalid data.';
    } else if (error.message.includes('Failed to load image')) {
      errorMessage += 'One or more images failed to load.';
    } else {
      errorMessage += 'Please check the console for details and try again.';
    }
    
    alert(errorMessage);
  }
};


// Watch for control changes to reset processing status
watch(() => props.controls, () => {
  if (hasProcessedImages.value) {
    props.images.forEach(img => {
      if (img.status === 'processed') {
        img.status = 'pending';
        img.processedData = null;
      }
    });
  }
}, { deep: true });
</script>

<style scoped>
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  overflow-y: auto;
}

.image-card {
  height: fit-content;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 150px;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
}

.v-card-title {
  font-size: 0.75rem;
  line-height: 1.2;
  word-break: break-all;
}
</style>
