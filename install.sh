#!/bin/bash
# Script robusto para instalar e testar PaddleOCR com fallback automático para paddlepaddle==2.6.2
# Autor: Atn4s com ajuda da IA 👾
clear
echo "🚀 Iniciando setup do LLM_Gladiator!"

# 1. Cria e ativa ambiente virtual
echo "🐍 Criando ambiente virtual 'LLM_Gladiator' na pasta atual"
python3.12 -m venv LLM_Gladiator
source LLM_Gladiator/bin/activate
    mv llm_wrappers LLM_Gladiator/
    mv limpeza_json.py LLM_Gladiator/
    mv LLM_Gladiator.py .py LLM_Gladiator/
    pip install -r requirements.txt
    mv requirements.txt LLM_Gladiator/
    mv processa_LLM.sh LLM_Gladiator/
    cd LLM_Gladiator/
    mkdir images

echo "🏁 Setup do LLM_Gladiator foi finalizado! Verifique se você possui o .env inserido no projeto! Ele possui as chaves API"
echo "🔄 Para utilizar o LLM_Gladiator, insira as imagens que deseja processar denntro da pasta images e execute o script processa_LLM.sh"
echo "O script processa_LLM.sh irá processar as imagens e gerar o JSON formatado com os resultados de forma automatica."
