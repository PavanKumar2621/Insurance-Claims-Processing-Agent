from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.logger import logger

from app.extractor import (
    extract_text_from_pdf,
    extract_fields
)

from app.validator import validate_fields
from app.router import determine_route


app = FastAPI()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():

    return {
        "message": "Insurance Claims Processing Agent Running"
    }


@app.post("/process-claim")
async def process_claim(file: UploadFile = File(...)):

    try:

        logger.info(f"Processing file: {file.filename}")

        file_path = f"{UPLOAD_FOLDER}/{file.filename}"

        # SAVE FILE
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("File saved successfully")

        # READ TEXT
        if file.filename.endswith(".pdf"):

            logger.info("Extracting text from PDF")

            text = extract_text_from_pdf(file_path)

        else:

            logger.info("Reading TXT file")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        # EXTRACT FIELDS
        logger.info("Extracting fields")

        data = extract_fields(text)

        logger.info(f"Extracted Data: {data}")

        # VALIDATE
        missing_fields = validate_fields(data)

        logger.info(f"Missing Fields: {missing_fields}")

        # ROUTING
        route, reason = determine_route(
            data,
            missing_fields
        )

        logger.info(f"Recommended Route: {route}")

        # FINAL RESPONSE
        return {
            "extractedFields": data,
            "missingFields": missing_fields,
            "recommendedRoute": route,
            "reasoning": reason
        }

    except Exception as e:

        logger.exception("Error occurred while processing claim")

        return {
            "error": str(e)
        }