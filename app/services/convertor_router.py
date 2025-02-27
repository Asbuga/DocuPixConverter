import os
import shutil

from fastapi import Depends, APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from schemas.schemas import ImageProcessingOptions
from core.users import current_active_user
from core.config import file_storage_settings as settings
from models.user import User

from .image_convertor import process_image
from .csv_to_xlsx_convertor import convert_csv_xlsx
from .docx_to_pdf_convertor import write_docx, write_pdf


file_router = APIRouter()
UPLOAD_DIR = settings.MEDIA_DIR
# os.makedirs(UPLOAD_DIR, exist_ok=True)


@file_router.post("/convert/image")
async def convert_image(
    file: UploadFile = File(...),
    resize: str = Form(None),
    convert_to: str = Form(None),
    grayscale: bool = Form(None),
    flip: str = Form(None),
    user: User = Depends(current_active_user)
):
    options = ImageProcessingOptions(
        resize=resize,
        convert_to=convert_to,
        grayscale=grayscale,
        flip=flip
    )

    user_folder = f"{UPLOAD_DIR}/{user.id}"
    os.makedirs(user_folder, exist_ok=True)

    file_location = os.path.join(user_folder, file.filename)
    
    with open(file_location, "wb") as buffers:
        shutil.copyfileobj(file.file, buffers)

    processed_file_location = process_image(file_location, options)
    return {"filename": os.path.basename(processed_file_location), "location": processed_file_location}


@file_router.post("/convert/csv-xlsx")
async def convert_csv_xlsx_file(
    file: UploadFile = File(...), 
    user: User = Depends(current_active_user)
):
    user_folder = f"{UPLOAD_DIR}/{user.id}"
    os.makedirs(user_folder, exist_ok=True)

    file_location = os.path.join(user_folder, file.filename)
    processed_file_location = convert_csv_xlsx(file_location)
    return {"filename": os.path.basename(processed_file_location), "location": processed_file_location}


@file_router.post("/convert/pdf-word")




@file_router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str, user: User = Depends(current_active_user)):
    user_folder = f"{UPLOAD_DIR}/{user.id}"
    file_location = os.path.join(user_folder, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)
