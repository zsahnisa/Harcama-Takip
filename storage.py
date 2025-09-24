import json, os, time, uuid
from typing import List, Dict

STORE_DIR = os.path.join(os.path.dirname(__file__), "data")
STORE_FILE = os.path.join(STORE_DIR, "expenses.json")
LOG_FILE = os.path.join(STORE_DIR, "ops.log")


def ensure_store():
    """Veri dosyaları yoksa oluştur."""
    os.makedirs(STORE_DIR, exist_ok=True)
    if not os.path.exists(STORE_FILE) or os.path.getsize(STORE_FILE) == 0:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "a", encoding="utf-8").close()


def _read() -> List[Dict]:
    """Dosyadan tüm kayıtları oku (boş/bozuk dosyaya karşı güvenli)."""
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            txt = f.read().strip()
            if not txt:
                return []
            return json.loads(txt)
    except (json.JSONDecodeError, FileNotFoundError):
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []


def _write(data: List[Dict]):
    """Tüm kayıtları dosyaya yaz."""
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all() -> List[Dict]:
    return _read()


def add_expense(amount: float, category: str, note: str) -> Dict:
    data = _read()
    item = {
        "id": uuid.uuid4().hex[:8],
        "ts": int(time.time()),
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "amount": round(float(amount), 2),
        "category": category.strip().lower(),
        "note": note.strip(),
    }
    data.append(item)
    _write(data)
    _log(("ADD", item["id"]))
    return item


def list_expenses(limit: int = 20) -> List[Dict]:
    data = _read()
    data.sort(key=lambda x: x["ts"], reverse=True)
    return data[:limit] if limit else data


def delete_expense(_id: str) -> bool:
    data = _read()
    idx = next((i for i, x in enumerate(data) if x["id"] == _id), None)
    if idx is None:
        return False
    data.pop(idx)
    _write(data)
    _log(("DEL", _id))
    return True


def undo_last() -> bool:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        return False
    if not lines:
        return False

    last = lines[-1]
    op, _id = last.split(" ", 1)
    data = _read()

    if op == "ADD":
        data = [x for x in data if x["id"] != _id]
        _write(data)
        _shrink_log()
        return True
    if op == "DEL":
        return False
    return False


def _log(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{entry[0]} {entry[1]}\n")


def _shrink_log():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    lines = lines[:-1]
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(l + ("\n" if not l.endswith("\n") else "") for l in lines)
