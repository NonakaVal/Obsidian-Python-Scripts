# -*- coding: utf-8 -*-

import os
import yaml
import sys
from datetime import datetime
from collections import defaultdict, Counter

# Forçar UTF-8 no terminal (Windows especialmente)
sys.stdout.reconfigure(encoding='utf-8')


################################## Configuração ##################################

caminho_da_pasta = r"C:\Users\desktop\Documents\Thoughts"
caminho_arquivo_saida = os.path.join(caminho_da_pasta, r"_index_notas.md")


################################## Funções utilitárias ##################################

def contar_palavras(texto):
    return len(texto.split())


def formatar_numero(num, decimal_places=1):
    if isinstance(num, int):
        return f"{num:,}".replace(",", ".")
    else:
        return f"{num:,.{decimal_places}f}".replace(",", "X").replace(".", ",").replace("X", ".")


################################## Análise de frontmatter ##################################

def analyze_frontmatter(directory):
    property_stats = defaultdict(Counter)
    property_presence = Counter()
    file_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and file != "_index_notas.md":
                file_path = os.path.join(root, file)
                file_count += 1

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if content.startswith("---"):
                    end_of_header = content.find("---", 3)
                    if end_of_header != -1:
                        header = content[3:end_of_header].strip()
                        try:
                            data = yaml.safe_load(header) or {}
                            for prop, value in data.items():
                                property_presence[prop] += 1
                                if isinstance(value, list):
                                    for item in value:
                                        property_stats[prop][str(item)] += 1
                                else:
                                    property_stats[prop][str(value)] += 1
                        except yaml.YAMLError:
                            pass

    return {
        'property_stats': dict(property_stats),
        'property_presence': property_presence,
        'total_files': file_count
    }


################################## Listagem de notas ##################################

def listar_notas_markdown_organizadas(pasta_raiz):
    notas_por_pasta = defaultdict(list)
    contagem_palavras_por_pasta = defaultdict(int)
    total_palavras_geral = 0
    total_notas_geral = 0
    datas_modificacao = []

    for raiz, _, arquivos in os.walk(pasta_raiz):
        caminho_relativo = os.path.relpath(raiz, pasta_raiz)
        if caminho_relativo == '.':
            continue

        for arquivo in arquivos:
            if arquivo.endswith(".md") and arquivo != "_index_notas.md":
                caminho_completo = os.path.join(raiz, arquivo)
                nome_nota = os.path.splitext(arquivo)[0]

                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    palavras = contar_palavras(conteudo)
                    total_palavras_geral += palavras
                    total_notas_geral += 1
                    contagem_palavras_por_pasta[caminho_relativo] += palavras

                mod_time = os.path.getmtime(caminho_completo)
                datas_modificacao.append(datetime.fromtimestamp(mod_time))

                notas_por_pasta[caminho_relativo].append((nome_nota, palavras))

    return notas_por_pasta, contagem_palavras_por_pasta, total_palavras_geral, total_notas_geral, datas_modificacao


################################## Funções de Hubs ##################################

def extrair_hub(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

            if linhas and linhas[0].strip() == '---':
                # Coletar as linhas do frontmatter
                yaml_linhas = []
                for linha in linhas[1:]:
                    if linha.strip() == '---':
                        break
                    yaml_linhas.append(linha)

                # Parse YAML
                frontmatter = yaml.safe_load("".join(yaml_linhas))
                hub = frontmatter.get('HUB')

                # Retornar como lista para padronizar
                if isinstance(hub, list):
                    return hub
                elif isinstance(hub, str):
                    return [hub]
                else:
                    return []
            else:
                return []
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return []

def contar_hubs(diretorio):
    contador = Counter()
    total_md = 0
    com_frontmatter = 0
    com_hub = 0

    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.md') and arquivo != "_index_notas.md":
                total_md += 1
                caminho_arquivo = os.path.join(raiz, arquivo)

                with open(caminho_arquivo, 'r', encoding='utf-8') as arq:
                    linhas = arq.readlines()

                    if linhas and linhas[0].strip() == '---':
                        com_frontmatter += 1
                        hubs = extrair_hub(caminho_arquivo)

                        if hubs:
                            contador.update(hubs)
                            com_hub += 1

    return {
        'contador_hubs': contador,
        'total_md': total_md,
        'com_frontmatter': com_frontmatter,
        'com_hub': com_hub
    }


################################## Gerar Markdown ##################################

def salvar_em_markdown(notas_organizadas, contagem_por_pasta, total_geral, total_notas, datas_modificacao, frontmatter_data, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        # Cabeçalho e informações básicas
        f.write(f"\n\n*Atualizado em {datetime.now().strftime('%Y/%m/%d %H:%M')}*\n\n")
        f.write("[🐍 Abrir Script Python](file:///C:/Users/desktop/Documents/PythonScripts/create_index_note_py_script.py)\n\n")

        f.write(" ## 🗒️ Informações Gerais\n\n")
        f.write(f"- **Total de Notas:** {formatar_numero(total_notas)}\n")
        media_palavras = total_geral / total_notas if total_notas > 0 else 0
        f.write(f"- **Média de Palavras por Nota:** {formatar_numero(media_palavras)}\n")
        f.write(f"- **Número de Pastas:** {formatar_numero(len(notas_organizadas))}\n")

        if contagem_por_pasta:
            pasta_mais_palavras = max(contagem_por_pasta.items(), key=lambda x: x[1])
            f.write(f"- **Pasta com mais palavras:** `{pasta_mais_palavras[0]}` ({formatar_numero(pasta_mais_palavras[1])} palavras)\n")

        if notas_organizadas:
            pasta_mais_notas = max(notas_organizadas.items(), key=lambda x: len(x[1]))
            f.write(f"- **Pasta com mais notas:** `{pasta_mais_notas[0]}` ({formatar_numero(len(pasta_mais_notas[1]))} notas)\n")

        # Seção de Hubs
        f.write("\n---\n\n## 🏷️ Hubs Mais Utilizados\n\n")
        hubs_data = contar_hubs(caminho_da_pasta)
        contador_hubs = hubs_data['contador_hubs']
        
        if contador_hubs:
            f.write("| Hub | Contagem |\n")
            f.write("|------|----------|\n")
            for hub, quantidade in contador_hubs.most_common(20):  # Mostrar os 20 mais comuns
                f.write(f"| `{hub}` | {quantidade} |\n")
            
            f.write("\n📊 Estatísticas de Hubs:\n")
            f.write(f"- Total de arquivos .md: {hubs_data['total_md']}\n")
            f.write(f"- Arquivos com frontmatter: {hubs_data['com_frontmatter']}\n")
            f.write(f"- Arquivos com hub definido: {hubs_data['com_hub']}\n")
            f.write(f"- Porcentagem com hub: {(hubs_data['com_hub']/hubs_data['com_frontmatter'])*100:.1f}% dos arquivos com frontmatter\n")
        else:
            f.write("Nenhum hub encontrado nos frontmatters.\n")

        # Seção de propriedades do frontmatter
        f.write("\n---\n\n## 🔍 Propriedades no Frontmatter\n\n")

        if frontmatter_data['property_presence']:
            f.write("| Propriedade | Arquivos | Cobertura |\n")
            f.write("|--------------|----------|-----------|\n")
            for prop, count in frontmatter_data['property_presence'].most_common(10):
                coverage = (count / frontmatter_data['total_files']) * 100 if frontmatter_data['total_files'] else 0
                f.write(f"| `{prop}` | {count} | {coverage:.1f}% |\n")
        else:
            f.write("Nenhuma propriedade encontrada no frontmatter.\n")

        # Seção de pastas e notas
        f.write("\n---\n\n# 🗂️ Pastas e Notas\n\n")

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
            partes = caminho_completo.split(os.sep)
            caminho_acumulado = []

            for i, parte in enumerate(partes):
                caminho_acumulado.append(parte)
                chave = os.sep.join(caminho_acumulado)

                if chave not in pastas_escritas:
                    header_level = min(i + 1, 6)
                    icone = icones_pasta.get(header_level, "📦")
                    f.write(f"{'#' * header_level} {icone} {parte}\n\n")
                    pastas_escritas.add(chave)

            for nome_nota, palavras in sorted(notas, key=lambda x: x[1], reverse=True):
                f.write(f"- 📄 [{nome_nota}] — {formatar_numero(palavras)} palavras\n")

            total_pasta = contagem_por_pasta[caminho_completo]
            media_pasta = total_pasta / len(notas) if len(notas) > 0 else 0
            f.write(f"\n**📊 Estatísticas da pasta:**\n")
            f.write(f"- Total: {formatar_numero(total_pasta)} palavras\n")
            f.write(f"- Média por nota: {formatar_numero(media_pasta)} palavras\n")
            f.write(f"- Número de notas: {formatar_numero(len(notas))}\n\n")

        f.write("---\n")


################################## Execução Principal ##################################

if __name__ == "__main__":
    notas_organizadas, contagem_por_pasta, total_palavras, total_notas, datas_modificacao = listar_notas_markdown_organizadas(caminho_da_pasta)

    frontmatter_data = analyze_frontmatter(caminho_da_pasta)

    salvar_em_markdown(
        notas_organizadas,
        contagem_por_pasta,
        total_palavras,
        total_notas,
        datas_modificacao,
        frontmatter_data,
        caminho_arquivo_saida
    )

    print("✅ Arquivo _index_notas.md gerado com sucesso!")