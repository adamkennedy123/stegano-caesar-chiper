import tkinter as tk
from tkinter import filedialog
from stegano import lsb
from PIL import Image, ImageTk

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_val = ord('A') if char.isupper() else ord('a')
            new_ascii = (ord(char) + shift - ascii_val) % 26 + ascii_val
            result += chr(new_ascii)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, 26 - shift)

def encrypt_message():
    plaintext = plaintext_entry.get()
    shift = int(shift_entry.get())
    
    # Meminta pengguna memilih file gambar
    image_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                            filetypes=(("PNG files", "*.png"),))
    
    if image_path:
        if not image_path.lower().endswith('.png'):  # Memeriksa apakah file yang dipilih adalah PNG
            tk.messagebox.showerror("Error", "Please select a PNG file.")
            return
        
        # Enkripsi pesan
        encrypted_text = caesar_encrypt(plaintext, shift)
        
        # Menyembunyikan pesan dalam gambar
        secret = lsb.hide(image_path, encrypted_text)
        secret_path = "secret.png"
        secret.save(secret_path)
        
        # Menampilkan gambar yang dienkripsi
        encrypted_image = Image.open(secret_path)
        encrypted_image.thumbnail((300, 300))  # Menyesuaikan ukuran gambar
        encrypted_photo = ImageTk.PhotoImage(encrypted_image)
        
        # Menampilkan gambar yang dienkripsi
        encrypted_image_label = tk.Label(frame, image=encrypted_photo)
        encrypted_image_label.image = encrypted_photo
        encrypted_image_label.grid(row=4, columnspan=2)
        
        # Menampilkan pesan yang dienkripsi
        encrypted_text_output.config(text=f"Encrypted Text: {encrypted_text}")


def decrypt_message():
    secret = lsb.reveal("secret.png")
    shift = int(shift_entry.get())
    decrypted_text = caesar_decrypt(secret, shift)
    decrypted_text_output.config(text=f"Decrypted Text: {decrypted_text}")



# GUI setup
root = tk.Tk()
root.title("Caesar Cipher & Steganography")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

plaintext_label = tk.Label(frame, text="Enter text:")
plaintext_label.grid(row=0, column=0)

plaintext_entry = tk.Entry(frame)
plaintext_entry.grid(row=0, column=1)

shift_label = tk.Label(frame, text="Shift amount:")
shift_label.grid(row=1, column=0)

shift_entry = tk.Entry(frame)
shift_entry.grid(row=1, column=1)

encrypt_button = tk.Button(frame, text="Encrypt", command=encrypt_message)
encrypt_button.grid(row=2, column=0)

decrypt_button = tk.Button(frame, text="Decrypt", command=decrypt_message)
decrypt_button.grid(row=2, column=1)

encrypted_text_output = tk.Label(frame, text="")
encrypted_text_output.grid(row=3, column=0)

decrypted_text_output = tk.Label(frame, text="")
decrypted_text_output.grid(row=3, column=1)

root.mainloop()
