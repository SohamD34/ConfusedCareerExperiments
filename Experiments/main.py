from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import os
import pymongo

app = FastAPI()

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://namanjha025:Stevesmith%4049@cluster0.xkpoqzw.mongodb.net/")
db = client.creators_db
documents_collection = db.documents
reports_collection = db.reports


# Data models
class DetailedReport(BaseModel):
    creator_id: str
    creator_name: str
    summary: str
    key_points: List[str]
    documents: List[str] = []


# Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")


@app.post("/uploadfile/")
def upload_file(creator_name: str = Form(...), file: UploadFile = File(None)):
    try:
        creator_id = str(uuid.uuid4())  # Generate a unique creator_id
        document_metadata = {
            "creator_id": creator_id,
            "creator_name": creator_name,
            "upload_timestamp": datetime.utcnow()
        }
        
        if file:
            file_path = f"uploads/{file.filename}"
            with open(file_path, 'wb') as out_file:
                content = file.file.read()
                out_file.write(content)
            document_metadata["filename"] = file.filename
        
        result = documents_collection.insert_one(document_metadata)
        if result.inserted_id:
            return {"status": "success", "file_id": str(result.inserted_id), "creator_id": creator_id}
        else:
            raise HTTPException(status_code=500, detail="File upload failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/detailed_report/")
def create_detailed_report(report: DetailedReport):
    try:
        report_dict = report.dict()
        result = reports_collection.insert_one(report_dict)
        if result.inserted_id:
            return {"status": "success", "report_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Report creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
