import os
import re
import sys
from pathlib import Path
from config import MAIN_PATH

# Garante suporte a UTF-8 no terminal (útil para emojis e acentuação)
sys.stdout.reconfigure(encoding='utf-8')

# ==========================
# 🔧 CONFIGURAÇÕES GERAIS
# ==========================

# ⚠️  CAMINHO DO ARQUIVO .MD QUE VAI SER EXECUTADO -- 
##📝 NO OBSIDIAN SE OBTEM COM CTRL+P "Copy file path"
RELATIVE_PATH = "DRAFTS/draft-test.md"     # Caminho relativo para o arquivo a processar


# ⚠️  PREFIXO QUE SERA ADICIONADO NO INICIO DE CADA NOTA GERADA -- 
PREFIXO = "draft-codeSearch"              

# ⚠️ MEDA DADOS QUE SERÃO APLICADOS EM CADA NOTA --
TEMPLATE_FRONTMATTER = """---
created: "[[2025-06-14]]"
HUB:
  - "[[hub-regex]]"
  - "[[hub-linux]]"
connections:
  - "[[flow-build-setup-codeSearch-with-ripgrep-fzf-bat]]"
tags:
  - learning
  - workflow
---"""


# ==========================
# 📦 FUNÇÕES UTILITÁRIAS
# ==========================

def sanitizar_nome_arquivo(nome: str) -> str:
    """Remove caracteres especiais e normaliza nomes de arquivos."""
    nome = re.sub(r'[\\/#%&{}<>*?$\'":@\[\]]', '', nome)  # Remove símbolos indesejados
    nome = nome.strip().lower().replace(' ', '-')         # Converte para slug
    return re.sub(r'-+', '-', nome) or "untitled"         # Evita nomes em branco

def extrair_secoes(conteudo: str) -> list[str]:
    """Extrai blocos iniciados por '##' até a próxima ocorrência."""
    padrao = r"(## .+?)(?=\n## |\Z)"
    return re.findall(padrao, conteudo, flags=re.DOTALL)

def salvar_nova_nota(destino: Path, nome_arquivo: str, conteudo: str):
    """Cria uma nova nota com o conteúdo extraído."""
    caminho = destino / nome_arquivo
    try:
        with open(caminho, 'w', encoding='utf-8') as f_out:
            f_out.write(conteudo)
        print(f"✅ Criado: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo: {e}")

def atualizar_arquivo_original(caminho: Path, conteudo: str):
    """Atualiza o arquivo principal com links para as novas notas."""
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"📝 Atualizado: {caminho.name}")
    except Exception as e:
        print(f"❌ Erro ao atualizar arquivo original: {e}")


# ==========================
# 📄 PROCESSAMENTO PRINCIPAL
# ==========================

def processar_arquivo(caminho_arquivo: str, caminho_relativo: str):
    """Executa todo o fluxo: lê, extrai seções, salva notas e atualiza original."""
    caminho = Path(caminho_arquivo)

    try:
        conteudo = caminho.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return

    nome_base = caminho.stem                         # Nome base do arquivo (sem extensão)
    pasta_destino = caminho.parent                   # Diretório onde salvar as novas notas
    secoes = extrair_secoes(conteudo)                # Lista de seções '##'
    novo_conteudo = conteudo                         # Conteúdo que será atualizado

    for secao in secoes:
        titulo = secao.splitlines()[0].replace("##", "").strip()
        nome_formatado = sanitizar_nome_arquivo(titulo)
        nome_arquivo = f"{PREFIXO}{nome_formatado}.md"

        frontmatter = TEMPLATE_FRONTMATTER.format(rel_path=caminho_relativo.replace('\\', '/'))
        secao_completa = f"{frontmatter}\n\n{secao.strip()}\n\n← Parte de [[{nome_base}]]"

        salvar_nova_nota(pasta_destino, nome_arquivo, secao_completa)
        novo_conteudo = novo_conteudo.replace(secao.strip(), f"# [[{PREFIXO}{nome_formatado}]]")

    atualizar_arquivo_original(caminho, novo_conteudo)


def construir_caminho_completo(relativo: str) -> str:
    """Transforma um caminho relativo em absoluto com base em MAIN_PATH."""
    return os.path.join(MAIN_PATH, relativo.replace("/", "\\"))


# ==========================
# 🚀 EXECUÇÃO PRINCIPAL
# ==========================

if __name__ == "__main__":
    print("📁 Zettelizer - Criação de notas a partir de seções Markdown")
    print(f"📍 Caminho base: {MAIN_PATH}")
    
    # Em versão futura, isso poderia ser um input()
    caminho_relativo = RELATIVE_PATH.strip()
    caminho_completo = construir_caminho_completo(caminho_relativo)

    print(f"\n🔍 Caminho completo: {caminho_completo}")

    if os.path.isfile(caminho_completo) and caminho_completo.endswith(".md"):
        print("\nIniciando processamento...\n")
        processar_arquivo(caminho_completo, caminho_relativo)
    else:
        print("\n❌ Arquivo não encontrado ou inválido")
        print("Por favor, verifique:")
        print(f"1. O caminho base está correto: {MAIN_PATH}")
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

