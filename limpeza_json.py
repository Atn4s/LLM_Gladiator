import json
import os
import sys
import re

def limpar_string_json(s):
    """
    Remove artefatos como delimitadores Markdown e tenta converter strings com escapes em JSON válido.
    """
    if not isinstance(s, str):
        return s

    # Remove delimitadores de bloco de código Markdown (como ```json)
    s = re.sub(r"^```(?:json)?\n?", "", s.strip(), flags=re.IGNORECASE)
    s = re.sub(r"```$", "", s.strip())
    
    # Tenta detectar se a string parece ser um JSON serializado com escapes
    if re.match(r'^[\s\n]*[\{\[]', s) and re.match(r'[\}\]]', s.strip()[-1]):
        try:
            # Remove escapes de aspas se existirem
            s = re.sub(r'(?<!\\)\\(?!\\)"', '"', s)
            # Remove escapes de barras invertidas duplas
            s = s.replace('\\\\', '\\')
            # Remove quebras de linha e tabs escapados
            s = s.replace('\\n', '').replace('\\t', '').replace('\\r', '')
            # Desserializa o JSON
            return json.loads(s)
        except json.JSONDecodeError:
            pass
    
    return s.strip()

def desserializar_multinivel(texto, max_niveis=5):
    """
    Tenta desserializar JSON múltiplas vezes até não conseguir mais ou atingir o limite.
    """
    if not isinstance(texto, str):
        return texto

    texto = limpar_string_json(texto)
    for _ in range(max_niveis):
        if not isinstance(texto, str):
            break
        texto = limpar_string_json(texto)
        if not texto.strip().startswith(('{', '[')):
            break
        try:
            texto = json.loads(texto)
        except json.JSONDecodeError:
            break
    return texto

def limpar_json(dados):
    """
    Recursivamente percorre e limpa o JSON.
    """
    if isinstance(dados, dict):
        novo_dict = {}
        for chave, valor in dados.items():
            if isinstance(valor, str):
                valor = desserializar_multinivel(valor)
                if isinstance(valor, (dict, list)):
                    valor = limpar_json(valor)
                elif isinstance(valor, str):
                    valor = limpar_string_json(valor)
            elif isinstance(valor, (dict, list)):
                valor = limpar_json(valor)
            novo_dict[chave] = valor
        return novo_dict
    elif isinstance(dados, list):
        return [limpar_json(item) for item in dados]
    elif isinstance(dados, str):
        return limpar_string_json(dados)
    else:
        return dados

def processar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            # Tenta ler diretamente como JSON
            try:
                dados = json.loads(conteudo)
            except json.JSONDecodeError:
                # Se falhar, tenta limpar o conteúdo como string JSON
                dados = limpar_string_json(conteudo)
                if isinstance(dados, str):
                    dados = json.loads(dados)
    except Exception as e:
        print(f"[Erro] lendo arquivo {caminho_arquivo}: {e}")
        return None

    dados_limpos = limpar_json(dados)

    pasta_destino = "resultados_limpos"
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_arquivo)
    caminho_saida = os.path.join(pasta_destino, nome_arquivo)

    try:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(dados_limpos, f, ensure_ascii=False, indent=2)
        print(f"[Sucesso] Arquivo processado e salvo: {caminho_saida}")
    except Exception as e:
        print(f"[Erro] salvando arquivo {caminho_saida}: {e}")

    return dados_limpos

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 codigo_json.py caminho1 [caminho2 ...]")
        sys.exit(1)

    caminhos = sys.argv[1:]
    for caminho in caminhos:
        processar_arquivo(caminho)
