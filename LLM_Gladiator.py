import os
import json
from functools import partial
from llm_wrappers.gemini_flash_wrapper import gemini_flash_extract
from llm_wrappers.gemma3_wrapper import gemma3_extract
from llm_wrappers.gemini_pro_wrapper import gemini_pro_extract
from llm_wrappers.mistral_wrapper import mistral_pixtral_extract
from llm_wrappers.github_wrapper import run_model_with_image

modelos = {
    "Gemini 2.0 Flash": gemini_flash_extract,
    "Gemini 2.5 Pro": gemini_pro_extract,
    "Gemma 3" : gemma3_extract,           
    "GitHub [Llama-3.2-11B-Vision-Instruct]": partial(run_model_with_image, "meta/Llama-3.2-11B-Vision-Instruct"),       
    "GitHub [Llama-3.2-90B-Vision-Instruct]": partial(run_model_with_image, "meta/Llama-3.2-90B-Vision-Instruct"),
    "GitHub [Llama-4-Scout-17B-16E-Instruct]": partial(run_model_with_image, "meta/Llama-4-Scout-17B-16E-Instruct"),
    "GitHub [Llama-4-Maverick-17B-128E-Instruct-FP8]": partial(run_model_with_image, "meta/Llama-4-Maverick-17B-128E-Instruct-FP8"),    
    "GitHub [Mistral Medium 3]": partial(run_model_with_image, "mistral-ai/mistral-medium-2505"),    
    "GitHub [OpenAI GPT-4.1]": partial(run_model_with_image, "openai/gpt-4.1"),
    "GitHub [OpenAI gpt-4o]": partial(run_model_with_image, "openai/gpt-4o"),
    "GitHub [OpenAI gpt-4o-mini]": partial(run_model_with_image, "openai/gpt-4o-mini"),
    "GitHub [Phi-3.5-vision-instruct]": partial(run_model_with_image, "microsoft/Phi-3.5-vision-instruct"),    
    "GitHub [Phi-4-multimodal-instruct]": partial(run_model_with_image, "microsoft/Phi-4-multimodal-instruct"),       
    "Mistral Pixtral-12b-2409": mistral_pixtral_extract    

    # "GitHub [Cohere-embed-v3-multilingual]": partial(run_model_with_image, "Cohere-embed-v3-multilingual"),        
}

# Criar pasta de saída se não existir
os.makedirs("results", exist_ok=True)

# Processar imagens
for img_index, img_name in enumerate(os.listdir("images")):
    img_path = os.path.join("images", img_name)
    print(f"\n📷 Processando imagem: {img_name}")

    for nome_modelo, funcao in modelos.items():
        try:
            texto = funcao(img_path)
        except Exception as e:
            texto = str(e)

        resultado = texto

        # Nome do arquivo: imagem0_gemini.json
        nome_base = os.path.splitext(img_name)[0].lower().replace(" ", "_")
        nome_modelo_id = nome_modelo.lower().replace(" ", "").replace("-", "")
        nome_arquivo = f"{nome_base}_{nome_modelo_id}.json"

        with open(os.path.join("results", nome_arquivo), "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)

print("\n✅ Teste concluído! Resultados salvos como arquivos .json em 'results/'")
