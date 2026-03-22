from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SKURequest(BaseModel):
    skus: List[str]
    brand: Optional[str] = None


@app.get("/")
def home():
    return {"status": "ProductScout API v2 running"}


@app.post("/process")
def process_skus(req: SKURequest):

    results = []

    for sku in req.skus:

        # Build search query
        query = f"{req.brand or ''} {sku}".strip()
        encoded_query = urllib.parse.quote(query)

        # Generate search URLs
        amazon_link = f"https://www.amazon.in/s?k={encoded_query}"
        myntra_link = f"https://www.myntra.com/{encoded_query}"
        flipkart_link = f"https://www.flipkart.com/search?q={encoded_query}"
        google_images = f"https://www.google.com/search?tbm=isch&q={encoded_query}"

        # Placeholder images (replace later with scraping)
        images = [
            f"https://source.unsplash.com/300x300/?shoes,{sku}",
            f"https://source.unsplash.com/300x300/?sneakers,{sku}",
            f"https://source.unsplash.com/300x300/?footwear,{sku}"
        ]

        results.append({
            "sku": sku,
            "product_name": f"{req.brand or 'Product'} {sku}",
            "price_inr": "Search",
            "price_usd": "Search",
            "price_eur": "Search",
            "links": {
                "amazon": amazon_link,
                "myntra": myntra_link,
                "flipkart": flipkart_link,
                "images": google_images
            },
            "images": images
        })

    return {
        "count": len(results),
        "results": results
    }
