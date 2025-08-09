import json
import os

# Caminho do arquivo de configuração
file_path = r"/home/nonaka/Documentos/Obsidian Vauts/Thoughts/.obsidian/plugins/templater-obsidian/data.json"

# Valores de troca
valores = ["SYSTEM/TEMPLATE", "CODE/05_SNIPPETS"]

# Verifica se o arquivo existe
if not os.path.exists(file_path):
    print("Arquivo não encontrado.")
    exit()

# Lê o JSON atual
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Troca o valor da chave "templates_folder"
atual = data.get("templates_folder", "")
if atual == valores[0]:
    data["templates_folder"] = valores[1]
elif atual == valores[1]:
    data["templates_folder"] = valores[0]
else:
    print(f"Valor inesperado: '{atual}'. Nenhuma alteração feita.")
    exit()

# Salva o arquivo atualizado
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f'"templates_folder" atualizado para: {data["templates_folder"]}')
