#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OBSIDIAN SMART NOTE LINKER
- Finds semantically similar notes using advanced NLP techniques
- Pure content-based analysis (no metadata dependencies)
- Efficient processing for large vaults
"""

import os
import re
import math
from pathlib import Path
from collections import defaultdict, Counter
import unicodedata
from typing import Dict, List, Tuple, Set

# Configuration
MIN_WORD_LENGTH = 3
SIMILARITY_THRESHOLD = 0.15
MAX_RESULTS = 10

class NoteLinker:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path).resolve()
        self._validate_vault()
        self.stopwords = self._load_stopwords()
        self.notes = {}
        self.vocabulary = set()
        self.tfidf_vectors = {}

    def _validate_vault(self):
        """Ensure the vault exists and contains markdown files"""
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault not found at {self.vault_path}")
        if not list(self.vault_path.glob('**/*.md')):
            print(f"⚠️ Warning: No markdown files found in {self.vault_path}")

    def _load_stopwords(self) -> Set[str]:
        """Load common words to ignore in analysis"""
        return {
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'em', 'no', 'na',
            'que', 'com', 'para', 'por', 'sem', 'ao', 'à', 'das', 'dos', 'the',
            'and', 'of', 'to', 'in', 'is', 'it', 'that', 'for', 'with', 'on'
        }

    def _normalize_text(self, text: str) -> str:
        """Standardize text for consistent processing"""
        text = unicodedata.normalize('NFKD', text.lower())
        return ''.join(c for c in text if not unicodedata.combining(c))

    def _tokenize(self, text: str) -> List[str]:
        """Extract meaningful words from text"""
        text = self._normalize_text(text)
        words = re.findall(r'\b[\w-]+\b', text)
        return [w for w in words 
                if w not in self.stopwords 
                and len(w) >= MIN_WORD_LENGTH
                and not w.isdigit()]

    def load_notes(self):
        """Load and process all markdown files in the vault"""
        for note_path in self.vault_path.glob('**/*.md'):
            if '.obsidian' in note_path.parts:
                continue
                
            try:
                with open(note_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove YAML frontmatter
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    # Remove markdown links
                    content = re.sub(r'\[\[(.*?)\]\]', r'\1', content)
                    self.notes[str(note_path.relative_to(self.vault_path))] = content
                    self.vocabulary.update(self._tokenize(content))
            except Exception as e:
                print(f"⚠️ Error processing {note_path.name}: {e}")

        self._build_tfidf_vectors()

    def _build_tfidf_vectors(self):
        """Calculate TF-IDF vectors for all documents"""
        doc_freq = defaultdict(int)
        for content in self.notes.values():
            unique_words = set(self._tokenize(content))
            for word in unique_words:
                doc_freq[word] += 1

        total_docs = len(self.notes)
        for note_path, content in self.notes.items():
            tokens = self._tokenize(content)
            term_freq = Counter(tokens)
            vector = {}
            
            for word, count in term_freq.items():
                tf = count / len(tokens)
                idf = math.log(total_docs / (1 + doc_freq[word]))
                vector[word] = tf * idf
                
            self.tfidf_vectors[note_path] = vector

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors"""
        common_words = set(vec_a.keys()) & set(vec_b.keys())
        dot_product = sum(vec_a[word] * vec_b[word] for word in common_words)
        
        norm_a = math.sqrt(sum(v**2 for v in vec_a.values()))
        norm_b = math.sqrt(sum(v**2 for v in vec_b.values()))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    def find_similar(self, target_note: str, threshold: float = SIMILARITY_THRESHOLD) -> List[Tuple[str, float]]:
        """Find notes similar to the target note"""
        if target_note not in self.tfidf_vectors:
            raise ValueError(f"Note not found: {target_note}")
            
        target_vector = self.tfidf_vectors[target_note]
        results = []
        
        for note_path, vector in self.tfidf_vectors.items():
            if note_path == target_note:
                continue
                
            similarity = self._cosine_similarity(target_vector, vector)
            if similarity >= threshold:
                results.append((note_path, similarity))
                
        return sorted(results, key=lambda x: x[1], reverse=True)[:MAX_RESULTS]


def display_results(target: str, results: List[Tuple[str, float]]):
    """Display results in a user-friendly format"""
    if not results:
        print(f"\nNo similar notes found for '{target}'")
        return
        
    print(f"\n🔗 Similar notes for '{target}':")
    print("=" * 60)
    for i, (note, score) in enumerate(results, 1):
        print(f"{i}. {note} ({score:.1%})")
        print(f"   {os.path.dirname(note)}")
        print()


def save_markdown(target_note: str, results: List[Tuple[str, float]]):
    """Save the similar notes as markdown backlinks"""
    base_name = Path(target_note).stem
    filename = f"SimilarLinks_{base_name}.md"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 🔗 Notas semelhantes para `{target_note}`\n\n")
            for note, score in results:
                relative_path = Path(note).with_suffix('')  # Remove .md
                f.write(f"- [[{relative_path}]] ({score:.1%})\n")
        print(f"✅ Resultados salvos em: {filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo Markdown: {e}")


if __name__ == "__main__":
    print("OBSIDIAN NOTE LINKER")
    print("=" * 40)
    
    try:
        from config import MAIN_PATH
        linker = NoteLinker(MAIN_PATH)
        linker.load_notes()
        
        print(f"\nLoaded {len(linker.notes)} notes from vault")
        print("\nEnter note path (e.g., 'Projetos/ideias.md')")
        print(f"Threshold (default: {SIMILARITY_THRESHOLD})")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                user_input = input(">> ").strip()
                if user_input.lower() in ('exit', 'quit', 'q'):
                    break
                    
                parts = user_input.split()
                note_path = parts[0]
                threshold = float(parts[1]) if len(parts) > 1 else SIMILARITY_THRESHOLD
                
                results = linker.find_similar(note_path, threshold)
                display_results(note_path, results)

                if results:
                    save_input = input("💾 Deseja salvar os resultados em um arquivo Markdown? (s/n): ").strip().lower()
                    if save_input == 's':
                        save_markdown(note_path, results)

            except Exception as e:
                print(f"Error: {e}")
                
    except ImportError:
        print("Error: Could not find config.py with MAIN_PATH")
    except Exception as e:
        print(f"Fatal error: {e}")
