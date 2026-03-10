from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/tryon")
async def try_on(person_image: UploadFile = File(...), cloth_image: UploadFile = File(...)):
    return {"message": "images received successfully"}