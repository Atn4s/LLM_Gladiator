import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    ImageDetailLevel,
)
from azure.core.credentials import AzureKeyCredential

# Carregar variáveis de ambiente
load_dotenv("./env")

# Variáveis
API_TOKEN = os.getenv("GITHUB_API_KEY")  # ou "GITHUB_TOKEN", conforme teu .env
ENDPOINT = "https://models.github.ai/inference"

# Inicializar cliente
client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_TOKEN),
)

def run_model_with_image(model_name, *args):
    if len(args) == 1:
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
        image_path = args[0]
    elif len(args) == 2:
        prompt, image_path = args
    else:
        return "Erro: argumentos inválidos para run_model_with_image()", 0

    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful assistant that analyzes images."),
                UserMessage(
                    content=[
                        TextContentItem(text=prompt),
                        ImageContentItem(
                            image_url=ImageUrl.load(
                                image_file=image_path,
                                image_format="jpg",
                                detail=ImageDetailLevel.HIGH
                            )
                        ),
                    ],
                ),
            ],
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar imagem com o modelo '{model_name}': {e}", 0