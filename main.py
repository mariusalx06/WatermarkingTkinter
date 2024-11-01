import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk


def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        display_image(file_path)


def display_image(file_path):
    global original_image
    original_image = Image.open(file_path)
    img = original_image.copy()
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk
    label.pack()

    window.geometry(f"{img.width}x{img.height + 170}")


def watermark_image():
    global current_watermarked_image

    if not original_image:
        messagebox.showerror("Error", "Please select an image first.")
        return

    watermark_text = simpledialog.askstring("Watermark", "Enter watermark text:")
    if not watermark_text:
        return

    watermarked_image = original_image.copy()
    draw = ImageDraw.Draw(watermarked_image)

    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except Exception as e:
        messagebox.showerror("Font Error", f"Could not load font: {e}")
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    position = ((watermarked_image.width - text_width) // 2, (watermarked_image.height - text_height) // 2)

    overlay = Image.new("RGBA", watermarked_image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    opacity = 128  #(0 to 255)
    overlay_draw.text(position, watermark_text, fill=(0, 206, 209, opacity), font=font)

    watermarked_image = Image.alpha_composite(watermarked_image.convert("RGBA"), overlay)
    watermarked_image = watermarked_image.convert("RGB")

    img_tk = ImageTk.PhotoImage(watermarked_image)
    label.config(image=img_tk)
    label.image = img_tk
    window.geometry(f"{watermarked_image.width}x{watermarked_image.height + 170}")
    save_button.pack(pady=10)

    current_watermarked_image = watermarked_image


def save_watermarked_image():
    if current_watermarked_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if file_path:
            current_watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Watermarked image saved successfully!")


window = tk.Tk()
window.title("Image Watermarking")
window.geometry("300x200")

select_button = tk.Button(window, text="Select Image", command=select_image)
select_button.pack(pady=20)

label = tk.Label(window)
label.pack()

watermark_button = tk.Button(window, text="Watermark Image", command=watermark_image)
watermark_button.pack(pady=10)

save_button = tk.Button(window, text="Save Watermarked Image", command=save_watermarked_image)
save_button.pack_forget()

original_image = None
current_watermarked_image = None

window.mainloop()
