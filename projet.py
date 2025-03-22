import fitz 
from PIL import Image, ImageEnhance
import io

def add_signature_to_pdf(pdf_path: str, image_path: str, output_path: str):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text_instances = page.search_for("signature:")

        if text_instances:
            rect = text_instances[0]
            x, y = rect.x0, rect.y1

            img = Image.open(image_path).convert("L")

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3.0)

            img = img.point(lambda p: 0 if p < 128 else 255)
            img = img.convert("RGB")

            img_width = 100
            img_ratio = img_width / img.width
            img_height = int(img.height * img_ratio)
            img = img.resize((img_width, img_height), Image.LANCZOS)

            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format="PNG")
            img_bytes = img_bytes_io.getvalue()

            img_rect = fitz.Rect(x, y, x + img_width, y + img_height)

            page.insert_image(img_rect, stream=img_bytes)
            break  
    doc.save(output_path)
    doc.close()
    
add_signature_to_pdf(
    "document_not_signed.pdf",
    "signature.png",
    "document_signed.pdf"
)
