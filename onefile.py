# import os
# from pathlib import Path
# import sys
# import io
# from collections import defaultdict

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# # 📌 Pasta de saída fixa
# PASTA_SAIDA = Path(r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\03_RESOURCES\NotebookLM-Sources-md")
# PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# # 📌 Lista de pastas para processar
# CAMINHOS = [
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\00_DRAFT",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\01_INDEX",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\02_CONCEPT",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\02_CONCEPT\LYT",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\02_CONCEPT\Tec\eng. software",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\03_RESOURCES",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\04_MAPS",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\CALENDAR",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\CODE",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\EFFORTS\09_AREAS",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\EFFORTS\10_PROJECTS",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\EFFORTS\11_ARCHIVES",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\SELF",
#     r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\SYSTEM"
# ]

# # 📌 Lista de pastas a ignorar
# IGNORAR_PASTAS = [
#     ".obsidian",
#     "Ideaverse Pro 2",
#     "css-multi-colluns-callouts-docs",
#     "cssSnippets",
# ]

# def extrair_frontmatter(texto: str):
#     """
#     Extrai frontmatter YAML (entre --- ... ---).
#     Retorna (dict_metadados, conteudo).
#     """
#     linhas = texto.splitlines()
#     if linhas and linhas[0].strip() == "---":
#         for i in range(1, len(linhas)):
#             if linhas[i].strip() == "---":
#                 meta_linhas = linhas[1:i]
#                 conteudo = "\n".join(linhas[i+1:]).strip()
#                 metadados = {}
#                 for linha in meta_linhas:
#                     if ":" in linha:
#                         chave, valor = linha.split(":", 1)
#                         metadados[chave.strip()] = valor.strip()
#                 return metadados, conteudo
#     return {}, texto.strip()

# def deve_ignorar(caminho: Path) -> bool:
#     return any(pasta.lower() in map(str.lower, caminho.parts) for pasta in IGNORAR_PASTAS)

# def juntar_arquivos(pasta_origem, arquivo_saida, separador="\n\n---\n\n", icone="📂", icone_nota="📝", icone_python="🐍"):
#     """
#     Junta todos os arquivos .md e .py de uma pasta em um único arquivo.
#     """
#     pasta = Path(pasta_origem)
#     arquivos = sorted([
#         arq for arq in pasta.rglob("*.*") 
#         if arq.suffix in [".md", ".py"] and not deve_ignorar(arq.parent)
#     ])
    
#     if not arquivos:
#         print(f"⚠ Nenhum arquivo válido encontrado em {pasta_origem}")
#         return
    
#     grupos = defaultdict(list)
#     for arq in arquivos:
#         grupos[arq.parent].append(arq)
    
#     with open(arquivo_saida, "w", encoding="utf-8") as saida:
#         for pasta_atual, arquivos in sorted(grupos.items()):
#             saida.write(f"# {icone} {pasta_atual.relative_to(pasta)}\n\n")
            
#             for i, arquivo in enumerate(sorted(arquivos)):
#                 with open(arquivo, "r", encoding="utf-8") as f:
#                     conteudo = f.read()
                
#                 if arquivo.suffix == ".md":
#                     metadados, corpo = extrair_frontmatter(conteudo)
                    
#                     # título
#                     titulo = f"## {arquivo.stem}\n\n"
#                     saida.write(titulo)
                    
#                     # metadados
#                     if metadados:
#                         meta_formatado = " | ".join(f"{k}: {v}" for k, v in metadados.items())
#                         saida.write(f"{icone_nota} {meta_formatado}\n\n")
                    
#                     # corpo do markdown
#                     saida.write(corpo)
                
#                 elif arquivo.suffix == ".py":
#                     # título com ícone Python
#                     titulo = f"## {icone_python} {arquivo.stem}.py\n\n"
#                     saida.write(titulo)
                    
#                     # código em bloco
#                     saida.write("```python\n")
#                     saida.write(conteudo.strip())
#                     saida.write("\n```\n")
                
#                 if i < len(arquivos) - 1:
#                     saida.write(separador)
            
#             saida.write("\n\n" + "="*50 + "\n\n")

#     print(f"✅ Arquivo '{arquivo_saida}' criado com {len(arquivos)} arquivos em {len(grupos)} subpastas.")

# if __name__ == "__main__":
#     for pasta in CAMINHOS:
#         nome_pasta = Path(pasta).name
#         arquivo_saida = PASTA_SAIDA / f"my_obsidian_folder_{nome_pasta}_onefile.txt"
#         juntar_arquivos(pasta, arquivo_saida)
