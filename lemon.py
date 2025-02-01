import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label  # Label eklenmeli
from PIL import Image, ImageTk

def detect_lemons(image_path):
    # Fotoğrafı oku
    image = cv2.imread(image_path)
    if image is None:
        print("Fotoğraf yüklenemedi!")
        return
    
    # Görüntüyü HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Limon rengi için alt ve üst sınırları tanımla (HSV değerleri)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    # Renk filtresi uygula
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Maskeyi yumuşatmak için morfolojik işlemler uygula
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Konturları bul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Limonların etrafına yeşil bir kare çiz
    for contour in contours:
        # Küçük gürültüleri filtrele
        if cv2.contourArea(contour) > 500:  # Min alan eşiği
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Sonucu göster
    cv2.imshow("Limon Tespiti", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def upload_image():
    # Dosya seçme penceresini aç
    file_path = filedialog.askopenfilename(
        title="Bir fotoğraf seçin",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        # Seçilen fotoğrafı işle
        detect_lemons(file_path)

# Tkinter GUI oluşturma
root = Tk()
root.title("Limon Tespit Uygulaması")
root.geometry("400x200")

label = Label(root, text="Lütfen bir fotoğraf yükleyin.", font=("Arial", 14))  # Label burada kullanılıyor
label.pack(pady=20)

upload_button = Button(root, text="Fotoğraf Yükle", command=upload_image, font=("Arial", 12))
upload_button.pack(pady=10)

root.mainloop()
