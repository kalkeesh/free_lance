# from fastapi import FastAPI, File, UploadFile, Form,HTTPException
# import os
# from pathlib import Path
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ASSETS_DIR = Path("assets")

# @app.post("/upload-image/")
# async def upload_image(category: str = Form(...), file: UploadFile = File(...)):
#     category_path = ASSETS_DIR / category
#     category_path.mkdir(parents=True, exist_ok=True)
#     file_location = category_path / file.filename
#     with open(file_location, "wb") as buffer:
#         buffer.write(await file.read())
#     return {"info": f"File '{file.filename}' successfully uploaded to '{category}/'"}


# @app.get("/images/")
# async def list_images(category: str):
#     category_path = ASSETS_DIR / category
#     if not category_path.exists() or not category_path.is_dir():
#         raise HTTPException(status_code=404, detail="Category not found")
#     image_files = [file.name for file in category_path.iterdir() if file.is_file()]
#     if not image_files:
#         return {"message": f"No images found in '{category}' category"}
#     return {"images": image_files}



# @app.get("/images/{category}/{image_name}")
# async def get_image(category: str, image_name: str):
#     image_path = ASSETS_DIR / category / image_name
#     if not image_path.exists() or not image_path.is_file():
#         raise HTTPException(status_code=404, detail="Image not found")
#     return FileResponse(image_path)
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSETS_DIR = Path("assets")

# Ensure the assets directory exists
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-image/")
async def upload_image(category: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    category_path = ASSETS_DIR / category
    category_path.mkdir(parents=True, exist_ok=True)
    
    # Save image file
    file_location = category_path / file.filename
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # Save the description in a text file associated with the image
    description_file = category_path / f"{file.filename}.txt"
    with open(description_file, "w") as desc_file:
        desc_file.write(description)

    return {"info": f"File '{file.filename}' successfully uploaded to '{category}/'"}


@app.get("/images/")
async def list_images(category: str):
    category_path = ASSETS_DIR / category
    if not category_path.exists() or not category_path.is_dir():
        raise HTTPException(status_code=404, detail="Category not found")

    image_data = []
    
    # Loop through image files and get corresponding descriptions
    for file in category_path.iterdir():
        if file.is_file() and not file.name.endswith(".txt"):
            description_file = category_path / f"{file.name}.txt"
            if description_file.exists():
                with open(description_file, "r") as desc_file:
                    description = desc_file.read().strip()
            else:
                description = "No description available"
            image_data.append({"name": file.name, "description": description})

    if not image_data:
        return {"message": f"No images found in '{category}' category"}
    
    return {"images": image_data}


@app.get("/images/{category}/{image_name}")
async def get_image(category: str, image_name: str):
    image_path = ASSETS_DIR / category / image_name
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
