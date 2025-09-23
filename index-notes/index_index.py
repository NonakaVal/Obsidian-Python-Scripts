# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from config import MAIN_PATH  # Caminho base fixo

# Forçar UTF-8 no terminal (Windows especialmente)
sys.stdout.reconfigure(encoding='utf-8')

################################## Configuração ##################################

# Verifica se MAIN_PATH existe
if not os.path.exists(MAIN_PATH):
    raise ValueError(f"O diretório principal não existe: {MAIN_PATH}")

# Caminho relativo informado pelo usuário
caminho_da_pasta = r"ATLAS/01_INDEX"

# Concatena com MAIN_PATH para formar o caminho absoluto
caminho_absoluto = os.path.join(MAIN_PATH, caminho_da_pasta)

# Nome da pasta raiz
nome_pasta = os.path.basename(caminho_absoluto.rstrip(os.sep))

# Caminho do arquivo de saída com nome personalizado
caminho_arquivo_saida = os.path.join(
    caminho_absoluto,
    f"_folder_index_{nome_pasta}.md"
)

# Palavras-chave para identificar templates
TEMPLATE_KEYWORDS = ["Templates", "Template", "Ideaverse-Templates"]

# Extensões de arquivo a serem incluídas
EXTENSOES_NOTAS = ['.md', '.base', '.canvas']


def is_template_path(path):
    """Verifica se o caminho é de template"""
    return any(keyword in path for keyword in TEMPLATE_KEYWORDS)


################################## Listagem de notas ##################################

def listar_notas_simples(pasta_raiz):
    """Lista todas as notas (md, base, canvas) de forma simples"""
    notas_por_pasta = {}

    for raiz, _, arquivos in os.walk(pasta_raiz):
        # Ignorar templates
        if is_template_path(raiz):
            continue

        caminho_relativo = os.path.relpath(raiz, pasta_raiz)
        if caminho_relativo == '.':
            caminho_relativo = "Raiz"

        notas_da_pasta = []
        for arquivo in arquivos:
            nome, ext = os.path.splitext(arquivo)
            if ext.lower() in EXTENSOES_NOTAS and not arquivo.startswith('_'):
                if ext.lower() == '.md':
                    nome_completo = nome  # Remove .md
                else:
                    nome_completo = f"{nome}{ext}"  # Mantém .base e .canvas
                notas_da_pasta.append(nome_completo)

        if notas_da_pasta:
            notas_por_pasta[caminho_relativo] = sorted(notas_da_pasta)

    return notas_por_pasta


################################## Gerar lista simples ##################################

def gerar_lista_simples(notas_organizadas, caminho_saida):
    """Gera apenas a hierarquia de pastas e notas"""
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        # Adicionar o frontmatter
        f.write("---\n")
        f.write("cssclasses:\n")
        f.write("  - dash\n")
        f.write("  - dashboard\n")
        f.write("tags:\n")
        f.write("  - index\n")
        f.write("---\n\n")

        
        f.write(f"*Atualizado em {datetime.now().strftime('%Y/%m/%d %H:%M')}*\n\n")
        
        f.write("## Index Index\n")
        f.write("- ⌨️ [[_folder_index_CODE|Code]]\n")
        f.write("- 📦 [[_folder_index_03_RESOURCES|Resources]]\n")
        f.write("- 📅 [[_folder_index_CALENDAR|Calendar]]\n")
        f.write("- 🏔️ [[_folder_index_EFFORTS|Efforts]]\n")
        f.write("- 🧠 [[_folder_index_SELF|Self]]\n")
        f.write("- ⚙️ [[_folder_index_SYSTEM|System]]\n")
        f.write("- 🦆 [[@-templates]]\n")
        f.write("\n---\n")
        f.write("## Atlas Index\n")

        pastas_escritas = set()
        icones_pasta = {
            1: "📁",
            2: "📂",
            3: "📘",
            4: "📙",
            5: "📗",
            6: "📄",
        }

        for caminho_completo, notas in sorted(notas_organizadas.items()):
            if caminho_completo == "Raiz":
                partes = [""]
            else:
                partes = caminho_completo.split(os.sep)

            caminho_acumulado = []

            for i, parte in enumerate(partes):
                if parte:
                    caminho_acumulado.append(parte)
                    chave = os.sep.join(caminho_acumulado)

                    if chave not in pastas_escritas:
                        header_level = min(i + 1, 6)
                        icone = icones_pasta.get(header_level, "📦")
                        f.write(f"{'#' * header_level} {icone} {parte}\n\n")
                        pastas_escritas.add(chave)

            for nome_nota in sorted(notas):
                if nome_nota.endswith('.base'):
                    icone = "🔷"
                elif nome_nota.endswith('.canvas'):
                    icone = "🎨"
                else:
                    icone = "📄"

                
                f.write(f"- {icone} [[{nome_nota}]]\n")

            f.write("\n")


################################## Execução Principal ##################################

if __name__ == "__main__":
    if not os.path.exists(caminho_absoluto):
        print(f"Erro: O diretório '{caminho_absoluto}' não existe!")
        sys.exit(1)

    try:
        notas_organizadas = listar_notas_simples(caminho_absoluto)
        gerar_lista_simples(notas_organizadas, caminho_arquivo_saida)

        total_geral = sum(len(notas) for notas in notas_organizadas.values())
        totais_por_tipo = {'md': 0, 'base': 0, 'canvas': 0}

        for notas in notas_organizadas.values():
            for nota in notas:
                if nota.endswith('.base'):
                    totais_por_tipo['base'] += 1
                elif nota.endswith('.canvas'):
                    totais_por_tipo['canvas'] += 1
                else:
                    totais_por_tipo['md'] += 1

        print(f"✅ Arquivo {caminho_arquivo_saida} gerado com sucesso!")
        print(f"📊 Total de pastas: {len(notas_organizadas)}")
        print(f"📝 Total de arquivos: {total_geral}")
        print(f"   - 📄 .md: {totais_por_tipo['md']} (sem extensão)")
        print(f"   - 🔷 .base: {totais_por_tipo['base']}")
        print(f"   - 🎨 .canvas: {totais_por_tipo['canvas']}")

    except Exception as e:
        print(f"❌ Erro ao gerar o arquivo: {e}")
        sys.exit(1)
