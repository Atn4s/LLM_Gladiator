# 🤖 Projeto LLM_Gladiator

Bem-vindo ao **LLM_Gladiator** — um projeto prático para reconhecimento de texto em imagens com uso de **modelos multimodais** e visualização estruturada dos resultados. Tudo automatizado via Shell Script, com suporte a vários modelos top de linha!

---

## 🚀 Objetivo

Realizar a extração de texto em imagens utilizando **modelos multimodais via APIs**. O projeto executa, compara e organiza os resultados gerados por diferentes LLMs com capacidade visual.

---

## 🧠 Tecnologias Utilizadas

- **LLM_Gladiator.py**: cérebro do projeto que orquestra os modelos
- **Modelos Suportados**:
  - Gemini 2.0 Flash / Gemini 2.5 Pro
  - Gemma 3
  - Llama 3.2 (11B e 90B)
  - Llama 4 (Scout / Maverick)
  - Mistral Medium 3 / Pixtral-12b
  - GPT-4.1 / GPT-4o / GPT-4o-mini
  - Phi-3.5 / Phi-4 multimodal

- **LLM_Wrappers/**: scripts individuais para configurar cada modelo
- **Limpeza_Json**: padroniza as saídas dos modelos em `.json` legíveis
- **Shell Script**: instalação + execução automatizadas

---

## 🛠️ Instalação

Clone o repositório e execute o script de instalação:

```bash
git clone https://github.com/Atn4s/LLM_Gladiator
cd LLM_Gladiator
bash install.sh
```

Esse script:

    Cria o ambiente virtual .venv com o nome LLM_Gladiator

    Instala todas as dependências necessárias

    Prepara a estrutura de diretórios

## 🔑 Configuração de API Keys

Antes de qualquer execução, crie um arquivo .env com suas chaves de API:
```
GOOGLE_API_KEY=your_google_key
MISTRAL_API_KEY=your_mistral_key
GITHUB_API_KEY=your_github_key
```

##  🖼️ Como usar
## 1. Preparando as imagens

Coloque as imagens a serem processadas na pasta:
```
images/
```
##  2. Executando o projeto

⚠️ Antes de rodar, ative o ambiente virtual:

```source LLM_Gladiator/bin/activate```

##  📌 Modo automático (recomendado)

```bash processa_LLM.sh```

Esse script irá:

    Executar LLM_Gladiator.py

    Processar todas as imagens da pasta images/ com os modelos disponíveis

    Salvar os resultados em .json (um por modelo) na pasta results/

    Executar limpeza_json.py para:

        Organizar e estruturar os .json

        Salvar os arquivos limpos na pasta resultados_limpos/

## ✋ Modo manual

Você também pode rodar o script diretamente:

```python LLM_Gladiator.py```

Ele executará os wrappers conforme definidos na pasta llm_wrappers/.
📁 Estrutura do Projeto
```
LLM_Gladiator.py             # Script principal de execução
limpeza_json.py              # Limpeza e organização dos JSONs gerados
llm_wrappers/                # Wrappers de configuração para cada modelo
├── gemini_flash_wrapper.py
├── gemini_pro_wrapper.py
├── gemma3_wrapper.py
├── github_wrapper.py
└── mistral_wrapper.py

images/                      # Pasta com as imagens a serem processadas
results/                     # Resultados brutos gerados pelos modelos
resultados_limpos/           # Resultados limpos e estruturados
```
## 📌 Observações Finais

    O projeto ainda está em desenvolvimento — fique à vontade para sugerir melhorias!
