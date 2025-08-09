#  pip install --user openai-whisper --break-system-packages

import time
import whisper
from datetime import datetime
from pathlib import Path

# Caminhos absolutos fornecidos
CAMINHO_AUDIOS = Path("/home/nonaka/Obsidian Vaults/Thoughts/+/audios-to-transcribe").resolve()
CAMINHO_SAIDA = Path("/home/nonaka/Obsidian Vaults/Thoughts/SKETCH/+").resolve()

def listar_audios(pasta):
    """
    Lista os arquivos de áudio na pasta especificada.
    """
    if not pasta.exists():
        print(f"Pasta de áudios '{pasta}' não encontrada. Criando pasta...")
        pasta.mkdir(parents=True)
        return []
    
    extensoes = ['.mp3', '.wav', '.ogg', '.opus', '.m4a', '.mp4', '.flac']
    return [f for f in pasta.iterdir() if f.suffix.lower() in extensoes]

def transcrever_audio(caminho_audio, modelo):
    """
    Transcreve um único arquivo de áudio.
    """
    try:
        print(f"\n▶️ Transcrevendo: {caminho_audio.name}")
        inicio = time.time()
        resultado = modelo.transcribe(str(caminho_audio))
        duracao = time.time() - inicio
        print(f"✔️ Finalizado em {duracao:.2f} segundos.")
        return resultado["text"]
    except Exception as e:
        print(f"❌ Erro ao transcrever {caminho_audio.name}: {e}")
        return None

def gerar_nome_arquivo_md():
    """
    Gera nome do arquivo Markdown com data e hora.
    """
    agora = datetime.now()
    return f"transcricoes_{agora.strftime('%Y-%m-%d_%H-%M-%S')}.md"

def gerar_frontmatter():
    """
    Retorna o frontmatter com data atual no formato Obsidian.
    """
    hoje = datetime.now().strftime("%Y-%m-%d")
    return f"""---
created: "[[{hoje}]]"
tags:
  - transcriptions
---\n\n"""

def processar_todos_audios(modelo_nome="medium"):
    """
    Processa todos os arquivos de áudio e gera um arquivo .md formatado.
    """
    audios = listar_audios(CAMINHO_AUDIOS)
    if not audios:
        print("Nenhum áudio encontrado.")
        return

    print(f"\n📥 {len(audios)} arquivos encontrados em: {CAMINHO_AUDIOS}")
    print(f"🧠 Carregando modelo Whisper '{modelo_nome}'...\n")
    modelo = whisper.load_model(modelo_nome)
    print("✅ Modelo carregado.\n")

    # Garante que a pasta de saída existe
    CAMINHO_SAIDA.mkdir(parents=True, exist_ok=True)
    markdown_path = CAMINHO_SAIDA / gerar_nome_arquivo_md()

    with open(markdown_path, "w", encoding="utf-8") as md:
        # Escreve o frontmatter no topo
        md.write(gerar_frontmatter())

        for audio in audios:
            texto = transcrever_audio(audio, modelo)
            if texto:
                md.write("\n---\n\n")
                md.write(f"[[{audio.name}]]\n\n")
                md.write(texto.strip() + "\n\n")
                md.write("---\n")

    print(f"\n📄 Transcrição final salva em:\n{markdown_path}")

if __name__ == "__main__":
    print("=== Transcrição Automática com Whisper ===")
    processar_todos_audios(modelo_nome="medium")
