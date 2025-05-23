import os
import re
import yaml
from typing import List, Dict, Optional

class FrontmatterProcessor:
    def __init__(self, root_path: str):
        self.root_path = root_path
    
    def extract_frontmatter(self, file_path: str) -> Dict:
        """Extrai e analisa o frontmatter YAML de um arquivo Markdown.
        
        Args:
            file_path: Caminho completo para o arquivo Markdown
            
        Returns:
            Dicionário com os metadados ou vazio se não existir/inválido
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if match:
                try:
                    return yaml.safe_load(match.group(1)) or {}
                except yaml.YAMLError:
                    return {}
        return {}

    def extract_raw_frontmatter(self, content: str) -> Optional[str]:
        """Extrai o frontmatter bruto (não analisado) de um conteúdo Markdown.
        
        Args:
            content: Conteúdo completo do arquivo Markdown
            
        Returns:
            Texto do frontmatter ou None se não existir
        """
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        return match.group(1) if match else None

    def find_files_with_lowercase_hub(self) -> List[str]:
        """Lista arquivos Markdown com 'hub' minúsculo no frontmatter.
        
        Returns:
            Lista de caminhos completos dos arquivos encontrados
        """
        files_with_hub = []
        
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    metadata = self.extract_frontmatter(full_path)
                    if "hub" in metadata and "HUB" not in metadata:
                        files_with_hub.append(full_path)
        
        return files_with_hub

    def replace_hub_with_HUB(self, file_path: str) -> bool:
        """Substitui 'hub:' por 'HUB:' no frontmatter do arquivo.
        
        Args:
            file_path: Caminho completo para o arquivo Markdown
            
        Returns:
            True se houve alteração, False caso contrário
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter_raw = self.extract_raw_frontmatter(content)
        if not frontmatter_raw:
            return False

        corrected = re.sub(r'^hub:', 'HUB:', frontmatter_raw, flags=re.MULTILINE)
        if frontmatter_raw == corrected:
            return False

        corrected_content = re.sub(
            r'^---\n(.*?)\n---\n',
            f"---\n{corrected}\n---\n",
            content,
            flags=re.DOTALL
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        
        return True

    def process_files(self):
        """Executa todo o fluxo: identificação e correção dos arquivos."""
        print(f"Buscando arquivos em: {self.root_path}")
        files_to_fix = self.find_files_with_lowercase_hub()
        
        if not files_to_fix:
            print("Nenhum arquivo com 'hub:' minúsculo encontrado.")
            return
        
        print("\nArquivos com 'hub:' minúsculo encontrados:")
        for file in files_to_fix:
            print(f"• {file}")
        
        print("\nIniciando correção...")
        for file_path in files_to_fix:
            if self.replace_hub_with_HUB(file_path):
                print(f"✔ Corrigido: {file_path}")
            else:
                print(f"— Sem alteração: {file_path}")
        
        print("\nProcesso concluído!")


if __name__ == "__main__":
    # Configuração - altere para o seu diretório
    NOTES_PATH = r"C:\Users\nonak\Documents\Thoughts"
    
    processor = FrontmatterProcessor(NOTES_PATH)
    processor.process_files()