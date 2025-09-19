<template>
  <div class="image-crop-container original-image-crop" ref="cropContainer" @click="onContainerClick">
    <div class="crop-overlay" v-if="isActive" data-crop-overlay="original">
      <div 
        class="crop-box" 
        :style="cropBoxStyle"
        @mousedown="startDrag"
        @mousemove="onDrag"
        @mouseup="endDrag"
        @mouseleave="endDrag"
        @click.stop
      >
        <div class="crop-handle crop-handle-nw" @mousedown="startResize('nw', $event)"></div>
        <div class="crop-handle crop-handle-ne" @mousedown="startResize('ne', $event)"></div>
        <div class="crop-handle crop-handle-sw" @mousedown="startResize('sw', $event)"></div>
        <div class="crop-handle crop-handle-se" @mousedown="startResize('se', $event)"></div>
        <div class="crop-handle crop-handle-n" @mousedown="startResize('n', $event)"></div>
        <div class="crop-handle crop-handle-s" @mousedown="startResize('s', $event)"></div>
        <div class="crop-handle crop-handle-w" @mousedown="startResize('w', $event)"></div>
        <div class="crop-handle crop-handle-e" @mousedown="startResize('e', $event)"></div>
      </div>
    </div>
    <v-img 
      :src="imageSrc" 
      aspect-ratio="1" 
      class="image-preview" 
      contain
      @load="onImageLoad"
      @click="onImageClick"
      @mousedown="preventImageDrag"
      @dragstart="preventImageDrag"
      draggable="false"
    ></v-img>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  imageSrc: {
    type: String,
    required: true
  },
  cropData: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:cropData']);


const cropContainer = ref(null);
const imageElement = ref(null);
const containerRect = ref({ width: 0, height: 0, left: 0, top: 0 });
const imageRect = ref({ width: 0, height: 0, left: 0, top: 0 });
const isDragging = ref(false);
const isResizing = ref(false);
const resizeHandle = ref(null);
const dragStart = ref({ x: 0, y: 0 });
const dragTimeout = ref(null);
const lastMousePosition = ref({ x: 0, y: 0 });
const isMouseDown = ref(false);
const lastUpdateTime = ref(0);
const updateThrottle = 16; // ~60fps

const cropBoxStyle = computed(() => {
  if (!imageRect.value.width || !imageRect.value.height) {
    return { display: 'none' };
  }
  
  const x = (props.cropData.x / 100) * imageRect.value.width + imageRect.value.left;
  const y = (props.cropData.y / 100) * imageRect.value.height + imageRect.value.top;
  const w = (props.cropData.w / 100) * imageRect.value.width;
  const h = (props.cropData.h / 100) * imageRect.value.height;
  
  return {
    left: `${x}px`,
    top: `${y}px`,
    width: `${w}px`,
    height: `${h}px`
  };
});

const onImageLoad = (event) => {
  updateImageRect();
};

const updateImageRect = () => {
  if (cropContainer.value) {
    const container = cropContainer.value;
    const img = container.querySelector('.v-img__img');
    
    if (img) {
      const rect = img.getBoundingClientRect();
      const containerRect = container.getBoundingClientRect();
      
      const newImageRect = {
        left: rect.left - containerRect.left,
        top: rect.top - containerRect.top,
        width: rect.width,
        height: rect.height
      };
      
      imageRect.value = newImageRect;
    }
  }
};

const preventImageDrag = (event) => {
  event.preventDefault();
  event.stopPropagation();
};

const onContainerClick = (event) => {
  if (!props.isActive) return;
  
  // Only create crop if clicking on the image area, not on crop box
  if (event.target.classList.contains('crop-box') || event.target.classList.contains('crop-handle')) {
    return;
  }
  
  updateImageRect(); // Ensure we have the latest image rect
  
  const rect = imageRect.value;
  const containerRect = cropContainer.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
    const newCrop = {
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      w: 40, // Default width - larger initial size
      h: 40  // Default height - larger initial size
    };
    
    emit('update:cropData', newCrop);
  }
};

const onImageClick = (event) => {
  // This is now handled by onContainerClick
  event.preventDefault();
  event.stopPropagation();
};

const startDrag = (event) => {
  if (!props.isActive) return;
  event.preventDefault();
  event.stopPropagation();
  
  isDragging.value = true;
  isMouseDown.value = true;
  dragStart.value = { x: event.clientX, y: event.clientY };
  lastMousePosition.value = { x: event.clientX, y: event.clientY };
  
  // Set a timeout to automatically end dragging if it gets stuck
  if (dragTimeout.value) {
    clearTimeout(dragTimeout.value);
  }
  dragTimeout.value = setTimeout(() => {
    endDrag();
  }, 10000); // 10 second timeout
};

const onDrag = (event) => {
  if (!isDragging.value || !props.isActive || !isMouseDown.value) return;
  
  const now = Date.now();
  if (now - lastUpdateTime.value < updateThrottle) return;
  lastUpdateTime.value = now;
  
  updateImageRect(); // Ensure we have the latest image rect
  const rect = imageRect.value;
  
  // Calculate delta from last position instead of start position for smoother tracking
  const deltaX = event.clientX - lastMousePosition.value.x;
  const deltaY = event.clientY - lastMousePosition.value.y;
  
  const newX = Math.max(0, Math.min(100, props.cropData.x + (deltaX / rect.width) * 100));
  const newY = Math.max(0, Math.min(100, props.cropData.y + (deltaY / rect.height) * 100));
  
  // Round to 1 decimal place
  const roundedX = Math.round(newX * 10) / 10;
  const roundedY = Math.round(newY * 10) / 10;
  
  emit('update:cropData', {
    ...props.cropData,
    x: roundedX,
    y: roundedY
  });
  
  // Update last position for next move
  lastMousePosition.value = { x: event.clientX, y: event.clientY };
};

const endDrag = () => {
  isDragging.value = false;
  isResizing.value = false;
  isMouseDown.value = false;
  resizeHandle.value = null;
  dragStart.value = { x: 0, y: 0 };
  lastMousePosition.value = { x: 0, y: 0 };
  
  // Clear any pending timeout
  if (dragTimeout.value) {
    clearTimeout(dragTimeout.value);
    dragTimeout.value = null;
  }
};

const startResize = (handle, event) => {
  if (!props.isActive) return;
  event.preventDefault();
  event.stopPropagation();
  
  isResizing.value = true;
  isMouseDown.value = true;
  resizeHandle.value = { 
    handle: handle, 
    initialCrop: { ...props.cropData } 
  };
  dragStart.value = { x: event.clientX, y: event.clientY };
  lastMousePosition.value = { x: event.clientX, y: event.clientY };
  
  // Set a timeout to automatically end resizing if it gets stuck
  if (dragTimeout.value) {
    clearTimeout(dragTimeout.value);
  }
  dragTimeout.value = setTimeout(() => {
    endDrag();
  }, 10000); // 10 second timeout
};

const handleResize = (event) => {
  if (!isResizing.value || !props.isActive || !isMouseDown.value) return;
  
  const now = Date.now();
  if (now - lastUpdateTime.value < updateThrottle) return;
  lastUpdateTime.value = now;
  
  updateImageRect(); // Ensure we have the latest image rect
  const rect = imageRect.value;
  
  // Use absolute position calculation for resize to prevent getting stuck
  const deltaX = event.clientX - dragStart.value.x;
  const deltaY = event.clientY - dragStart.value.y;
  
  let newCrop = { ...props.cropData };
  
  // Store initial crop values at start of resize
  if (!resizeHandle.value.initialCrop) {
    resizeHandle.value.initialCrop = { ...props.cropData };
  }
  
  const initialCrop = resizeHandle.value.initialCrop;
  
  switch (resizeHandle.value.handle) {
    case 'nw':
      newCrop.x = Math.max(0, Math.min(100, initialCrop.x + (deltaX / rect.width) * 100));
      newCrop.y = Math.max(0, Math.min(100, initialCrop.y + (deltaY / rect.height) * 100));
      newCrop.w = Math.max(1, initialCrop.w - (deltaX / rect.width) * 100);
      newCrop.h = Math.max(1, initialCrop.h - (deltaY / rect.height) * 100);
      break;
    case 'ne':
      newCrop.y = Math.max(0, Math.min(100, initialCrop.y + (deltaY / rect.height) * 100));
      newCrop.w = Math.max(1, initialCrop.w + (deltaX / rect.width) * 100);
      newCrop.h = Math.max(1, initialCrop.h - (deltaY / rect.height) * 100);
      break;
    case 'sw':
      newCrop.x = Math.max(0, Math.min(100, initialCrop.x + (deltaX / rect.width) * 100));
      newCrop.w = Math.max(1, initialCrop.w - (deltaX / rect.width) * 100);
      newCrop.h = Math.max(1, initialCrop.h + (deltaY / rect.height) * 100);
      break;
    case 'se':
      newCrop.w = Math.max(1, initialCrop.w + (deltaX / rect.width) * 100);
      newCrop.h = Math.max(1, initialCrop.h + (deltaY / rect.height) * 100);
      break;
    case 'n':
      newCrop.y = Math.max(0, Math.min(100, initialCrop.y + (deltaY / rect.height) * 100));
      newCrop.h = Math.max(1, initialCrop.h - (deltaY / rect.height) * 100);
      break;
    case 's':
      newCrop.h = Math.max(1, initialCrop.h + (deltaY / rect.height) * 100);
      break;
    case 'w':
      newCrop.x = Math.max(0, Math.min(100, initialCrop.x + (deltaX / rect.width) * 100));
      newCrop.w = Math.max(1, initialCrop.w - (deltaX / rect.width) * 100);
      break;
    case 'e':
      newCrop.w = Math.max(1, initialCrop.w + (deltaX / rect.width) * 100);
      break;
  }
  
  // Ensure crop stays within bounds
  if (newCrop.x + newCrop.w > 100) newCrop.w = 100 - newCrop.x;
  if (newCrop.y + newCrop.h > 100) newCrop.h = 100 - newCrop.y;
  
  // Round to 1 decimal place
  newCrop.x = Math.round(newCrop.x * 10) / 10;
  newCrop.y = Math.round(newCrop.y * 10) / 10;
  newCrop.w = Math.round(newCrop.w * 10) / 10;
  newCrop.h = Math.round(newCrop.h * 10) / 10;
  
  emit('update:cropData', newCrop);
};

const handleMouseMove = (event) => {
  // Check if mouse button is still pressed (buttons: 1 = left button)
  if (event.buttons !== 1) {
    if (isDragging.value || isResizing.value) {
      endDrag();
    }
    return;
  }
  
  if (isDragging.value) {
    onDrag(event);
  } else if (isResizing.value) {
    handleResize(event);
  }
};

const handleMouseUp = (event) => {
  if (isDragging.value || isResizing.value) {
    endDrag();
  }
};

const handleMouseLeave = (event) => {
  if (isDragging.value || isResizing.value) {
    endDrag();
  }
};

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove);
  window.addEventListener('mouseup', handleMouseUp);
  window.addEventListener('mouseleave', handleMouseLeave);
  window.addEventListener('resize', updateImageRect);
});

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove);
  window.removeEventListener('mouseup', handleMouseUp);
  window.removeEventListener('mouseleave', handleMouseLeave);
  window.removeEventListener('resize', updateImageRect);
  
  // Clear any pending timeout
  if (dragTimeout.value) {
    clearTimeout(dragTimeout.value);
    dragTimeout.value = null;
  }
});

watch(() => props.imageSrc, () => {
  setTimeout(updateImageRect, 100);
});
</script>

<style scoped>
.image-crop-container {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: crosshair;
  user-select: none;
  overflow: hidden;
  isolation: isolate;
}

.original-image-crop .crop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: auto;
  z-index: 1000;
  contain: layout style paint;
}

.image-preview {
  width: 100%;
  height: 100%;
  pointer-events: none;
  user-select: none;
  -webkit-user-drag: none;
  -khtml-user-drag: none;
  -moz-user-drag: none;
  -o-user-drag: none;
  user-drag: none;
}

.crop-box {
  position: absolute;
  border: 2px solid #2196F3;
  background: rgba(33, 150, 243, 0.1);
  pointer-events: all;
  cursor: move;
  z-index: 10;
  box-sizing: border-box;
  user-select: none;
}

.crop-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #2196F3;
  border: 1px solid white;
  border-radius: 50%;
  pointer-events: all;
}

.crop-handle-nw {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.crop-handle-ne {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.crop-handle-sw {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.crop-handle-se {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.crop-handle-n {
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  cursor: n-resize;
}

.crop-handle-s {
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  cursor: s-resize;
}

.crop-handle-w {
  top: 50%;
  left: -4px;
  transform: translateY(-50%);
  cursor: w-resize;
}

.crop-handle-e {
  top: 50%;
  right: -4px;
  transform: translateY(-50%);
  cursor: e-resize;
}
</style>
