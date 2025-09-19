<template>
  <v-app :theme="'dark'" ref="appRef">
    <v-app-bar app color="black" elevation="0" style="border-bottom: 1px solid rgba(255, 255, 255, 0.12);">
      <v-app-bar-nav-icon v-if="!$vuetify.display.lgAndUp" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div class="d-flex align-center">
        <img src="/appicon.png" alt="VisionForge" style="height: 64px; width: auto;" />
        <v-toolbar-title class="font-weight-bold">VisionForge</v-toolbar-title>
      </div>
      <v-spacer></v-spacer>
      <v-btn 
        v-if="imageSrc || isBatchMode" 
        variant="tonal" 
        color="primary" 
        @click="triggerFileUpload"
      >
        <v-icon left>mdi-upload</v-icon>
        Upload New
      </v-btn>
      <v-btn 
        v-if="imageSrc && !isBatchMode"
        variant="text" 
        :color="exportButtonColor" 
        :disabled="!canExport"
        class="ml-2 export-button"
      >
        Export
        <v-icon right>mdi-menu-down</v-icon>
        <v-menu activator="parent" :disabled="!canExport">
          <v-list>
            <v-list-item @click="exportImage('png')" :disabled="!canExport">
              <v-list-item-title>Export as PNG</v-list-item-title>
            </v-list-item>
            <v-list-item @click="exportImage('jpg')" :disabled="!canExport">
              <v-list-item-title>Export as JPG</v-list-item-title>
            </v-list-item>
            <v-list-item @click="exportPDF" :disabled="!canExport">
              <v-list-item-title>Export as PDF Report</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-btn>
    </v-app-bar>

    <!-- Hidden file input for Upload New button -->
    <input 
      type="file" 
      ref="mainFileInput" 
      @change="onMainFileSelected" 
      accept="image/*" 
      multiple 
      style="display: none;" 
    />

    <v-navigation-drawer v-if="imageSrc || isBatchMode" app :permanent="$vuetify.display.lgAndUp" v-model="drawer" color="black" :width="400">
      <ControlPanel ref="controlPanel" :has-image="!!imageSrc" @user-interaction="markUserInteraction" @controls-reset="handleControlsReset" />
    </v-navigation-drawer>

    <v-main style="background-color: black;">
      <div class="fill-height d-flex justify-center align-center pa-4">
        <v-sheet color="black" class="fill-height w-100 d-flex" border rounded="lg">
            <FileUpload 
              v-if="!imageSrc && !isBatchMode" 
              @file-uploaded="onFileUploaded" 
              @batch-files-uploaded="onBatchFilesUploaded"
              ref="fileUpload" 
            />
            <BatchProcessor 
              v-else-if="isBatchMode" 
              :images="batchImages"
              :controls="controlState"
              @processing-complete="onBatchComplete"
            />
            <div v-else class="fill-height w-100 d-flex flex-column">
              <ImageDisplay 
                :original-src="imageSrc" 
                :processed-src="processedImageSrc"
                :crop-data="controlState.crop"
                :is-crop-active="false"
                @update:crop-data="updateCropData"
              />
              <v-overlay v-if="isProcessing" class="align-center justify-center">
                <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
                <div class="text-h6 mt-4">Processing image...</div>
              </v-overlay>
            </div>
        </v-sheet>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useDisplay } from 'vuetify';
import ControlPanel from './components/ControlPanel.vue';
import ImageDisplay from './components/ImageDisplay.vue';
import FileUpload from './components/FileUpload.vue';
import BatchProcessor from './components/BatchProcessor.vue';
import { useControls } from './composables/useControls.js';
import apiService from './services/api.js';
import jsPDF from 'jspdf';

const { controlState } = useControls();

const drawer = ref(useDisplay().lgAndUp.value);
const imageSrc = ref(null);
const processedImageSrc = ref(null);
const fileUpload = ref(null);
const mainFileInput = ref(null);
const batchImages = ref([]);
const isBatchMode = ref(false);
const controlPanel = ref(null);
const appRef = ref(null);
const isProcessing = ref(false);
const currentFile = ref(null);
const isCropActive = ref(false);
const hasUserInteracted = ref(false);
const resetTriggered = ref(0);

// Export button state
const canExport = computed(() => {
  const can = imageSrc.value && hasUserInteracted.value;
  console.log('canExport:', can, 'imageSrc:', !!imageSrc.value, 'hasUserInteracted:', hasUserInteracted.value);
  return can;
});

const exportButtonColor = computed(() => {
  if (!imageSrc.value) {
    console.log('Export button color: grey (no image)');
    return 'grey'; // Gray when no image
  } else if (!hasUserInteracted.value) {
    console.log('Export button color: grey (no controls)');
    return 'grey'; // Gray when no controls applied
  } else {
    console.log('Export button color: white (ready)');
    return 'white'; // White when ready to export
  }
});

const onFileUploaded = (file) => {
  if (file) {
    currentFile.value = file;
    hasUserInteracted.value = false; // Reset user interaction flag
    isBatchMode.value = false; // Switch to single image mode
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result;
      processedImageSrc.value = e.target.result; // Initially, processed = original
      // Reset controls after image is loaded
      setTimeout(() => {
        controlPanel.value?.resetAll();
      }, 100);
    };
    reader.readAsDataURL(file);
  }
};

const onBatchFilesUploaded = (files) => {
  if (files && files.length > 0) {
    batchImages.value = [];
    isBatchMode.value = true;
    hasUserInteracted.value = false; // Reset user interaction flag
    
    // Process files sequentially to ensure proper loading
    const processFiles = async () => {
      for (const file of files) {
        const imageData = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve({
            name: file.name,
            preview: e.target.result,
            status: 'pending',
            processedData: null
          });
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        batchImages.value.push(imageData);
      }
    };
    
    processFiles().then(() => {
      // Reset controls after all images are loaded
      setTimeout(() => {
        controlPanel.value?.resetAll();
      }, 100);
    });
  }
};

const triggerFileUpload = () => {
  mainFileInput.value?.click();
};

const onMainFileSelected = (event) => {
  const files = Array.from(event.target.files);
  if (files.length === 1) {
    // Single image selected
    onFileUploaded(files[0]);
  } else if (files.length > 1) {
    // Multiple images selected
    onBatchFilesUploaded(files);
  }
};

const onBatchComplete = (processedImages) => {
  console.log('Batch processing completed:', processedImages);
  // You can add additional logic here if needed
};

const switchToSingleMode = () => {
  isBatchMode.value = false;
  batchImages.value = [];
  imageSrc.value = null;
  processedImageSrc.value = null;
  hasUserInteracted.value = false;
};

// Watch for control changes and process image
watch(controlState, async () => {
  console.log('Control state changed:', controlState);
  console.log('Image src exists:', !!imageSrc.value);
  console.log('Current file exists:', !!currentFile.value);
  console.log('User has interacted:', hasUserInteracted.value);
  
  if (imageSrc.value && currentFile.value && hasUserInteracted.value) {
    console.log('Triggering image processing...');
    // Add a small delay to prevent too many rapid requests
    clearTimeout(processTimeout.value);
    processTimeout.value = setTimeout(async () => {
      await processImage();
    }, 300);
  }
}, { deep: true });

// Watch for reset (when all controls are at default values)
watch(controlState, () => {
  const isAtDefault = checkIfAtDefaultState();
  if (isAtDefault && hasUserInteracted.value) {
    console.log('Detected reset - controls are at default values');
    hasUserInteracted.value = false;
    if (imageSrc.value) {
      processedImageSrc.value = imageSrc.value;
    }
  }
}, { deep: true });

const processTimeout = ref(null);

const processImage = async () => {
  console.log('processImage called');
  if (!imageSrc.value || !currentFile.value) {
    console.log('Missing imageSrc or currentFile, returning');
    return;
  }
  
  // Check if all controls are at their default values
  const isAtDefaultState = checkIfAtDefaultState();
  console.log('Is at default state:', isAtDefaultState);
  if (isAtDefaultState) {
    console.log('Returning to original image - all controls at default');
    processedImageSrc.value = imageSrc.value; // Return to original
    return;
  }
  
  console.log('Processing image with current controls:', controlState);
  isProcessing.value = true;
  try {
    console.log('Calling API service...');
    const result = await apiService.processImage(imageSrc.value, controlState);
    console.log('API result:', result);
    if (result.success) {
      console.log('Setting processed image');
      processedImageSrc.value = result.processed_image;
    } else {
      console.log('API returned success: false');
    }
  } catch (error) {
    console.error('Error processing image:', error);
    // Fallback to original image if processing fails
    processedImageSrc.value = imageSrc.value;
  } finally {
    isProcessing.value = false;
  }
};

const checkIfAtDefaultState = () => {
  // Check if all controls are at their default values
  const defaults = {
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
    blendAlpha: 0
  };
  
  // Deep comparison of control state with defaults
  const isDefault = JSON.stringify(controlState) === JSON.stringify(defaults);
  console.log('Is at default state:', isDefault);
  if (!isDefault) {
    console.log('Current state:', JSON.stringify(controlState, null, 2));
    console.log('Default state:', JSON.stringify(defaults, null, 2));
  }
  return isDefault;
};

const updateCropData = (newCropData) => {
  controlState.crop = newCropData;
  hasUserInteracted.value = true; // Mark that user has interacted
};

const markUserInteraction = () => {
  console.log('User interaction detected, setting hasUserInteracted to true');
  hasUserInteracted.value = true;
};

const handleControlsReset = () => {
  console.log('Controls reset received, setting hasUserInteracted to false');
  hasUserInteracted.value = false;
  resetTriggered.value++;
  // Reset processed image to original
  if (imageSrc.value) {
    console.log('Resetting processed image to original');
    processedImageSrc.value = imageSrc.value;
  }
};

// Expose methods to global scope for direct access
window.parentApp = {
  handleControlsReset
};

// Watch for crop active state changes
watch(() => controlPanel.value?.isCropActive, (newValue) => {
  isCropActive.value = newValue;
});

// Watch for reset trigger to force reactivity
watch(resetTriggered, (newValue) => {
  console.log('Reset trigger changed:', newValue);
  console.log('hasUserInteracted after reset:', hasUserInteracted.value);
  console.log('canExport after reset:', canExport.value);
});

// Export functions
const exportImage = (format) => {
  if (!processedImageSrc.value) {
    alert('No image to export');
    return;
  }
  
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const img = new Image();
  
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    
    // Convert to desired format
    const mimeType = format === 'jpg' ? 'image/jpeg' : 'image/png';
    const quality = format === 'jpg' ? 0.9 : 1.0;
    
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `visionforge-export.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, mimeType, quality);
  };
  
  img.src = processedImageSrc.value;
};

const exportPDF = () => {
  if (!processedImageSrc.value) {
    alert('No image to export');
    return;
  }
  
  const img = new Image();
  img.onload = () => {
    const pdf = new jsPDF();
    const imgWidth = 190; // A4 width in mm
    const pageHeight = 295; // A4 height in mm
    const imgHeight = (img.height * imgWidth) / img.width;
    let heightLeft = imgHeight;
    
    let position = 10; // Top margin
    
    // Add title
    pdf.setFontSize(20);
    pdf.text('VisionForge Export Report', 20, position);
    position += 15;
    
    // Add timestamp
    pdf.setFontSize(12);
    pdf.text(`Generated: ${new Date().toLocaleString()}`, 20, position);
    position += 10;
    
    // Add image
    pdf.addImage(img, 'PNG', 10, position, imgWidth, imgHeight);
    
    // Add controls summary
    position += imgHeight + 10;
    if (position > pageHeight - 20) {
      pdf.addPage();
      position = 20;
    }
    
    pdf.setFontSize(14);
    pdf.text('Applied Controls:', 20, position);
    position += 10;
    
    pdf.setFontSize(10);
    const controls = getControlsSummary();
    controls.forEach(control => {
      if (position > pageHeight - 20) {
        pdf.addPage();
        position = 20;
      }
      pdf.text(control, 20, position);
      position += 5;
    });
    
    pdf.save('visionforge-report.pdf');
  };
  
  img.src = processedImageSrc.value;
};

const getControlsSummary = () => {
  const summary = [];
  
  // Color controls
  if (controlState.grayscaleAmount > 0) {
    summary.push(`Grayscale: ${(controlState.grayscaleAmount * 100).toFixed(1)}%`);
  }
  if (controlState.colorSpace !== 'RGB') {
    summary.push(`Color Space: ${controlState.colorSpace}`);
  }
  
  // Transform controls
  if (controlState.rotate !== 0) {
    summary.push(`Rotation: ${controlState.rotate.toFixed(1)}°`);
  }
  if (controlState.translateX !== 0 || controlState.translateY !== 0) {
    summary.push(`Translation: X=${controlState.translateX.toFixed(1)}, Y=${controlState.translateY.toFixed(1)}`);
  }
  if (controlState.scale !== 1) {
    summary.push(`Scale: ${controlState.scale.toFixed(2)}x (${controlState.scaleInterpolation})`);
  }
  if (controlState.crop.w > 0 && controlState.crop.h > 0) {
    summary.push(`Crop: ${controlState.crop.x.toFixed(1)}%, ${controlState.crop.y.toFixed(1)}%, ${controlState.crop.w.toFixed(1)}%, ${controlState.crop.h.toFixed(1)}%`);
  }
  
  // Filter controls
  if (controlState.blur.ksize > 3) {
    summary.push(`Blur: ${controlState.blur.method} (${controlState.blur.ksize}px)`);
  }
  if (controlState.sharpenStrength > 0) {
    summary.push(`Sharpen: ${controlState.sharpenStrength.toFixed(1)}`);
  }
  
  // Edge detection
  if (controlState.edges.method !== 'None') {
    summary.push(`Edge Detection: ${controlState.edges.method}`);
  }
  
  // Other controls
  if (controlState.brightness !== 0) {
    summary.push(`Brightness: ${controlState.brightness}`);
  }
  if (controlState.blendAlpha > 0) {
    summary.push(`Blend with Original: ${(controlState.blendAlpha * 100).toFixed(1)}%`);
  }
  
  return summary.length > 0 ? summary : ['No controls applied'];
};

</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  background-color: black;
}

.fill-height {
  height: 100%;
  width: 100%;
}

/* Remove padding from the navigation drawer to make the control panel seamless */
.v-navigation-drawer__content {
  padding: 0 !important;
}

/* Export button styling */
.export-button {
  color: white !important;
}

.export-button.v-btn--disabled {
  color: rgba(255, 255, 255, 0.38) !important;
}
</style>
