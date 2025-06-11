import os
import sys
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def desenhar_bbox(draw, coords, text, font):
    x0, y0, x1, y1 = coords
    draw.rectangle([x0, y0, x1, y1], outline="red", width=2)

    # Texto acima do retângulo
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    text_x = x0
    text_y = y0 - text_h - 2

    # Contorno preto
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            draw.text((text_x + dx, text_y + dy), text, font=font, fill=(0, 0, 0))

    # Texto branco
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))


def process_json(json_data, draw, font):
    def process_field(field):
        if ("coordinates" in field or "bounding_box" in field) and "value" in field:
            coords = field.get("coordinates") or field.get("bounding_box")
            desenhar_bbox(draw, coords, str(field["value"]), font)
        if "fields" in field:
            for subfield in field["fields"]:
                process_field(subfield)
        if isinstance(field.get("type"), dict) and field["type"].get("type") == "array":
            for item in field.get("type", {}).get("items", {}).get("fields", []):
                if "coordinates" in item and "value" in item:
                    desenhar_bbox(draw, item["coordinates"], str(item["value"]), font)
        if isinstance(field.get("value"), list):
            for item in field["value"]:
                if isinstance(item, dict):
                    for subfield in item.get("fields", []):
                        process_field(subfield)

    for field in json_data["fields"]:
        process_field(field)


def process_image_with_json(img_path, json_path):
    # === Carrega a imagem ===
    img_cv = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)

    # === Fonte padrão ===
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux padrão
    if not os.path.exists(font_path):
        font_path = "arial.ttf"  # Windows fallback
    font = ImageFont.truetype(font_path, 16)

    # === Lê o JSON ===
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # === Processa JSON e desenha ===
    process_json(json_data, draw, font)

    # === Mostra o resultado ===    
    plt.imshow(img_pil)
    plt.axis("off")
    plt.title("Imagem com bounding boxes do JSON")
    plt.gca().set_aspect('equal', adjustable='box')  # <-- mantém aspecto
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python plote_me.py <caminho_imagem> <caminho_json>")
        sys.exit(1)

    img_path = sys.argv[1]
    json_path = sys.argv[2]

    print(f"[INFO] Processando imagem: {img_path}")
    print(f"[INFO] Usando JSON: {json_path}")

    process_image_with_json(img_path, json_path)