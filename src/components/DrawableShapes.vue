<template>
  <div class="drawable-shapes-container" ref="containerRef">
    <!-- Debug info -->
    <div style="position: absolute; top: 0; left: 0; background: red; color: white; padding: 4px; font-size: 12px; z-index: 9999;">
      Shapes: {{ drawItems.length }}
    </div>
    
    <div 
      v-for="(item, index) in drawItems" 
      v-show="imageRect.width > 0 && imageRect.height > 0"
      :key="index"
      class="drawable-shape"
      :class="[`shape-${item.type}`, { 'selected': selectedIndex === index }]"
      :style="getShapeStyle(item, index)"
      @mousedown="startDrag(index, $event)"
      @click="selectShape(index, $event)"
    >
      <!-- Shape content based on type -->
      <div v-if="item.type === 'rect'" class="shape-content">
        <div class="shape-handles">
          <div class="handle handle-nw" @mousedown.stop="startResize(index, 'nw', $event)"></div>
          <div class="handle handle-ne" @mousedown.stop="startResize(index, 'ne', $event)"></div>
          <div class="handle handle-sw" @mousedown.stop="startResize(index, 'sw', $event)"></div>
          <div class="handle handle-se" @mousedown.stop="startResize(index, 'se', $event)"></div>
        </div>
      </div>
      
      <div v-else-if="item.type === 'circle'" class="shape-content">
        <div class="shape-handles">
          <div class="handle handle-resize" @mousedown.stop="startResize(index, 'circle', $event)"></div>
        </div>
      </div>
      
      <div v-else-if="item.type === 'line'" class="shape-content">
        <div class="shape-handles">
          <div class="handle handle-start" @mousedown.stop="startResize(index, 'start', $event)"></div>
          <div class="handle handle-end" @mousedown.stop="startResize(index, 'end', $event)"></div>
        </div>
      </div>
      
      <div v-else-if="item.type === 'text'" class="shape-content">
        <div class="shape-handles">
          <div class="handle handle-move" @mousedown.stop="startResize(index, 'text', $event)"></div>
        </div>
        <div class="text-content">{{ item.text }}</div>
      </div>
      
      <!-- Color picker for selected shape -->
      <div v-if="selectedIndex === index" class="color-picker-overlay">
        <v-color-picker
          v-model="item.color"
          mode="hex"
          hide-mode-switch
          hide-inputs
          show-swatches
          class="shape-color-picker"
          @update:model-value="updateShapeColor(index, $event)"
        ></v-color-picker>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  drawItems: {
    type: Array,
    required: true
  },
  imageRect: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:drawItems', 'selectShape']);

const containerRef = ref(null);
const selectedIndex = ref(-1);
const isDragging = ref(false);
const isResizing = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const resizeType = ref('');
const currentIndex = ref(-1);

const isValidShape = (item) => {
  if (!item || !item.type) return false;
  
  switch (item.type) {
    case 'rect':
      const [x, y, w, h] = item.xywh || [];
      return Array.isArray(item.xywh) && item.xywh.length === 4 && 
             typeof x === 'number' && typeof y === 'number' && 
             typeof w === 'number' && typeof h === 'number' &&
             w > 0 && h > 0 && x >= 0 && y >= 0;
             
    case 'circle':
      const [cx, cy, r] = item.xyr || [];
      return Array.isArray(item.xyr) && item.xyr.length === 3 && 
             typeof cx === 'number' && typeof cy === 'number' && 
             typeof r === 'number' && r > 0 && cx >= 0 && cy >= 0;
             
    case 'line':
      const [x1, y1, x2, y2] = item.xyxy || [];
      return Array.isArray(item.xyxy) && item.xyxy.length === 4 && 
             typeof x1 === 'number' && typeof y1 === 'number' && 
             typeof x2 === 'number' && typeof y2 === 'number';
             
    case 'text':
      const [tx, ty] = item.xy || [];
      return Array.isArray(item.xy) && item.xy.length === 2 && 
             typeof tx === 'number' && typeof ty === 'number' &&
             tx >= 0 && ty >= 0 && item.text;
             
    default:
      return false;
  }
};

const getShapeStyle = (item, index) => {
  if (!props.imageRect.width || !props.imageRect.height) {
    console.log('Image rect not ready:', props.imageRect);
    return { display: 'none' };
  }
  
  // Validate shape coordinates before rendering
  if (!isValidShape(item)) {
    console.log(`Shape ${index} has invalid coordinates, hiding:`, item);
    return { display: 'none' };
  }
  
  const scaleX = props.imageRect.width / 100;
  const scaleY = props.imageRect.height / 100;
  
  console.log(`Shape ${index} (${item.type}):`, {
    item,
    imageRect: props.imageRect,
    scaleX,
    scaleY
  });
  
  // Log specific coordinates for debugging
  if (item.type === 'rect') {
    const [x, y, w, h] = item.xywh;
    console.log(`Rect coordinates: x=${x}, y=${y}, w=${w}, h=${h}`);
    console.log(`Calculated position: left=${x * scaleX}px, top=${y * scaleY}px, width=${w * scaleX}px, height=${h * scaleY}px`);
  }
  
  let style = {
    position: 'absolute',
    cursor: 'move',
    zIndex: selectedIndex.value === index ? 1000 : 10
  };
  
  switch (item.type) {
    case 'rect':
      const [x, y, w, h] = item.xywh;
      style.left = `${x * scaleX}px`;
      style.top = `${y * scaleY}px`;
      style.width = `${w * scaleX}px`;
      style.height = `${h * scaleY}px`;
      style.border = `2px solid ${item.color}`;
      style.backgroundColor = 'transparent';
      break;
      
    case 'circle':
      const [cx, cy, r] = item.xyr;
      style.left = `${(cx - r) * scaleX}px`;
      style.top = `${(cy - r) * scaleY}px`;
      style.width = `${r * 2 * scaleX}px`;
      style.height = `${r * 2 * scaleY}px`;
      style.borderRadius = '50%';
      style.border = `2px solid ${item.color}`;
      style.backgroundColor = 'transparent';
      break;
      
    case 'line':
      const [x1, y1, x2, y2] = item.xyxy;
      const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
      const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
      style.left = `${x1 * scaleX}px`;
      style.top = `${y1 * scaleY}px`;
      style.width = `${length * scaleX}px`;
      style.height = `${item.thickness}px`;
      style.transform = `rotate(${angle}deg)`;
      style.backgroundColor = item.color;
      break;
      
    case 'text':
      const [tx, ty] = item.xy;
      style.left = `${tx * scaleX}px`;
      style.top = `${ty * scaleY}px`;
      style.color = item.color;
      style.fontSize = `${item.scale * 16}px`;
      style.fontWeight = 'bold';
      style.pointerEvents = 'none';
      break;
  }
  
  return style;
};

const selectShape = (index, event) => {
  event.stopPropagation();
  selectedIndex.value = index;
  emit('selectShape', index);
};

const startDrag = (index, event) => {
  if (event.target.classList.contains('handle')) return;
  
  event.preventDefault();
  isDragging.value = true;
  currentIndex.value = index;
  dragStart.value = { x: event.clientX, y: event.clientY };
  
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', endDrag);
};

const onDrag = (event) => {
  if (!isDragging.value || currentIndex.value === -1) return;
  
  const deltaX = event.clientX - dragStart.value.x;
  const deltaY = event.clientY - dragStart.value.y;
  
  const scaleX = props.imageRect.width / 100;
  const scaleY = props.imageRect.height / 100;
  
  const deltaPercentX = (deltaX / scaleX);
  const deltaPercentY = (deltaY / scaleY);
  
  const item = props.drawItems[currentIndex.value];
  const newItems = [...props.drawItems];
  
  switch (item.type) {
    case 'rect':
      newItems[currentIndex.value] = {
        ...item,
        xywh: [
          Math.max(0, Math.min(100 - item.xywh[2], item.xywh[0] + deltaPercentX)),
          Math.max(0, Math.min(100 - item.xywh[3], item.xywh[1] + deltaPercentY)),
          item.xywh[2],
          item.xywh[3]
        ]
      };
      break;
      
    case 'circle':
      newItems[currentIndex.value] = {
        ...item,
        xyr: [
          Math.max(item.xyr[2], Math.min(100 - item.xyr[2], item.xyr[0] + deltaPercentX)),
          Math.max(item.xyr[2], Math.min(100 - item.xyr[2], item.xyr[1] + deltaPercentY)),
          item.xyr[2]
        ]
      };
      break;
      
    case 'line':
      newItems[currentIndex.value] = {
        ...item,
        xyxy: [
          Math.max(0, Math.min(100, item.xyxy[0] + deltaPercentX)),
          Math.max(0, Math.min(100, item.xyxy[1] + deltaPercentY)),
          Math.max(0, Math.min(100, item.xyxy[2] + deltaPercentX)),
          Math.max(0, Math.min(100, item.xyxy[3] + deltaPercentY))
        ]
      };
      break;
      
    case 'text':
      newItems[currentIndex.value] = {
        ...item,
        xy: [
          Math.max(0, Math.min(100, item.xy[0] + deltaPercentX)),
          Math.max(0, Math.min(100, item.xy[1] + deltaPercentY))
        ]
      };
      break;
  }
  
  emit('update:drawItems', newItems);
  dragStart.value = { x: event.clientX, y: event.clientY };
};

const startResize = (index, type, event) => {
  event.preventDefault();
  event.stopPropagation();
  
  isResizing.value = true;
  resizeType.value = type;
  currentIndex.value = index;
  dragStart.value = { x: event.clientX, y: event.clientY };
  
  document.addEventListener('mousemove', onResize);
  document.addEventListener('mouseup', endDrag);
};

const onResize = (event) => {
  if (!isResizing.value || currentIndex.value === -1) return;
  
  const deltaX = event.clientX - dragStart.value.x;
  const deltaY = event.clientY - dragStart.value.y;
  
  const scaleX = props.imageRect.width / 100;
  const scaleY = props.imageRect.height / 100;
  
  const deltaPercentX = (deltaX / scaleX);
  const deltaPercentY = (deltaY / scaleY);
  
  const item = props.drawItems[currentIndex.value];
  const newItems = [...props.drawItems];
  
  switch (resizeType.value) {
    case 'nw':
      newItems[currentIndex.value] = {
        ...item,
        xywh: [
          Math.max(0, item.xywh[0] + deltaPercentX),
          Math.max(0, item.xywh[1] + deltaPercentY),
          Math.max(10, item.xywh[2] - deltaPercentX),
          Math.max(10, item.xywh[3] - deltaPercentY)
        ]
      };
      break;
      
    case 'se':
      newItems[currentIndex.value] = {
        ...item,
        xywh: [
          item.xywh[0],
          item.xywh[1],
          Math.max(10, Math.min(100 - item.xywh[0], item.xywh[2] + deltaPercentX)),
          Math.max(10, Math.min(100 - item.xywh[1], item.xywh[3] + deltaPercentY))
        ]
      };
      break;
      
    case 'circle':
      const newRadius = Math.max(5, item.xyr[2] + deltaPercentX);
      newItems[currentIndex.value] = {
        ...item,
        xyr: [item.xyr[0], item.xyr[1], newRadius]
      };
      break;
      
    case 'start':
      newItems[currentIndex.value] = {
        ...item,
        xyxy: [
          Math.max(0, Math.min(100, item.xyxy[0] + deltaPercentX)),
          Math.max(0, Math.min(100, item.xyxy[1] + deltaPercentY)),
          item.xyxy[2],
          item.xyxy[3]
        ]
      };
      break;
      
    case 'end':
      newItems[currentIndex.value] = {
        ...item,
        xyxy: [
          item.xyxy[0],
          item.xyxy[1],
          Math.max(0, Math.min(100, item.xyxy[2] + deltaPercentX)),
          Math.max(0, Math.min(100, item.xyxy[3] + deltaPercentY))
        ]
      };
      break;
  }
  
  emit('update:drawItems', newItems);
  dragStart.value = { x: event.clientX, y: event.clientY };
};

const endDrag = () => {
  isDragging.value = false;
  isResizing.value = false;
  currentIndex.value = -1;
  resizeType.value = '';
  
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mousemove', onResize);
  document.removeEventListener('mouseup', endDrag);
};

const updateShapeColor = (index, color) => {
  const newItems = [...props.drawItems];
  newItems[index] = { ...newItems[index], color };
  emit('update:drawItems', newItems);
};

onMounted(() => {
  // Debug: Log all draw items
  console.log('All draw items on mount:', props.drawItems);
  console.log('Number of draw items:', props.drawItems.length);
  
  // Clean up invalid shapes on mount
  const validItems = props.drawItems.filter(isValidShape);
  if (validItems.length !== props.drawItems.length) {
    console.log('Cleaning up invalid shapes:', props.drawItems.length - validItems.length);
    emit('update:drawItems', validItems);
  }
  
  // Add click outside to deselect
  document.addEventListener('click', (event) => {
    if (!containerRef.value?.contains(event.target)) {
      selectedIndex.value = -1;
    }
  });
});

onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mousemove', onResize);
  document.removeEventListener('mouseup', endDrag);
});
</script>

<style scoped>
.drawable-shapes-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
}

.drawable-shape {
  pointer-events: all;
  position: relative;
}

.drawable-shape.selected {
  z-index: 1000;
}

.shape-content {
  width: 100%;
  height: 100%;
  position: relative;
}

.shape-handles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #2196F3;
  border: 2px solid white;
  border-radius: 50%;
  pointer-events: all;
  cursor: pointer;
}

.handle-nw {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.handle-ne {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.handle-sw {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.handle-se {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.handle-resize {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.handle-start {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.handle-end {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.handle-move {
  top: -4px;
  left: -4px;
  cursor: move;
}

.text-content {
  pointer-events: none;
  white-space: nowrap;
  user-select: none;
}

.color-picker-overlay {
  position: absolute;
  top: -200px;
  left: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 1001;
}

.shape-color-picker {
  width: 200px;
  height: 150px;
}
</style>
