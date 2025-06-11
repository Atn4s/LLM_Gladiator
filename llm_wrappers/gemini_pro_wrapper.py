import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def gemini_pro_extract(image_path: str):
    model = genai.GenerativeModel('models/gemini-2.5-pro-preview-05-06')
    img = Image.open(image_path)
    prompt = """Extraia todo o texto e informações úteis da imagem fornecida. Para cada informação encontrada, retorne:

    - O valor extraído
    - O nome do campo correspondente (ex: "cnpj_estabelecimento", "valor_total", etc.)
    - As coordenadas aproximadas do texto na imagem, no formato: [x1, y1, x2, y2] (bounding box)

    Responda no seguinte formato JSON:

    {
  "fields": [
    {
      "name": "chave_acesso",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "cnpj_estabelecimento",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "cpf",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "data_emissao",
      "type": ["null", "string"],
      "default": null,
      "logicalType": "timestamp-millis"
    },
    {
      "name": "itens",
      "type": {
        "type": "array",
        "items": {
          "name": "Item",
          "fields": [
            {
              "name": "codigo",
              "type": ["null", "string"],
              "default": null
            },
            {
              "name": "desconto",
              "type": ["null", "double"],
              "default": null
            },
            {
              "name": "descricao",
              "type": ["null", "string"],
              "default": null
            },
            {
              "name": "numero",
              "type": ["null", "int"],
              "default": null
            },
            {
              "name": "preco_total",
              "type": ["null", "double"],
              "default": null
            },
            {
              "name": "preco_unitario",
              "type": ["null", "double"],
              "default": null
            },
            {
              "name": "quantidade",
              "type": ["null", "int"],
              "default": null
            }
          ]
        }
      },
      "default": []
    },
    {
      "name": "nome_estabelecimento",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "total_itens",
      "type": ["null", "int"],
      "default": null
    },
    {
      "name": "valor_total",
      "type": ["null", "double"],
      "default": null
    },
    {
      "name": "valor_total_desconto",
      "type": ["null", "double"],
      "default": null
    },
    {
      "name": "valor_total_pago",
      "type": ["null", "double"],
      "default": null
    }
  ]
}

Por favor, preencha apenas os campos que encontrar informações correspondentes na imagem."""

    response = model.generate_content([prompt, img], stream=False)
    return response.text
