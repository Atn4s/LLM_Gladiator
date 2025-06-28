import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env no qual deve conter a chave de API do Google 
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Função para extrair informações de uma imagem, baseado nas instruções do modelo Gemini 2.0 Flash
# A função recebe o caminho da imagem como parâmetro e retorna um JSON com os dados extraídos.
def gemini_flash_extract(image_path: str):
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    img = Image.open(image_path)
    prompt = """Extraia todo o texto e informações úteis da imagem fornecida.

IMPORTANTE:
- Responda APENAS com um JSON válido como para o esquema abaixo.
- Não inclua informações adicionais, formatação Markdown, ```json```, nem explicações.
- O JSON deve conter todos os campos especificados abaixo, mesmo que alguns estejam vazios.
- Use exatamente o formato JSON abaixo para cada dado encontrado:

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
