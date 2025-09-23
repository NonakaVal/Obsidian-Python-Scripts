import os
from pathlib import Path
import sys
import io
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 📌 Pasta de saída fixa
PASTA_SAIDA = Path(r"C:\Users\nonak\OneDrive\Área de Trabalho\Thoughts\ATLAS\03_RESOURCES\NotebookLM-Sources-md\Dusk_separado")

# Garante que a pasta existe
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

def extrair_conteudo_sem_frontmatter(texto: str) -> str:
    """
    Remove o frontmatter YAML (entre --- ... ---) se existir,
    retornando apenas o conteúdo da nota.
    """
    linhas = texto.splitlines()
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                return "\n".join(linhas[i+1:]).strip()
    return texto.strip()

def juntar_markdowns_por_pasta(pasta_origem, pasta_saida, separador="\n\n---\n\n", icone="📂"):
    """
    Cria um arquivo .md para cada pasta (e subpasta) contendo todos os arquivos .md daquela pasta,
    ignorando pastas .obsidian e metadados (frontmatter YAML).
    """
    pasta = Path(pasta_origem)
    
    # Encontra todos os arquivos .txt, ignorando pastas .obsidian
    arquivos_txt = []
    for arq in pasta.rglob("*.txt"):
        # Verifica se algum diretório pai é .obsidian
        if ".obsidian" not in arq.parts:
            arquivos_txt.append(arq)

    if not arquivos_txt:
        print("⚠ Nenhum arquivo .txt encontrado na pasta informada (ignorando pastas .obsidian).")
        return
    
    # Agrupar arquivos por pasta
    grupos = defaultdict(list)
    for arq in arquivos_txt:
        grupos[arq.parent].append(arq)
    
    # Cria um arquivo para cada pasta
    arquivos_criados = 0
    for pasta_atual, arquivos in sorted(grupos.items()):
        # Nome do arquivo de saída baseado no nome da pasta
        if pasta_atual == pasta:
            # Se for a pasta raiz, usa o nome da pasta principal
            nome_arquivo_saida = f"{pasta.name}.txt"
        else:
            # Para subpastas, usa o caminho relativo como nome
            caminho_relativo = pasta_atual.relative_to(pasta)
            # Substitui separadores de caminho por _ para evitar problemas
            nome_pasta_formatado = str(caminho_relativo).replace(os.sep, "_")
            nome_arquivo_saida = f"{nome_pasta_formatado}.txt"
        
        caminho_arquivo_saida = Path(pasta_saida) / nome_arquivo_saida
        
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as saida:
            # Header da pasta
            saida.write(f"# {icone} {pasta_atual.relative_to(pasta) if pasta_atual != pasta else pasta.name}\n\n")
            
            for i, arquivo in enumerate(sorted(arquivos)):
                with open(arquivo, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                conteudo_limpo = extrair_conteudo_sem_frontmatter(conteudo)
                
                # título com o nome do arquivo
                titulo = f"## {arquivo.stem}\n\n"
                saida.write(titulo + conteudo_limpo)
                
                if i < len(arquivos) - 1:
                    saida.write(separador)
        
        arquivos_criados += 1
        print(f"✅ Criado: {nome_arquivo_saida} ({len(arquivos)} notas)")

    print(f"\n🎉 Processamento concluído! {arquivos_criados} arquivos .md criados em '{pasta_saida}'.")

if __name__ == "__main__":
    pasta = input("Digite o caminho da pasta com arquivos .md: ").strip()
    nome_pasta = Path(pasta).name  # pega apenas o nome da pasta
    pasta_saida = PASTA_SAIDA / f"{nome_pasta}_unique"
    
    # Cria a pasta de saída específica para este vault
    pasta_saida.mkdir(parents=True, exist_ok=True)
    
    juntar_markdowns_por_pasta(pasta, pasta_saida)