# Backend/app/routers/upload.py

# import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

# Create an instance of the APIRouter
router = APIRouter()

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = Path().resolve().parent.parent / 'uploads/courses'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'avi', 'mov'}

# Create the upload folder if it doesn't exist
if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True)

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/upload_course_material")
async def upload_course_material(file: UploadFile = File(...)):
    """Handle file uploads for course materials (e.g., videos, images, PDFs)."""
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed. Allowed types: png, jpg, jpeg, gif, pdf, mp4, avi, mov."
        )

    # Secure the filename by removing any special characters
    filename = file.filename

    # Save the file
    file_path = UPLOAD_FOLDER / filename

    # Check if file already exists (you can also choose to overwrite or rename it)
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")

    # Save the uploaded file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return JSONResponse(content={"message": f"File uploaded successfully to {file_path}"}, status_code=200)