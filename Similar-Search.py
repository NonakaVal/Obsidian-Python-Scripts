#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from datetime import datetime

class BuscadorSimples:
    def __init__(self, pasta_notas):
        self.pasta_notas = Path(pasta_notas).resolve()
        self.palavras_comuns = self._carregar_palavras_comuns()
        self.min_tamanho_palavra = 3
        self.tags_ignoradas = {
            'hub', 'created', 'connections', 'cssclasses', 
            'area', 'type', 'link-to-lib', 'summary'
        }
        
    def _carregar_palavras_comuns(self):
        """Lista de palavras comuns em português e inglês para ignorar"""
        return {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
            'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 
            'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob',
            'the', 'and', 'or', 'of', 'to', 'in', 'on', 'at'
        }
    
    def _processar_texto(self, texto):
        """Extrai palavras relevantes do texto"""
        palavras = re.findall(r'\b\w+\b', texto.lower())
        return [
            palavra for palavra in palavras 
            if palavra not in self.palavras_comuns 
            and len(palavra) >= self.min_tamanho_palavra
        ]
    
    def _extrair_tags_links(self, texto):
        """Captura tags (#) e links ([[ ]]), filtrando tags ignoradas"""
        tags = set(re.findall(r'#(\w+)', texto.lower()))
        links = set(re.findall(r'\[\[([^\|\]]+)', texto.lower()))
        return tags.union(links) - self.tags_ignoradas
    
    def _calcular_similaridade(self, alvo, comparado):
        """Calcula similaridade usando difflib e sobreposição de termos"""
        similaridade_texto = SequenceMatcher(None, alvo['texto'], comparado['texto']).ratio()
        similaridade_termos = len(alvo['termos'] & comparado['termos']) / max(1, len(alvo['termos'] | comparado['termos']))
        similaridade_tags = len(alvo['tags'] & comparado['tags']) / max(1, len(alvo['tags'] | comparado['tags']))
        
        # Combina as métricas com pesos diferentes
        return (
            0.4 * similaridade_texto + 
            0.4 * similaridade_termos + 
            0.2 * similaridade_tags
        )
    
    def buscar_similares(self, arquivo_alvo, limite_similaridade=0.2):
        """Encontra notas similares à nota alvo"""
        caminho_alvo = Path(arquivo_alvo).resolve()
        
        if not caminho_alvo.exists():
            print(f"Erro: Arquivo não encontrado - {caminho_alvo}", file=sys.stderr)
            return []
        
        # Processa o arquivo alvo
        conteudo_alvo = caminho_alvo.read_text(encoding='utf-8')
        alvo = {
            'texto': conteudo_alvo.lower(),
            'termos': set(self._processar_texto(conteudo_alvo)),
            'tags': self._extrair_tags_links(conteudo_alvo),
            'nome_arquivo': caminho_alvo.name,
            'caminho_relativo': str(caminho_alvo.relative_to(self.pasta_notas))
        }
        
        resultados = []
        
        # Percorre todos os arquivos .md na pasta de notas
        for arquivo in self.pasta_notas.rglob('*.md'):
            if arquivo == caminho_alvo:
                continue
                
            try:
                conteudo = arquivo.read_text(encoding='utf-8')
                comparado = {
                    'texto': conteudo.lower(),
                    'termos': set(self._processar_texto(conteudo)),
                    'tags': self._extrair_tags_links(conteudo),
                    'nome_arquivo': arquivo.name,
                    'caminho_relativo': str(arquivo.relative_to(self.pasta_notas))
                }
                
                similaridade = self._calcular_similaridade(alvo, comparado)
                if similaridade >= limite_similaridade:
                    resultados.append({
                        'arquivo_alvo': alvo['caminho_relativo'],
                        'arquivo_comparado': comparado['caminho_relativo'],
                        'similaridade': similaridade,
                        'termos_comuns': list(alvo['termos'] & comparado['termos']),
                        'tags_comuns': list(alvo['tags'] & comparado['tags']),
                        'data_analise': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {str(e)}", file=sys.stderr)
                continue
        
        return sorted(resultados, key=lambda x: x['similaridade'], reverse=True)

def mostrar_resultados(resultados):
    """Exibe os resultados formatados"""
    if not resultados:
        print("Nenhuma nota similar encontrada.")
        return
    
    print("\nNotas similares encontradas:")
    print("-" * 80)
    print(f"Arquivo alvo: {resultados[0]['arquivo_alvo']}")
    print("-" * 80)
    for i, resultado in enumerate(resultados, 1):
        print(f"{i}. {resultado['arquivo_comparado']}")
        print(f"   Similaridade: {resultado['similaridade']:.1%}")
        print(f"   Termos comuns: {', '.join(resultado['termos_comuns'][:5])}{'...' if len(resultado['termos_comuns']) > 5 else ''}")
        print(f"   Tags comuns: {', '.join(resultado['tags_comuns'])}")
        print("-" * 80)

def salvar_csv(resultados, arquivo_saida=None):
    """Salva os resultados em um arquivo CSV"""
    if not resultados:
        return
        
    if arquivo_saida is None:
        arquivo_saida = f"similaridade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    campos = [
        'data_analise',
        'arquivo_alvo',
        'arquivo_comparado',
        'similaridade',
        'termos_comuns',
        'tags_comuns'
    ]
    
    try:
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)
        print(f"\nResultados salvos em: {arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {str(e)}", file=sys.stderr)

def obter_caminho_arquivo(pasta_base):
    """Solicita ao usuário um caminho relativo dentro da pasta base"""
    while True:
        caminho_relativo = input(
            "Digite o caminho relativo do arquivo dentro de Thoughts (ou 'sair' para encerrar):\n> "
        ).strip()
        
        if caminho_relativo.lower() in ('sair', 'exit', 'quit'):
            return None
        
        caminho_completo = Path(pasta_base) / Path(caminho_relativo)
        if caminho_completo.exists():
            return caminho_completo
        else:
            print(f"Arquivo não encontrado: {caminho_completo}. Por favor, tente novamente.")

def main():
    pasta_notas = r"C:\Users\desktop\Documents\Thoughts"
    buscador = BuscadorSimples(pasta_notas)
    
    print("Buscador de Notas Similares")
    print("=" * 40)
    
    while True:
        caminho_arquivo = obter_caminho_arquivo(pasta_notas)
        if caminho_arquivo is None:
            break
            
        resultados = buscador.buscar_similares(caminho_arquivo)
        mostrar_resultados(resultados)
        # salvar_csv(resultados)
        
        continuar = input("\nDeseja buscar por outro arquivo? (s/n): ").strip().lower()
        if continuar != 's':
            break


if __name__ == "__main__":
    main()