
<template>
  <v-sheet 
    elevation="0" 
    rounded="lg" 
    class="bg-black fill-height w-100 d-flex flex-column justify-center align-center pa-4 text-center"
  >
    <v-icon size="80" color="grey-lighten-1">mdi-image-plus-outline</v-icon>
    <h1 class="text-h4 font-weight-bold mt-6">Start Your Creation</h1>
    <p class="text-medium-emphasis mt-2">Upload images to begin editing and see the magic happen.</p>
    <div class="mt-8">
      <v-btn 
        variant="tonal" 
        color="primary"
        size="large"
        @click="triggerUpload"
      >
        <v-icon left>mdi-upload</v-icon>
        Upload Image
      </v-btn>
    </div>
    <input type="file" ref="fileInput" @change="onFileSelected" accept="image/*" multiple style="display: none;" />
  </v-sheet>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['file-uploaded', 'batch-files-uploaded']);
const fileInput = ref(null);

const triggerUpload = () => {
  fileInput.value?.click();
};

const onFileSelected = (event) => {
  const files = Array.from(event.target.files);
  if (files.length === 1) {
    // Single image selected
    emit('file-uploaded', files[0]);
  } else if (files.length > 1) {
    // Multiple images selected
    emit('batch-files-uploaded', files);
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
