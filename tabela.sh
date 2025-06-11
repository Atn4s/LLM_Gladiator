#!/bin/bash

if [ "$#" -lt 1 ]; then
  echo "Uso: $0 arquivo1.json arquivo2.json ..."
  exit 1
fi

# Função para extrair campos primitivos e montar tabela geral
extract_table() {
  local json="$1"

  # Extrai nomes dos campos primitivos (string, number, boolean)
  mapfile -t names < <(echo "$json" | jq -r '.fields[] | select((.value | type) == "string" or (.value | type) == "number" or (.value | type) == "boolean") | .name')

  # Extrai valores correspondentes, trocando pipes para evitar bagunça na tabela
  mapfile -t values < <(echo "$json" | jq -r '.fields[] | select((.value | type) == "string" or (.value | type) == "number" or (.value | type) == "boolean") | (.value // .default // "—")' | sed 's/|/\\|/g')

  # Monta linha de cabeçalho e linha de valores
  local header="| Imagem | Modelo | Itens Count "
  local line="| $imagem | $modelo | $itens_count "

  for n in "${names[@]}"; do
    header+="| $n "
  done
  header+="|"

  for v in "${values[@]}"; do
    line+="| $v "
  done
  line+="|"

  echo "$header"
  echo "$line"
}

# Função para imprimir itens detalhados em tabela
print_itens() {
  local json="$1"
  
  # Verifica se 'itens' é array
  local is_array=$(echo "$json" | jq -r '.fields[]? | select(.name=="itens") | (.value | type) // empty')
  
  echo "| Código | Descrição | Quantidade | Preço Unitário | Preço Total |"
  echo "|--------|-----------|------------|----------------|-------------|"
  
  if [ "$is_array" = "array" ]; then
    echo "$json" | jq -r '
      .fields[]? 
      | select(.name=="itens") 
      | .value[]? 
      | [
          (.codigo // "—"),
          (.descricao // "—"),
          (.quantidade // "—"),
          (.preco_unitario // "—"),
          (.preco_total // "—")
        ] | @tsv' | while IFS=$'\t' read -r cod desc qtd pu pt; do
          printf "| %s | %s | %s | %s | %s |\n" "$cod" "$desc" "$qtd" "$pu" "$pt"
    done
  else
    # Caso itens não seja array (pode ser estruturado diferente)
    echo "$json" | jq -r '
      [.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="codigo") | .default // empty] as $cods |
      [.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="descricao") | .default // empty] as $descs |
      [.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="quantidade") | .default // empty] as $qtds |
      [.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="preco_unitario") | .default // empty] as $pus |
      [.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="preco_total") | .default // empty] as $pts |
      range(0; [$cods, $descs, $qtds, $pus, $pts] | map(length) | max) as $i |
      [
        ($cods[$i] // "—"),
        ($descs[$i] // "—"),
        ($qtds[$i] // "—"),
        ($pus[$i] // "—"),
        ($pts[$i] // "—")
      ] | @tsv
    ' 2>/dev/null | while IFS=$'\t' read -r cod desc qtd pu pt; do
      [ "$cod" != "—" ] && printf "| %s | %s | %s | %s | %s |\n" "$cod" "$desc" "$qtd" "$pu" "$pt"
    done
  fi
}

for json_file in "$@"; do
  if [ ! -f "$json_file" ]; then
    echo "Arquivo não encontrado: $json_file"
    continue
  fi

  imagem=$(jq -r '.imagem // "—"' "$json_file" 2>/dev/null || echo "—")
  modelo=$(jq -r '.modelo // "—"' "$json_file" 2>/dev/null || echo "—")

  texto_extraido=$(jq -r '.texto_extraido // empty' "$json_file" 2>/dev/null | sed '1s/^```json//' | sed '$s/```$//')

  if [ -z "$texto_extraido" ]; then
    echo "Arquivo $json_file: texto_extraido não encontrado ou vazio."
    continue
  fi

  # Conta itens - primeiro tenta array, depois campos default
  itens_count="—"
  array_count=$(echo "$texto_extraido" | jq -r '.fields[]? | select(.name=="itens") | .value | length // 0' 2>/dev/null || echo "0")
  if [ "$array_count" -gt 0 ]; then
    itens_count=$array_count
  else
    field_count=$(echo "$texto_extraido" | jq -r '[.fields[]? | select(.name=="itens") | .type.items.fields[]? | select(.name=="codigo") | .default // empty] | length // 0' 2>/dev/null || echo "0")
    [ "$field_count" -gt 0 ] && itens_count=$field_count
  fi

  echo ""
  extract_table "$texto_extraido"
  echo ""
  echo "Itens detalhados:"
  print_itens "$texto_extraido"
  echo ""
done
