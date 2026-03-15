from fastapi import FastAPI, File, UploadFile
import os
import tempfile
from gradio_client import Client, handle_file

app = FastAPI()

IDM_VTON_API = "yisol/IDM-VTON"

@app.post("/tryon")
async def try_on(person_image: UploadFile = File(...), cloth_image: UploadFile = File(...)):
    
    temp_dir = None
    result_image_path = None
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        person_image_path = os.path.join(temp_dir, "person_image.jpg")
        person_content = await person_image.read()
        with open(person_image_path, "wb") as f:
            f.write(person_content)
        
        cloth_image_path = os.path.join(temp_dir, "cloth_image.jpg")
        cloth_content = await cloth_image.read()
        with open(cloth_image_path, "wb") as f:
            f.write(cloth_content)
        
        client = Client(IDM_VTON_API)
        
        result = client.predict(
    dict={
        "background": handle_file(person_image_path),
        "layers": [],
        "composite": None
    },
    garm_img=handle_file(cloth_image_path),
    garment_des="clothing item",
    is_checked=True,
    is_checked_crop=False,
    denoise_steps=30,
    seed=42,
    api_name="/tryon"
)
        
        result_image_path = result[0]
        
        return {
            "status": "success",
            "message": "Virtual try-on completed successfully",
            "result_image": result_image_path,
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process try-on: {str(e)}",
        }
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
