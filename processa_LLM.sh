#!/bin/bash
# Script para processar imagens com LLM_Gladiator
# Autor: Atn4s com ajuda da IA 👾
clear
echo "🚀 Iniciando processamento de imagens com LLM_Gladiator!"
python3 LLM_Gladiator.py 
echo "🏁 Processamento concluído! Agora a formatação do JSON será realizada"
python3 limpeza_json.py