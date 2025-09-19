<template>
  <v-app :theme="'dark'">
    <v-app-bar app color="black" elevation="0" border>
      <v-app-bar-nav-icon v-if="!$vuetify.display.lgAndUp" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="font-weight-bold">VisionForge</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn variant="tonal" color="primary" @click="triggerFileUpload">
        <v-icon left>mdi-upload</v-icon>
        Upload New
      </v-btn>
      <v-btn variant="tonal" color="primary" class="ml-2">
        <v-icon left>mdi-download</v-icon>
        Export
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer app :permanent="$vuetify.display.lgAndUp" v-model="drawer" color="black" :width="400">
      <ControlPanel />
    </v-navigation-drawer>

    <v-main style="background-color: black;">
      <div class="fill-height d-flex justify-center align-center pa-4">
        <v-sheet color="black" class="fill-height w-100 d-flex" border rounded="lg">
            <FileUpload v-if="!imageSrc" @file-uploaded="onFileUploaded" ref="fileUpload" />
            <ImageDisplay v-else :original-src="imageSrc" :processed-src="processedImageSrc" />
        </v-sheet>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import { useDisplay } from 'vuetify';
import ControlPanel from './components/ControlPanel.vue';
import ImageDisplay from './components/ImageDisplay.vue';
import FileUpload from './components/FileUpload.vue';

const drawer = ref(useDisplay().lgAndUp.value);
const imageSrc = ref(null);
const processedImageSrc = ref(null);
const fileUpload = ref(null);

const onFileUploaded = (file) => {
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result;
      processedImageSrc.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const triggerFileUpload = () => {
  fileUpload.value?.triggerUpload();
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
</style>
