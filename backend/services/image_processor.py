import cv2
import numpy as np
from typing import Dict, Any, Optional, Tuple
import math

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
    
    def process_image(self, image: np.ndarray, controls: Dict[str, Any]) -> np.ndarray:
        """
        Main image processing function that applies all controls
        """
        self.original_image = image.copy()
        self.processed_image = image.copy()
        
        # Apply transformations in order
        self._apply_color_operations(controls)
        self._apply_transform_operations(controls)
        self._apply_filter_operations(controls)
        self._apply_edge_operations(controls)
        self._apply_bitwise_operations(controls)
        self._apply_adaptive_threshold(controls)
        self._apply_morphology_operations(controls)
        self._apply_color_boost(controls)
        self._apply_draw_operations(controls)
        self._apply_final_operations(controls)
        
        return self.processed_image
    
    def _apply_color_operations(self, controls: Dict[str, Any]):
        """Apply color space and grayscale operations"""
        if controls.get('grayscaleAmount', 0) > 0:
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            alpha = controls['grayscaleAmount']
            self.processed_image = cv2.addWeighted(self.processed_image, 1-alpha, gray, alpha, 0)
        
        # Color space conversion
        color_space = controls.get('colorSpace', 'RGB')
        if color_space != 'RGB':
            if color_space == 'HSV':
                self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2HSV)
            elif color_space == 'LAB':
                self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2LAB)
            elif color_space == 'YCrCb':
                self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2YCrCb)
    
    def _apply_transform_operations(self, controls: Dict[str, Any]):
        """Apply rotation, translation, scaling, and cropping"""
        h, w = self.processed_image.shape[:2]
        
        # Rotation
        if controls.get('rotate', 0) != 0:
            angle = controls['rotate']
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.processed_image = cv2.warpAffine(self.processed_image, M, (w, h))
        
        # Translation
        tx = controls.get('translateX', 0)
        ty = controls.get('translateY', 0)
        if tx != 0 or ty != 0:
            M = np.float32([[1, 0, tx], [0, 1, ty]])
            self.processed_image = cv2.warpAffine(self.processed_image, M, (w, h))
        
        # Scaling
        scale = controls.get('scale', 1.0)
        if scale != 1.0:
            interpolation_method = controls.get('scaleInterpolation', 'linear')
            interpolation = self._get_interpolation_method(interpolation_method)
            new_w = int(w * scale)
            new_h = int(h * scale)
            print(f"Scaling with {interpolation_method} interpolation: {scale}x from {w}x{h} to {new_w}x{new_h}")
            self.processed_image = cv2.resize(self.processed_image, (new_w, new_h), interpolation=interpolation)
        
        # Cropping
        crop = controls.get('crop', {})
        if crop and isinstance(crop, dict):
            crop_w = crop.get('w', 0)
            crop_h = crop.get('h', 0)
            crop_x = crop.get('x', 0)
            crop_y = crop.get('y', 0)
            
            # Only apply crop if we have valid dimensions
            if crop_w > 0 and crop_h > 0 and crop_x >= 0 and crop_y >= 0:
                img_h, img_w = self.processed_image.shape[:2]
                
                # Convert percentage to pixel coordinates
                x = int((crop_x / 100) * img_w)
                y = int((crop_y / 100) * img_h)
                w = int((crop_w / 100) * img_w)
                h = int((crop_h / 100) * img_h)
                
                # Ensure crop coordinates are within image bounds
                x = max(0, min(x, img_w - 1))
                y = max(0, min(y, img_h - 1))
                w = min(w, img_w - x)
                h = min(h, img_h - y)
                
                # Only crop if we have valid dimensions
                if w > 0 and h > 0 and x < img_w and y < img_h:
                    self.processed_image = self.processed_image[y:y+h, x:x+w]
    
    def _apply_filter_operations(self, controls: Dict[str, Any]):
        """Apply blur and sharpen filters"""
        # Blur
        blur_data = controls.get('blur', {})
        if blur_data.get('ksize', 3) > 3:
            method = blur_data.get('method', 'gaussian')
            ksize = blur_data.get('ksize', 3)
            
            if method == 'gaussian':
                self.processed_image = cv2.GaussianBlur(self.processed_image, (ksize, ksize), 0)
            elif method == 'median':
                self.processed_image = cv2.medianBlur(self.processed_image, ksize)
            elif method == 'bilateral':
                self.processed_image = cv2.bilateralFilter(self.processed_image, ksize, 80, 80)
            elif method == 'box':
                self.processed_image = cv2.boxFilter(self.processed_image, -1, (ksize, ksize))
        
        # Sharpen
        sharpen_strength = controls.get('sharpenStrength', 0)
        if sharpen_strength > 0:
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * sharpen_strength
            kernel[1,1] = kernel[1,1] + 1
            self.processed_image = cv2.filter2D(self.processed_image, -1, kernel)
    
    def _apply_edge_operations(self, controls: Dict[str, Any]):
        """Apply edge detection operations"""
        edges_data = controls.get('edges', {})
        method = edges_data.get('method', 'None')
        
        if method == 'Canny':
            t1 = edges_data.get('canny_t1', 50)
            t2 = edges_data.get('canny_t2', 100)
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, t1, t2)
            self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        elif method == 'Sobel':
            ksize = edges_data.get('sobel_ksize', 3)
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            sobel = np.sqrt(sobelx**2 + sobely**2)
            sobel = np.uint8(sobel / sobel.max() * 255)
            self.processed_image = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
    
    def _apply_bitwise_operations(self, controls: Dict[str, Any]):
        """Apply bitwise operations"""
        bitwise_data = controls.get('bitwise', {})
        operation = bitwise_data.get('operation', 'None')
        
        if operation != 'None':
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            threshold = bitwise_data.get('maskThreshold', 128)
            _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            
            if operation == 'NOT':
                result = cv2.bitwise_not(self.processed_image)
            elif operation == 'AND':
                result = cv2.bitwise_and(self.processed_image, self.processed_image, mask=mask)
            elif operation == 'OR':
                result = cv2.bitwise_or(self.processed_image, self.processed_image, mask=mask)
            elif operation == 'XOR':
                result = cv2.bitwise_xor(self.processed_image, self.processed_image, mask=mask)
            else:
                return
            
            self.processed_image = result
    
    def _apply_adaptive_threshold(self, controls: Dict[str, Any]):
        """Apply adaptive thresholding"""
        adaptive_data = controls.get('adaptiveThreshold', {})
        mode = adaptive_data.get('mode', 'Simple')
        
        if mode == 'Adaptive':
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            method = adaptive_data.get('method', 'mean')
            block_size = adaptive_data.get('blockSize', 11)
            c = adaptive_data.get('c', 2)
            
            if method == 'mean':
                adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
            else:  # gaussian
                adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            
            thresh = cv2.adaptiveThreshold(gray, 255, adaptive_method, cv2.THRESH_BINARY, block_size, c)
            self.processed_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    
    def _apply_morphology_operations(self, controls: Dict[str, Any]):
        """Apply morphological operations"""
        morphology_data = controls.get('morphology', {})
        kernel_size = morphology_data.get('kernelSize', 3)
        iterations = morphology_data.get('iterations', 1)
        operation = morphology_data.get('operation', 'erode_dilate')
        
        if kernel_size > 1 and iterations > 0:
            # Ensure kernel size is odd
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            
            if operation == 'erode':
                # Erosion: removes small bright spots
                self.processed_image = cv2.erode(self.processed_image, kernel, iterations=iterations)
            elif operation == 'dilate':
                # Dilation: fills small dark spots
                self.processed_image = cv2.dilate(self.processed_image, kernel, iterations=iterations)
            elif operation == 'erode_dilate':
                # Erosion followed by dilation (opening)
                self.processed_image = cv2.erode(self.processed_image, kernel, iterations=iterations)
                self.processed_image = cv2.dilate(self.processed_image, kernel, iterations=iterations)
            elif operation == 'dilate_erode':
                # Dilation followed by erosion (closing)
                self.processed_image = cv2.dilate(self.processed_image, kernel, iterations=iterations)
                self.processed_image = cv2.erode(self.processed_image, kernel, iterations=iterations)
            elif operation == 'open':
                # Opening: erosion followed by dilation
                self.processed_image = cv2.morphologyEx(self.processed_image, cv2.MORPH_OPEN, kernel, iterations=iterations)
            elif operation == 'close':
                # Closing: dilation followed by erosion
                self.processed_image = cv2.morphologyEx(self.processed_image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
            elif operation == 'gradient':
                # Morphological gradient
                self.processed_image = cv2.morphologyEx(self.processed_image, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
            elif operation == 'tophat':
                # Top hat
                self.processed_image = cv2.morphologyEx(self.processed_image, cv2.MORPH_TOPHAT, kernel, iterations=iterations)
            elif operation == 'blackhat':
                # Black hat
                self.processed_image = cv2.morphologyEx(self.processed_image, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
            
            print(f"Applied morphology: {operation}, kernel_size={kernel_size}, iterations={iterations}")
    
    def _apply_color_boost(self, controls: Dict[str, Any]):
        """Apply color boost operations"""
        color_boost = controls.get('colorBoost', {})
        
        # Convert to HSV for saturation and hue operations
        hsv = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Saturation
        saturation = color_boost.get('saturation', 0)
        if saturation != 0:
            hsv[:, :, 1] = hsv[:, :, 1] * (1 + saturation)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Hue shift
        hue_shift = color_boost.get('hueShift', 0)
        if hue_shift != 0:
            hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
        
        # Convert back to BGR
        self.processed_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # RGB channel gains
        rgb_gains = color_boost.get('rgbGains', {})
        if rgb_gains:
            self.processed_image[:, :, 2] = np.clip(self.processed_image[:, :, 2] * rgb_gains.get('r', 1), 0, 255)
            self.processed_image[:, :, 1] = np.clip(self.processed_image[:, :, 1] * rgb_gains.get('g', 1), 0, 255)
            self.processed_image[:, :, 0] = np.clip(self.processed_image[:, :, 0] * rgb_gains.get('b', 1), 0, 255)
        
        # Contrast and brightness
        contrast = color_boost.get('contrast', 0)
        brightness = color_boost.get('brightness', 0)
        if contrast != 0 or brightness != 0:
            self.processed_image = cv2.convertScaleAbs(self.processed_image, alpha=1+contrast, beta=brightness)
    
    def _apply_draw_operations(self, controls: Dict[str, Any]):
        """Apply drawing operations"""
        draw_items = controls.get('drawItems', [])
        
        for item in draw_items:
            color = self._hex_to_bgr(item.get('color', '#FF0000'))
            thickness = item.get('thickness', 2)
            
            if item.get('type') == 'rect' and item.get('xywh'):
                x, y, w, h = item['xywh']
                cv2.rectangle(self.processed_image, (x, y), (x+w, y+h), color, thickness)
            
            elif item.get('type') == 'circle' and item.get('xyr'):
                x, y, r = item['xyr']
                cv2.circle(self.processed_image, (x, y), r, color, thickness)
            
            elif item.get('type') == 'line' and item.get('xyxy'):
                x1, y1, x2, y2 = item['xyxy']
                cv2.line(self.processed_image, (x1, y1), (x2, y2), color, thickness)
            
            elif item.get('type') == 'text' and item.get('text'):
                x, y = item.get('xy', [20, 20])
                scale = item.get('scale', 1.0)
                cv2.putText(self.processed_image, item['text'], (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)
    
    def _apply_final_operations(self, controls: Dict[str, Any]):
        """Apply final operations like brightness and blending"""
        # Brightness
        brightness = controls.get('brightness', 0)
        if brightness != 0:
            self.processed_image = cv2.convertScaleAbs(self.processed_image, beta=brightness)
        
        # Blend with original
        blend_alpha = controls.get('blendAlpha', 0)
        if blend_alpha > 0 and self.original_image is not None:
            # Resize original to match processed if needed
            if self.original_image.shape != self.processed_image.shape:
                self.original_image = cv2.resize(self.original_image, 
                                               (self.processed_image.shape[1], self.processed_image.shape[0]))
            self.processed_image = cv2.addWeighted(self.processed_image, 1-blend_alpha, 
                                                 self.original_image, blend_alpha, 0)
    
    def _get_interpolation_method(self, method: str) -> int:
        """Get OpenCV interpolation method"""
        methods = {
            'nearest': cv2.INTER_NEAREST,
            'linear': cv2.INTER_LINEAR,
            'cubic': cv2.INTER_CUBIC,
            'area': cv2.INTER_AREA,
            'lanczos': cv2.INTER_LANCZOS4
        }
        return methods.get(method, cv2.INTER_LINEAR)
    
    def _hex_to_bgr(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to BGR tuple"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (b, g, r)  # OpenCV uses BGR



