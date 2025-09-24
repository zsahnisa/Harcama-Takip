# main.py
import curses
from storage import ensure_store, add_expense, list_expenses, delete_expense, undo_last, load_all
from reports import monthly_summary, category_summary, total_sum
from utils import print_table


# ---- Var olan menü eylemleri (senin mevcut fonksiyonların) ----
def menu_add():
    raw = input("Tutar: ").strip().replace(",", ".")
    try:
        amount = float(raw)
    except ValueError:
        print("❌ Geçerli bir sayı giriniz.")
        return
    category = input("Kategori [genel]: ").strip() or "genel"
    note = input("Açıklama: ").strip()
    expense = add_expense(amount=amount, category=category, note=note)
    print(f"✅ Harcama eklendi: {expense['id']} • {expense['amount']:.2f} TL • "
          f"{expense['category']} • {expense['note']}")


def menu_list():
    limit_raw = input("Kaç kayıt listelensin? [20]: ").strip()
    limit = int(limit_raw) if limit_raw else 20
    rows = list_expenses(limit=limit)
    if not rows:
        print("Henüz kayıt yok.")
        return
    print_table(rows, headers=["id", "date", "amount", "category", "note"])


def menu_delete():
    _id = input("Silmek istediğiniz kaydın ID'si: ").strip()
    ok = delete_expense(_id)
    print("🗑️ Silindi." if ok else "❌ ID bulunamadı.")


def menu_undo():
    ok = undo_last()
    print("↩️ Son işlem geri alındı." if ok else "❌ Geri alınacak işlem yok.")


def menu_summary():
    data = load_all()
    if not data:
        print("❌ Özet için kayıt yok.")
        return
    print("\n📅 Aylık Özet")
    print_table(monthly_summary(data), headers=["month", "total"])
    print("\n🏷️ Kategori Özeti")
    print_table(category_summary(data), headers=["category", "total"])
    print(f"\n💰 Genel Toplam: {total_sum(data):.2f} TL")


# ---- Ok tuşlarıyla çalışan curses menü ----
MENU_ITEMS = [
    ("Harcama ekle", menu_add),
    ("Harcamaları listele", menu_list),
    ("Harcama sil", menu_delete),
    ("Son işlemi geri al", menu_undo),
    ("Özet rapor", menu_summary),
    ("Çıkış", None),
]


def draw_menu(stdscr, selected_idx: int):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "=== Harcamatik ==="
    subtitle = "Yön tuşlarıyla gez, Enter ile seç • (q: çıkış)"
    stdscr.addstr(1, max(0, (w - len(title)) // 2), title, curses.A_BOLD)
    stdscr.addstr(2, max(0, (w - len(subtitle)) // 2), subtitle)

    start_row = 4
    for i, (label, _) in enumerate(MENU_ITEMS):
        prefix = "➤ " if i == selected_idx else "  "
        style = curses.A_REVERSE if i == selected_idx else curses.A_NORMAL
        line = prefix + label
        stdscr.addstr(start_row + i, 2, line[: w - 4], style)

    stdscr.refresh()


def run_curses_menu():
    selected_idx = 0

    def _loop(stdscr):
        nonlocal selected_idx
        curses.curs_set(0)  # imleci gizle
        stdscr.nodelay(False)
        stdscr.keypad(True)

        while True:
            draw_menu(stdscr, selected_idx)
            key = stdscr.getch()

            if key in (curses.KEY_UP, ord('k')):
                selected_idx = (selected_idx - 1) % len(MENU_ITEMS)
            elif key in (curses.KEY_DOWN, ord('j')):
                selected_idx = (selected_idx + 1) % len(MENU_ITEMS)
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter
                return selected_idx
            elif key in (ord('q'), ord('Q')):
                return len(MENU_ITEMS) - 1  # "Çıkış"

    idx = curses.wrapper(_loop)
    return idx


def main_loop():
    while True:
        idx = run_curses_menu()       # ok tuşlarıyla seçim
        label, handler = MENU_ITEMS[idx]

        if handler is None:
            print("👋 Görüşmek üzere!")
            break

        # Curses ekranından çıktıktan sonra normal input() ile soru-cevap
        print(f"\n— {label} —")
        try:
            handler()
        except Exception as e:
            print(f"❌ Hata: {e}")

        input("\nDevam etmek için Enter’a basın...")  # menüye dönüşten önce beklet


if __name__ == "__main__":
    ensure_store()
    try:
        main_loop()
    except Exception as e:
        # Bazı ortamlarda (problemli TERM vs.) curses hata verebilir: güvenli çıkış
        print(f"Curses menü başlatılamadı: {e}")
        print("Yedek mod: sayısal menü ile devam edebilirsiniz.\n")

        # Basit yedek menü (senin eski metin menün)
        while True:
            print("\n=== Harcamatik ===")
            for i, (label, _) in enumerate(MENU_ITEMS, start=1):
                print(f"{i}) {label}")
            choice = input("Seçiminiz: ").strip()

            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(MENU_ITEMS):
                    raise ValueError
            except ValueError:
                print("❌ Geçersiz seçim, tekrar deneyiniz.")
                continue

            _, handler = MENU_ITEMS[idx]
            if handler is None:
                print("👋 Görüşmek üzere!")
                break

            print()
            handler()
            input("\nDevam etmek için Enter’a basın...")
