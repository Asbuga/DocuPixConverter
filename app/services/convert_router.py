import os
import shutil

from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from core.config import file_storage_settings as settings
from core.users import current_active_user
from models.user import User
from schemas.schemas import ImageProcessingOptions

from .csv_to_xlsx_convertor import convert_csv_xlsx
from .docx_to_pdf_convertor import write_docx, write_pdf
from .image_convertor import process_image


convert_router = APIRouter()
UPLOAD_DIR = settings.MEDIA_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


@convert_router.post("/convert/image")
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
    return {
        "filename": os.path.basename(processed_file_location), 
        "location": processed_file_location
    }


@convert_router.post("/convert/csv-xlsx")
async def convert_csv_xlsx_file(
    file: UploadFile = File(...), 
    user: User = Depends(current_active_user)
):
    user_folder = os.path.join(str(UPLOAD_DIR), str(user.id))
    os.makedirs(user_folder, exist_ok=True)

    file_location = os.path.join(user_folder, file.filename)


    with open(file_location, "wb") as buffers:
        shutil.copyfileobj(file.file, buffers)
    
    filename = convert_csv_xlsx(file_location)
    
    return {"filename": filename}


@convert_router.post("/convert/pdf-docs")
async def convert_pdf_word_file(
    file: UploadFile = File(...), 
    user: User = Depends(current_active_user)
):
    user_folder = f"{UPLOAD_DIR}/{user.id}"
    os.makedirs(user_folder, exist_ok=True)

    file_location = os.path.join(user_folder, file.filename)
    file_docs = file_location.split(".")[0] + ".docs"
    processed_file_location = write_docx(
                                file_word=file_docs, file_pdf=file_location
                                )
    return {
        "filename": os.path.basename(processed_file_location), 
        "location": processed_file_location
    }


@convert_router.post("/convert/docs-pdf")
async def convert_pdf_word_file(
    file: UploadFile = File(...), 
    user: User = Depends(current_active_user)
):
    user_folder = f"{UPLOAD_DIR}/{user.id}"
    os.makedirs(user_folder, exist_ok=True)

    file_location = os.path.join(user_folder, file.filename)
    file_pdf = file_location.split(".")[0] + ".pdf"
    processed_file_location = write_pdf(
                                file_pdf=file_pdf, file_word=file_location
                                )
    return {
        "filename": os.path.basename(processed_file_location), 
        "location": processed_file_location
    }


@convert_router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str, user: User = Depends(current_active_user)):
    user_folder = os.path.join(str(UPLOAD_DIR), str(user.id))
    file_location = os.path.join(user_folder, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return {
        "message": [
            user_folder,
            file_location
        ]
    }
    return FileResponse(file_location)
