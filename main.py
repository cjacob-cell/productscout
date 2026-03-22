from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SKURequest(BaseModel):
    skus: List[str]

@app.get("/")
def home():
    return {"status": "ProductScout API running"}

@app.post("/process")
def process_skus(req: SKURequest):
    results = []

    for sku in req.skus:
        results.append({
            "sku": sku,
            "product_name": f"Skechers Model {sku}",
            "price_inr": 4999,
            "price_usd": 79,
            "price_eur": 69,
            "availability": "In Stock",
            "image": "https://via.placeholder.com/150"
        })

    return {
        "count": len(results),
        "results": results
    }