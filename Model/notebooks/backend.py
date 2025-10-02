from fastapi import FastAPI, Form, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import io
from qdrant_client import models, QdrantClient
from pydantic import BaseModel
import torch
import uuid

# --------------------------
# Qdrant Setup
# --------------------------
client = QdrantClient("http://localhost:6333")
COLLECTION_NAME = "Student"

def create_collection(size: int) -> None:
    try:
        collections = client.get_collections()
        existing = [c.name for c in collections.collections]
        
        if COLLECTION_NAME not in existing:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE)
            )
            print(f"Collection '{COLLECTION_NAME}' created.")
        else:
            print(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
    except Exception as e:
        print(f"Error creating collection: {e}")

create_collection(512)

# --------------------------
# FastAPI Setup
# --------------------------
app = FastAPI(title="Student Management System", version="0.0.1")

# Face models
mtcnn = MTCNN(keep_all=False, device='cpu')  # keep_all=False for single face registration
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# --------------------------
# Pydantic Models
# --------------------------
class StudentMetadata(BaseModel):
    PRN: str
    name: str
    source: str

# --------------------------
# API Routes
# --------------------------
@app.post("/register", summary="Register student image embedding and metadata")
async def register_student(
    PRN: str = Form(...),
    name: str = Form(...),
    source: str = Form(...),
    img: UploadFile = File(...)
):
    try:
        img_bytes = await img.read()
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Detect and crop face
        face_tensor = mtcnn(pil_img)
        if face_tensor is None:
            return JSONResponse(status_code=400, content={"error": "No face detected in the image."})

        # Generate embedding
        with torch.no_grad():
            embedding = resnet(face_tensor.unsqueeze(0))
        embedding = embedding.detach().cpu().numpy()[0]

        # Create metadata dict
        metadata = {
            "PRN": PRN,
            "name": name,
            "source": source
        }

        # Store in Qdrant with unique ID
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload=metadata
                )
            ]
        )

        return {"status": "registered", **metadata}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/all_students/", summary="Fetch all registered students")
def get_all_students():
    try:
        all_points = []
        offset = None

        while True:
            response = client.scroll(
                collection_name=COLLECTION_NAME,
                offset=offset,
                limit=100,
                with_vectors=False  # Don't return vectors for efficiency
            )
            all_points.extend(response[0])
            
            if response[1] is None:
                break
            offset = response[1]

        result = []
        for point in all_points:
            result.append({
                "id": point.id,
                "payload": point.payload
            })

        return {"students": result, "count": len(result)}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/identify", summary="Identify person(s) in crowd image")
async def identify_persons(img: UploadFile = File(...), threshold: float = 0.6):
    try:
        img_bytes = await img.read()
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Detect faces in the crowd with keep_all=True
        mtcnn_crowd = MTCNN(keep_all=True, device='cpu')
        face_tensors, probs = mtcnn_crowd(pil_img, return_prob=True)

        if face_tensors is None:
            return JSONResponse(status_code=400, content={"error": "No faces detected in the image."})

        results = []
        for idx, face_tensor in enumerate(face_tensors):
            with torch.no_grad():
                embedding = resnet(face_tensor.unsqueeze(0))
            embedding = embedding.detach().cpu().numpy()[0]

            # Search in Qdrant
            search_result = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding.tolist(),
                limit=1
            )

            if search_result and search_result[0].score >= threshold:
                results.append({
                    "face_index": idx,
                    "match_score": float(search_result[0].score),
                    "student": search_result[0].payload,
                    "detection_confidence": float(probs[idx]) if probs is not None else None
                })
            else:
                results.append({
                    "face_index": idx,
                    "match_score": float(search_result[0].score) if search_result else None,
                    "student": None,
                    "detection_confidence": float(probs[idx]) if probs is not None else None,
                    "reason": "No match above threshold" if search_result else "No match found"
                })

        return {
            "identified_students": results,
            "total_faces_detected": len(face_tensors)
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})