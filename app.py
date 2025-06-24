import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, simpledialog
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений")
        
        # Создаем кнопки
        Button(root, text="Загрузить изображение", command=self.load_image).pack()
        Button(root, text="Показать красный канал", command=lambda: self.show_channel('red')).pack()
        Button(root, text="Обрезать изображение", command=self.crop_image).pack()
        Button(root, text="Повернуть изображение", command=self.rotate_image).pack()
        Button(root, text="Нарисовать прямоугольник", command=self.draw_rectangle).pack()
        
        self.image = None
        self.image_label = Label(root)
        self.image_label.pack()
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.show_image()
    
    def show_image(self):
        if self.image is not None:
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.config(image=imgtk)
            self.image_label.image = imgtk
    
    def show_channel(self, channel):
        if self.image is not None:
            channels = {'red': 2, 'green': 1, 'blue': 0}
            channel_index = channels.get(channel, 2)
            single_channel = np.zeros_like(self.image)
            single_channel[:,:,channel_index] = self.image[:,:,channel_index]
            self.image = single_channel
            self.show_image()
    
    def crop_image(self):
        if self.image is not None:
            coords = simpledialog.askstring("Обрезка", "Введите координаты (x1 y1 x2 y2):")
            try:
                x1, y1, x2, y2 = map(int, coords.split())
                self.image = self.image[y1:y2, x1:x2]
                self.show_image()
            except:
                print("Некорректный ввод!")
    
    def rotate_image(self):
        if self.image is not None:
            angle = simpledialog.askfloat("Поворот", "Введите угол поворота:")
            if angle:
                h, w = self.image.shape[:2]
                M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
                self.image = cv2.warpAffine(self.image, M, (w, h))
                self.show_image()
    
    def draw_rectangle(self):
        if self.image is not None:
            coords = simpledialog.askstring("Прямоугольник", "Введите координаты (x1 y1 x2 y2):")
            try:
                x1, y1, x2, y2 = map(int, coords.split())
                cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                self.show_image()
            except:
                print("Некорректный ввод!")

if __name__ == "__main__":
    root = Tk()
    app = ImageEditor(root)
    root.mainloop()