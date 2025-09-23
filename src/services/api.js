const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async processImage(imageData, controls) {
    try {
      const formData = new FormData();
      
      // If imageData is a File object
      if (imageData instanceof File) {
        formData.append('image', imageData);
      } else {
        // If it's a base64 string
        formData.append('image_data', imageData);
      }
      
      formData.append('controls', JSON.stringify(controls));

      const response = await fetch(`${this.baseURL}/process-image-base64`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error processing image:', error);
      throw error;
    }
  }

  async processImageBase64(imageData, controls) {
    try {
      const formData = new FormData();
      formData.append('image_data', imageData);
      formData.append('controls', JSON.stringify(controls));

      const response = await fetch(`${this.baseURL}/process-image-base64`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error processing image base64:', error);
      throw error;
    }
  }

  async uploadImage(file) {
    try {
      const formData = new FormData();
      formData.append('image', file);
      formData.append('controls', JSON.stringify({})); // Empty controls for initial upload

      const response = await fetch(`${this.baseURL}/process-image`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  async zipImages(files) {
    try {
      const response = await fetch(`${this.baseURL}/zip-images`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ files })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      return blob;
    } catch (error) {
      console.error('Error creating ZIP:', error);
      throw error;
    }
  }
}

export default new ApiService();



