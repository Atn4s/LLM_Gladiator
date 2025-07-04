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
    mv LLM_Gladiator.py LLM_Gladiator/
    echo "📦 Instalando dependências do LLM_Gladiator"
    pip install -r requirements.txt
    mv requirements.txt LLM_Gladiator/
    mv processa_LLM.sh LLM_Gladiator/
    cd LLM_Gladiator/
    mkdir images

clear
echo "🏁 Setup do LLM_Gladiator foi finalizado!"