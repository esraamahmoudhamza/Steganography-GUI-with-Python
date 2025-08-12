import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StegoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steganography")
        self.geometry("800x550")
        self.resizable(False, False)

        self.stego_image_path = None

        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Steganography GUI", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(10, 0))

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        self.stego_frame = ctk.CTkFrame(container, width=600)
        self.stego_frame.pack(fill="both", expand=True, padx=10)

        stego_title = ctk.CTkLabel(self.stego_frame, text="Steganography", font=ctk.CTkFont(size=18, weight="bold"))
        stego_title.pack(pady=10)

        top_stego_frame = ctk.CTkFrame(self.stego_frame)
        top_stego_frame.pack(fill="x", padx=10)

        self.btn_stego_select = ctk.CTkButton(top_stego_frame, text="Select Image", width=140, command=self.select_stego_image)
        self.btn_stego_select.grid(row=0, column=0, padx=5, pady=5)

        self.entry_stego_text = ctk.CTkEntry(top_stego_frame, placeholder_text="Enter text to hide inside image")
        self.entry_stego_text.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        top_stego_frame.columnconfigure(1, weight=1)

        stego_img_frame = ctk.CTkFrame(self.stego_frame)
        stego_img_frame.pack(pady=10, padx=10, fill="x")

        self.lbl_stego_original_img = ctk.CTkLabel(stego_img_frame)
        self.lbl_stego_original_img.grid(row=0, column=0, padx=10)

        self.lbl_stego_img = ctk.CTkLabel(stego_img_frame)
        self.lbl_stego_img.grid(row=0, column=1, padx=10)

        stego_btn_frame = ctk.CTkFrame(self.stego_frame)
        stego_btn_frame.pack(padx=10, pady=10, fill="x")

        self.btn_hide_text = ctk.CTkButton(stego_btn_frame, text="Hide Text", command=self.hide_text_in_image)
        self.btn_hide_text.pack(side="left", expand=True, padx=10)

        self.btn_extract_text = ctk.CTkButton(stego_btn_frame, text="Extract Text", command=self.extract_text_from_image)
        self.btn_extract_text.pack(side="left", expand=True, padx=10)

        self.entry_extracted_text = ctk.CTkEntry(self.stego_frame, placeholder_text="Extracted text appears here")
        self.entry_extracted_text.pack(padx=20, pady=10, fill="x")

    def select_stego_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.bmp *.jpeg")])
        if path:
            self.stego_image_path = path
            self.load_image_to_label(path, self.lbl_stego_original_img)
            self.lbl_stego_img.configure(image=None)
            self.entry_extracted_text.delete(0, ctk.END)

    def hide_text_in_image(self):
        if not self.stego_image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        text = self.entry_stego_text.get()
        if not text:
            messagebox.showerror("Error", "Enter text to hide.")
            return
        img = Image.open(self.stego_image_path)
        encoded_img = self.lsb_encode(img, text)
        encoded_img.save("stego_output.png")
        self.load_image_to_label("stego_output.png", self.lbl_stego_img)

    def extract_text_from_image(self):
        if not self.stego_image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        img = Image.open("stego_output.png")
        text = self.lsb_decode(img)
        self.entry_extracted_text.delete(0, ctk.END)
        self.entry_extracted_text.insert(0, text)

    def lsb_encode(self, image, message):
        message += chr(0)
        binary = ''.join(format(ord(c), '08b') for c in message)
        img = image.convert('RGB')
        pixels = img.load()
        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(binary):
                    return img
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary[idx])
                idx += 1
                if idx < len(binary):
                    g = (g & ~1) | int(binary[idx])
                    idx += 1
                if idx < len(binary):
                    b = (b & ~1) | int(binary[idx])
                    idx += 1
                pixels[x, y] = (r, g, b)
        return img

    def lsb_decode(self, image):
        img = image.convert('RGB')
        pixels = img.load()
        width, height = img.size
        binary = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary += str(r & 1)
                binary += str(g & 1)
                binary += str(b & 1)
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        message = ""
        for ch in chars:
            if len(ch) != 8:
                continue
            c = chr(int(ch, 2))
            if c == chr(0):
                break
            message += c
        return message

    def load_image_to_label(self, path, label):
        img = Image.open(path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        label.configure(image=photo)
        label.image = photo

if __name__ == "__main__":
    app = StegoApp()
    app.mainloop()
