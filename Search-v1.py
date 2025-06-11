# -*- coding: utf-8 -*-

import os
import re
import sys
from collections import defaultdict

class BuscadorNotas:
    def __init__(self, pasta_raiz):
        self.indice = defaultdict(list)
        self.construir_indice(pasta_raiz)
    
    def construir_indice(self, pasta_raiz):
        """Cria índice invertido para busca rápida"""
        print("Construindo índice de busca...")

        for root, _, files in os.walk(pasta_raiz):
            for file in files:
                if file.endswith(".md"):
                    caminho = os.path.join(root, file)
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            conteudo = f.read().lower()
                            palavras = set(re.findall(r'\b\w+\b', conteudo))  # Removida restrição de 4+ letras
                            for palavra in palavras:
                                self.indice[palavra].append((file, caminho))
                    except Exception as e:
                        print(f"Erro ao ler '{file}': {e}")

        print(f"Índice construído com {len(self.indice)} termos\n")
    
    def buscar(self, termo):
        """Busca notas contendo o termo"""
        termo = termo.lower()
        resultados = self.indice.get(termo, [])

        print(f"\nResultados para '{termo}':")
        if not resultados:
            print("Nenhuma nota encontrada.")
        else:
            print(f"Encontrado em {len(resultados)} nota(s):")
            for arquivo, caminho in resultados:
                print(f"- {arquivo} -> {caminho}")
        
        return resultados

if __name__ == "__main__":
    caminho_da_pasta = r"C:\Users\desktop\Documents\Thoughts"  # Ajuste para seu caminho

    if not os.path.exists(caminho_da_pasta):
        print(f"Caminho não encontrado: {caminho_da_pasta}")
        sys.exit(1)

    buscador = BuscadorNotas(caminho_da_pasta)

    if len(sys.argv) > 1:
        # Modo direto - busca o termo passado como argumento
        termo = ' '.join(sys.argv[1:])
        buscador.buscar(termo)
    else:
        # Modo interativo (se nenhum termo for passado)
        while True:
            termo = input("\nDigite um termo para buscar (ou 'sair' para terminar): ")
            if termo.lower() == 'sair':
                print("Encerrando busca.")
                break
            buscador.buscar(termo)