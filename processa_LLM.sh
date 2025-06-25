#!/bin/bash
# Script para processar imagens com LLM_Gladiator
# Autor: Atn4s com ajuda da IA 👾
clear
source bin/activate

echo "🚀 Iniciando processamento de imagens com LLM_Gladiator!"
python3.12 LLM_Gladiator.py 
echo "🏁 Processamento concluído! Agora a formatação do JSON será realizada"
python3.12 limpeza_json.py