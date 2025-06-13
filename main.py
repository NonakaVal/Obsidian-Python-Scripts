# main.py

import os
import subprocess


MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

IGNORAR = {"main.py", "config.py", "__init__.py"}

def listar_scripts():
    scripts = [
        f for f in os.listdir(MAIN_PATH)
        if f.endswith(".py") and f not in IGNORAR
    ]
    return sorted(scripts)

def mostrar_menu(scripts):
    print("\n📜 Scripts disponíveis:")
    for i, script in enumerate(scripts):
        print(f"{i+1}. {script}")
    escolha = input("\nDigite o número do script para rodar (ou ENTER para rodar todos): ")
    return escolha

def executar_script(script_path):
    subprocess.run(["python", script_path], cwd=MAIN_PATH)

def main():
    print(f"📂 Procurando scripts em: {MAIN_PATH}")
    scripts = listar_scripts()
    if not scripts:
        print("Nenhum script .py encontrado.")
        return

    escolha = mostrar_menu(scripts)

    if escolha.strip().isdigit():
        idx = int(escolha.strip()) - 1
        if 0 <= idx < len(scripts):
            executar_script(os.path.join(MAIN_PATH, scripts[idx]))
        else:
            print("Índice inválido.")
    else:
        for script in scripts:
            print(f"\n🚀 Executando {script}...")
            executar_script(os.path.join(MAIN_PATH, script))

if __name__ == "__main__":
    main()
