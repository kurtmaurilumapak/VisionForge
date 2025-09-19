from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal

class CropData(BaseModel):
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0

class BlurData(BaseModel):
    method: str = "gaussian"
    ksize: int = 3

class EdgesData(BaseModel):
    method: str = "None"
    canny_t1: int = 50
    canny_t2: int = 100
    link_canny_t2: bool = True
    sobel_ksize: int = 3

class BitwiseData(BaseModel):
    operation: str = "None"
    maskThreshold: int = 128
    maskUpload: Optional[str] = None

class AdaptiveThresholdData(BaseModel):
    mode: str = "Simple"
    method: str = "mean"
    blockSize: int = 11
    c: int = 2

class MorphologyData(BaseModel):
    kernelSize: int = 3
    iterations: int = 1
    operation: Literal['erode', 'dilate', 'erode_dilate', 'dilate_erode', 'open', 'close', 'gradient', 'tophat', 'blackhat'] = 'erode_dilate'

class RGBGains(BaseModel):
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0

class ColorBoostData(BaseModel):
    saturation: float = 0.0
    hueShift: float = 0.0
    vibrance: float = 1.0
    rgbGains: RGBGains = RGBGains()
    contrast: float = 0.0
    brightness: float = 0.0

class DrawItem(BaseModel):
    type: str
    color: str = "#FF0000"
    thickness: int = 2
    # Different properties for different shapes
    xywh: Optional[List[int]] = None  # For rectangles
    xyr: Optional[List[int]] = None   # For circles
    xyxy: Optional[List[int]] = None  # For lines
    xy: Optional[List[int]] = None    # For text
    text: Optional[str] = None        # For text
    scale: Optional[float] = None     # For text

class ControlState(BaseModel):
    # Color
    grayscaleAmount: float = 0.0
    colorSpace: str = "RGB"
    
    # Transform
    rotate: float = 0.0
    translateX: float = 0.0
    translateY: float = 0.0
    scale: float = 1.0
    scaleInterpolation: str = "linear"
    crop: CropData = CropData()
    cropAspect: str = "None"
    
    # Filters
    blur: BlurData = BlurData()
    sharpenStrength: float = 0.0
    
    # Edges
    edges: EdgesData = EdgesData()
    
    # Bitwise Operations
    bitwise: BitwiseData = BitwiseData()
    
    # Adaptive Threshold
    adaptiveThreshold: AdaptiveThresholdData = AdaptiveThresholdData()
    
    # Morphology
    morphology: MorphologyData = MorphologyData()
    
    # Color Boost
    colorBoost: ColorBoostData = ColorBoostData()
    
    # Draw
    drawItems: List[DrawItem] = []
    
    # Operations
    brightness: float = 0.0
    blendAlpha: float = 0.0



