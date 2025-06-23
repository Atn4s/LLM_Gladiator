import base64
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

def mistral_pixtral_extract(image_path: str):
    """Extrai texto e informações úteis de uma imagem usando o modelo Pixtral da MistralAI."""
    
    # Encode da imagem em base64
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Erro: Arquivo {image_path} não encontrado.")
    except Exception as e:
        raise RuntimeError(f"Erro ao codificar a imagem: {e}")
    
    # Configuração do cliente Mistral
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Erro: MISTRAL_API_KEY não encontrada nas variáveis de ambiente.")
    
    model = "pixtral-12b-2409"
    client = Mistral(api_key=api_key)

    # Monta mensagem para o modelo
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Extraia todo o texto e informações úteis da imagem fornecida.

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
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}" 
                }
            ]
        }
    ]

    # Requisição ao modelo
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        resposta = chat_response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Erro na chamada do modelo Mistral: {e}")
    
    # Retorna o conteúdo da resposta e custo estimado (chute, pois a Mistral não publica o preço por token com imagem ainda)
    return resposta
