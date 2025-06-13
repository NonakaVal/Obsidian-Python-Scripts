import os
import re
import sys
from pathlib import Path
from config import MAIN_PATH
sys.stdout.reconfigure(encoding='utf-8')

# Configurações
PREFIXO = "python-"  # Prefixo para os arquivos criados


FRONTMATTER = """---
created: "[[2025-06-11]]"
tags:
  - learning/review
HUB:
  - "[[hub-python]]"
  - "[[hub-ml-models]]"
  - "[[hub-hypothesis-testing]]"
connections:
  - "[[concept-ml-python-correlacao]]"
  - "[[concept-regressao-linear-residuos]]"
  - "[[concept-linear-regression]]"
  - "[[metricas-da-regressao]]"
  - "[[sklearn-criando-modelos]]"
  - "[[doc-sklearn-simple-linear-regression-model]]"
---"""

def sanitizar_nome_arquivo(nome):
    nome = re.sub(r'[\\/#%&{}<>*?$\'":@\[\]]', '', nome)
    nome = nome.strip().lower().replace(' ', '-')
    nome = re.sub(r'-+', '-', nome)
    return nome or "untitled"

def extrair_secoes(conteudo):
    # Padrão modificado para capturar ## em vez de ###
    padrao = r"(## .+?)(?=\n## |\Z)"
    return re.findall(padrao, conteudo, flags=re.DOTALL)

def processar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return

    nome_base = Path(caminho_arquivo).stem
    pasta_destino = os.path.dirname(caminho_arquivo)
    secoes = extrair_secoes(conteudo)
    novo_conteudo = conteudo

    for secao in secoes:
        titulo = secao.splitlines()[0].replace("##", "").strip()  # Modificado para remover ##
        nome_formatado = sanitizar_nome_arquivo(titulo)
        nome_arquivo = f"{PREFIXO}{nome_formatado}.md"
        caminho_novo = os.path.join(pasta_destino, nome_arquivo)

        secao_completa = f"{FRONTMATTER}\n\n{secao.strip()}\n\n← Parte de [[{nome_base}]]"

        try:
            with open(caminho_novo, 'w', encoding='utf-8') as f_out:
                f_out.write(secao_completa)
            print(f"✅ Criado: {nome_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao criar arquivo: {e}")
            continue

        novo_conteudo = novo_conteudo.replace(secao.strip(), f"# [[{PREFIXO}{nome_formatado}]]")

    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(novo_conteudo)
        print(f"📝 Atualizado: {Path(caminho_arquivo).name}")
    except Exception as e:
        print(f"❌ Erro ao atualizar arquivo original: {e}")

def construir_caminho_completo(caminho_relativo):
    caminho_relativo = caminho_relativo.replace('/', '\\')
    return os.path.join(BASE_PATH, caminho_relativo)

if __name__ == "__main__":
    BASE_PATH =   MAIN_PATH  # Caminho base fix
    print("📁 Zettelizer - Crie notas a partir de seções Markdown")
    print(f"📍 Caminho base: {BASE_PATH}")
    print("\nCole o caminho relativo (ex: ATLAS\\02_CONCEPT\\arquivo.md):")
    
    caminho_relativo = input().strip()
    caminho_completo = construir_caminho_completo(caminho_relativo)
    
    print(f"\n🔍 Caminho completo: {caminho_completo}")
    
    if os.path.isfile(caminho_completo) and caminho_completo.endswith(".md"):
        print("\nIniciando processamento...\n")
        processar_arquivo(caminho_completo)
    else:
        print("\n❌ Arquivo não encontrado ou inválido")
        print("Por favor, verifique:")
        print(f"1. O caminho base está correto: {BASE_PATH}")
        print(f"2. O arquivo existe em: {caminho_completo}")
        print("3. O formato do input está correto (ex: ATLAS\\02_CONCEPT\\arquivo.md)")







# import os
# import re

# PREFIXO = "ruby-"  # Prefixo para os arquivos criados

# FRONTMATTER = """---
# tags:
#   - learning
# created: "[[2025-06-10]]"
# HUB:
#   - "[[hub-ruby]]"
# connections:
#   - "[[concept-aoc-1.35-intro-algebra-de-boole]]"
#   - "[[concept-math-algebra-booleana]]"
#   - "[[python-variable-types]]"
# ---"""

# def sanitizar_nome_arquivo(nome):
#     # Remove caracteres especiais
#     nome = re.sub(r'[\\/#%&{}<>*?$\'":@]', '', nome)
#     # Substitui espaços por hífens e converte para minúsculas
#     nome = nome.strip().lower().replace(' ', '-')
#     # Remove múltiplos hífens consecutivos
#     nome = re.sub(r'-+', '-', nome)
#     return nome

# def extrair_secoes(conteudo):
#     padrao = r"(### .+?)(?=\n### |\Z)"
#     return re.findall(padrao, conteudo, flags=re.DOTALL)

# def processar_arquivo(caminho_arquivo):
#     with open(caminho_arquivo, 'r', encoding='utf-8') as f:
#         conteudo = f.read()

#     nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]
#     pasta_destino = os.path.dirname(caminho_arquivo)
#     secoes = extrair_secoes(conteudo)
#     novo_conteudo = conteudo

#     for secao in secoes:
#         linha_header = secao.splitlines()[0]
#         titulo = linha_header.replace("###", "").strip()
#         nome_formatado = sanitizar_nome_arquivo(titulo)
#         nome_arquivo = f"{PREFIXO}{nome_formatado}.md"
#         caminho_novo = os.path.join(pasta_destino, nome_arquivo)

#         # Conteúdo da nova nota
#         secao_completa = (
#             f"{FRONTMATTER}\n\n"
#             f"{secao.strip()}\n\n"
#             f"← Parte de [[{nome_base}]]"
#         )

#         with open(caminho_novo, 'w', encoding='utf-8') as f_out:
#             f_out.write(secao_completa)

#         print(f"✅ Criado: {caminho_novo}")

#         # Substitui no conteúdo original por link com #
#         novo_conteudo = novo_conteudo.replace(secao.strip(), f"# [[{PREFIXO}{nome_formatado}]]")

#     with open(caminho_arquivo, 'w', encoding='utf-8') as f:
#         f.write(novo_conteudo)

#     print(f"📝 Atualizado: {caminho_arquivo}")

# # Execução
# if __name__ == "__main__":
#     caminho = input("Digite o caminho completo do arquivo .md: ").strip('"')
#     if os.path.isfile(caminho) and caminho.endswith(".md"):
#         processar_arquivo(caminho)
#     else:
#         print("❌ Caminho inválido ou arquivo não encontrado.")

