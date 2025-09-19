
<template>
  <v-sheet 
    elevation="0" 
    rounded="lg" 
    class="bg-black fill-height w-100 d-flex flex-column justify-center align-center pa-4 text-center"
  >
    <v-icon size="80" color="grey-lighten-1">mdi-image-plus-outline</v-icon>
    <h1 class="text-h4 font-weight-bold mt-6">Start Your Creation</h1>
    <p class="text-medium-emphasis mt-2">Upload an image to begin editing and see the magic happen.</p>
    <v-btn 
      variant="tonal" 
      color="primary" 
      class="mt-8" 
      @click="triggerUpload"
    >
      <v-icon left>mdi-camera-plus-outline</v-icon>
      Select Image
    </v-btn>
    <input type="file" ref="fileInput" @change="onFileSelected" accept="image/*" style="display: none;" />
  </v-sheet>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['file-uploaded']);
const fileInput = ref(null);

const triggerUpload = () => {
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const file = event.target.files[0];
  if (file) {
    emit('file-uploaded', file);
  }
};

// Expose the triggerUpload method to be called from the parent (App.vue)
defineExpose({
  triggerUpload,
});
</script>

<style scoped>
/* Add a subtle animation to the icon */
.v-icon {
  transition: transform 0.3s ease-in-out;
}

.v-sheet:hover .v-icon {
  transform: scale(1.1);
}
</style>
