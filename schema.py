from typing import List, Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: Optional[str] = None
    qty: Optional[float] = None
    price: Optional[float] = None

class Confidence(BaseModel):
    merchant: float
    date: float
    currency: float
    items: float
    subtotal: float
    tax: float
    total: float

class Receipt(BaseModel):
    document_type: str
    merchant: Optional[str] = None
    date: Optional[str] = None
    currency: Optional[str] = None
    items: List[Item] = []
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    confidence: Confidence
    uncertain_fields: List[str] = []
    notes: Optional[str] = None
