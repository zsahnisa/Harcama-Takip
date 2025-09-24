# Harcamatik (CLI Harcama Takipçisi)

Menülü ve etkileşimli (ok tuşlarıyla kontrol) **komut satırı** uygulaması. Harcamalarınızı ekleyip listeleyebilir, silip geri alabilir; aylık ve kategori bazlı özet raporları görebilirsiniz.

---

## 🚀 Özellikler
- **Ok tuşlarıyla menü**: ↑/↓ ile gez, **Enter** ile seç, **q** ile menüden çık
- **Harcama ekle**: tutar, kategori, açıklama
- **Listele**: son N kayıt
- **Sil**: ID ile
- **Geri al**: son ekleme işlemini iptal et (basit log mantığı)
- **Özet**: aylık toplam, kategori toplamları, genel toplam

---

## 🧰 Kurulum

### macOS / Linux
Sistem Python’ı yeterlidir. Ek kurulum gerekmiyor.
```bash
python3 --version
```

### Windows
`curses` için ek paket gerekir:
```bash
py -m pip install windows-curses
```

---

## ▶️ Çalıştırma
```bash
python3 main.py
```
- **↑/↓**: menüde gezinme  
- **Enter**: seçimi çalıştırma  
- **q**: menüden çıkış (veya “Çıkış” maddesini seç)  

İşlem tamamlandığında “Devam etmek için Enter’a basın...” uyarısından sonra menüye dönülür.

---