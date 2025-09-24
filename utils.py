from datetime import datetime

def month_key(iso_str: str) -> str:
    """Tarihi YYYY-MM formatına çevirir."""
    dt = datetime.strptime(iso_str[:19], "%Y-%m-%d %H:%M:%S")
    return f"{dt.year}-{dt.month:02d}"


def print_table(rows, headers):
    """Basit tablo çıktısı üretir."""
    if not rows:
        print("(boş)")
        return

    widths = []
    cols = headers
    for h in cols:
        maxw = max(len(str(r.get(h, ""))) for r in rows)
        widths.append(max(maxw, len(h)))

    line = " | ".join(h.ljust(w) for h, w in zip(cols, widths))
    sep = "-+-".join("-" * w for w in widths)
    print(line)
    print(sep)

    for r in rows:
        print(" | ".join(str(r.get(c, "")).ljust(w) for c, w in zip(cols, widths)))
