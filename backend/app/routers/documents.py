from fastapi import APIRouter
from app.database.mongodb import db

router = APIRouter()

documents_collection = db["documents"]

@router.post("/documents")
async def save_document(document: dict):

    result = documents_collection.insert_one(document)

    return {
        "status": "success",
        "message": "Document saved successfully.",
        "document_id": str(result.inserted_id),
    }


@router.get("/documents")
async def get_documents():

    documents = []

    for document in documents_collection.find():

        document["_id"] = str(document["_id"])

        documents.append(document)

    return {
        "status": "success",
        "data": documents,
    }