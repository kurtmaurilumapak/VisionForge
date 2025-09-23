from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
from typing import Optional, List, Dict, Any
import uvicorn
import zipfile

from services.image_processor import ImageProcessor
from models.control_models import ControlState
from config import HOST, PORT, RELOAD, ALLOWED_ORIGINS, API_TITLE, API_VERSION, API_DESCRIPTION

app = FastAPI(
    title=API_TITLE, 
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize image processor
image_processor = ImageProcessor()

@app.get("/")
async def root():
    return {"message": "VisionForge API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/process-image")
async def process_image(
    image: UploadFile = File(...),
    controls: str = Form(...)
):
    """
    Process image with the given controls
    """
    try:
        # Parse controls JSON
        control_data = json.loads(controls)
        
        # Read and decode image
        image_bytes = await image.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process image
        processed_img = image_processor.process_image(img, control_data)
        
        # Encode processed image
        _, buffer = cv2.imencode('.png', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "success": True,
            "processed_image": f"data:image/png;base64,{img_base64}",
            "original_size": img.shape[:2],
            "processed_size": processed_img.shape[:2]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-image-base64")
async def process_image_base64(
    image_data: str = Form(...),
    controls: str = Form(...)
):
    """
    Process image from base64 string
    """
    try:
        # Parse controls JSON
        try:
            control_data = json.loads(controls)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid controls JSON: {str(e)}")
        
        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Validate image dimensions
        if img.shape[0] == 0 or img.shape[1] == 0:
            raise HTTPException(status_code=400, detail="Invalid image dimensions")
        
        # Process image
        try:
            processed_img = image_processor.process_image(img, control_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")
        
        # Validate processed image
        if processed_img is None or processed_img.shape[0] == 0 or processed_img.shape[1] == 0:
            raise HTTPException(status_code=500, detail="Image processing resulted in invalid image")
        
        # Encode processed image
        try:
            _, buffer = cv2.imencode('.png', processed_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image encoding error: {str(e)}")
        
        return {
            "success": True,
            "processed_image": f"data:image/png;base64,{img_base64}",
            "original_size": img.shape[:2],
            "processed_size": processed_img.shape[:2]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import os
    # Respect Electron override to avoid uvicorn reload worker that can outlive Electron
    reload_env = os.getenv("RELOAD", str(RELOAD))
    is_electron = os.getenv("ELECTRON") == "1"
    reload_flag = False if is_electron else (reload_env.lower() == "true")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=reload_flag)

# -------- ZIP Creation Endpoint --------
@app.post("/zip-images")
async def zip_images(payload: Dict[str, Any]):
    """
    Accepts JSON payload with list of files to zip.
    Expected payload format:
    {
      "files": [
        {"name": "image1.png", "dataUrl": "data:image/png;base64,...."},
        ...
      ]
    }
    Returns: application/zip stream
    """
    try:
        files = payload.get("files", [])
        if not isinstance(files, list) or len(files) == 0:
            raise HTTPException(status_code=400, detail="No files provided")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for idx, f in enumerate(files):
                name = f.get("name") or f"image_{idx + 1}.png"
                data_url = f.get("dataUrl")
                if not data_url or not isinstance(data_url, str):
                    continue
                try:
                    # Support data URLs (e.g., data:image/png;base64,....)
                    if data_url.startswith("data:image"):
                        base64_part = data_url.split(",", 1)[1]
                    else:
                        base64_part = data_url
                    raw = base64.b64decode(base64_part)
                except Exception:
                    # Skip invalid entries
                    continue
                # Ensure extension
                if "." not in name:
                    name = name + ".png"
                zipf.writestr(name, raw)

        zip_buffer.seek(0)
        headers = {
            "Content-Disposition": f"attachment; filename=visionforge_results.zip"
        }
        return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ZIP: {str(e)}")
