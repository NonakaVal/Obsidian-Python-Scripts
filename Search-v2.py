# -*- coding: utf-8 -*-

import os
import re
from collections import defaultdict

class BuscadorNotas:
    def __init__(self, pasta_raiz):
        self.indice = defaultdict(list)
        self.conteudo_notas = {}
        self.construir_indice(pasta_raiz)
    
    def construir_indice(self, pasta_raiz):
        print("Construindo índice de busca...")

        for root, _, files in os.walk(pasta_raiz):
            for file in files:
                if file.endswith(".md"):
                    caminho = os.path.join(root, file)
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            conteudo = f.read()
                            self.conteudo_notas[caminho] = conteudo
                            
                            # Indexa conteúdo
                            palavras = re.finditer(r'\b\w+\b', conteudo.lower())
                            for match in palavras:
                                palavra = match.group()
                                posicao = match.start()
                                self.indice[palavra].append((file, caminho, posicao))
                            
                            # Indexa nome do arquivo
                            nome_arquivo = os.path.splitext(file)[0].lower()
                            for palavra in nome_arquivo.split():
                                self.indice[palavra].append((file, caminho, 0))
                            
                    except Exception as e:
                        print(f"Erro ao ler '{file}': {e}")

        print(f"Índice pronto - {len(self.indice)} termos em {len(self.conteudo_notas)} notas\n")
    
    def buscar(self, termo):
        termo = termo.lower()
        resultados = self.indice.get(termo, [])
        
        # Remove duplicados
        resultados_unicos = []
        vistos = set()
        for r in resultados:
            if r[1] not in vistos:
                vistos.add(r[1])
                resultados_unicos.append(r)

        print(f"\nResultados para '{termo}':")
        if not resultados_unicos:
            print("Nenhum resultado encontrado.")
            return []
        
        print(f"Encontrado em {len(resultados_unicos)} nota(s):")
        
        for arquivo, caminho, posicao in resultados_unicos:
            conteudo = self.conteudo_notas[caminho]
            inicio = max(0, posicao - 30)
            fim = min(len(conteudo), posicao + 30)
            snippet = conteudo[inicio:fim].replace('\n', ' ').strip()
            
            print(f"\nArquivo: {arquivo}")
            print(f"Caminho: {caminho}")
            print(f"Trecho: ...{snippet}...")
        
        return resultados_unicos

if __name__ == "__main__":
    caminho_da_pasta = r"C:\Users\desktop\Documents\Thoughts"

    if not os.path.exists(caminho_da_pasta):
        print(f"Caminho não encontrado: {caminho_da_pasta}")
    else:
        buscador = BuscadorNotas(caminho_da_pasta)

        while True:
            entrada = input("\nBuscar (ou 'sair' para encerrar): ").strip()
            if entrada.lower() == 'sair':
                print("Encerrando busca.")
                break
            buscador.buscar(entrada)