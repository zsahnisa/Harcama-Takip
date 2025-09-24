from collections import defaultdict
from typing import List, Dict
from utils import month_key

def monthly_summary(data: List[Dict]):
    """Aylık toplam harcamaları döndürür."""
    buckets = defaultdict(float)
    for x in data:
        buckets[month_key(x["date"])] += float(x["amount"])
    return [{"month": k, "total": round(v, 2)} for k, v in sorted(buckets.items())]


def category_summary(data: List[Dict]):
    """Kategori bazlı toplamları döndürür."""
    buckets = defaultdict(float)
    for x in data:
        buckets[x["category"]] += float(x["amount"])
    return [{"category": k, "total": round(v, 2)} for k, v in sorted(buckets.items())]


def total_sum(data: List[Dict]) -> float:
    return round(sum(float(x["amount"]) for x in data), 2)
