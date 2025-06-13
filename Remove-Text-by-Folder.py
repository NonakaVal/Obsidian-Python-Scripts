import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import MAIN_PATH

def confirm_action(prompt: str) -> bool:
    """Solicita confirmação do usuário."""
    response = input(f"{prompt} (digite 'CONFIRMAR' para prosseguir): ").strip()
    return response.upper() == "CONFIRMAR"

def remove_text_from_markdown(directory: str, target_text: str) -> None:
    """
    Remove um texto específico de arquivos Markdown com verificações de segurança.
    
    Args:
        directory: Diretório para procurar arquivos .md
        target_text: Texto a ser removido dos arquivos
    """
    # Verificação 1: Confirmar o diretório
    print(f"\nDiretório a ser analisado: {directory}")
    dir_confirm = input("Digite parte do caminho para confirmar: ").strip()
    
    if dir_confirm not in directory:
        print("Verificação do diretório falhou. Operação cancelada.")
        return
    
    # Verificação 2: Confirmar o texto a ser removido
    print(f"\nTexto a ser removido: '{target_text}'")
    if not confirm_action("Confirmar remoção deste texto?"):
        print("Operação cancelada pelo usuário.")
        return
    
    print("\nIniciando processamento...")
    files_updated = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verifica se o texto está presente
                    if target_text not in content:
                        continue
                        
                    # Remove o texto
                    updated_content = content.replace(target_text, '')
                    
                    # Verifica se houve alteração
                    if content != updated_content:
                        # Cria backup antes de modificar
                        backup_path = file_path + '.bak'
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Salva as alterações
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        
                        files_updated += 1
                        print(f"✓ Atualizado: {file_path} (backup em {backup_path})")
                
                except PermissionError:
                    print(f"! Permissão negada: {file_path}")
                except Exception as e:
                    print(f"! Erro ao processar {file_path}: {str(e)}")
    
    print(f"\nOperação concluída! {files_updated} arquivos foram modificados.")

if __name__ == "__main__":
    # Configurações
    directory_to_scan = MAIN_PATH
    
    target_text_to_remove = "↪[_cssSnippetCollection](_cssSnippetCollection.md)"
    
    # Executa a função principal
    remove_text_from_markdown(directory_to_scan, target_text_to_remove)