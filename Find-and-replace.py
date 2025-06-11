import os
from typing import List


def replace_text_in_md_files(root_dir: str, old_text: str, new_text: str) -> List[str]:
    """
    Replace all occurrences of old_text with new_text in .md files within root_dir and its subdirectories.
    
    Args:
        root_dir: The root directory to search for .md files
        old_text: The text to be replaced
        new_text: The replacement text
        
    Returns:
        A list of paths to modified files
    """
    modified_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in (f for f in filenames if f.endswith(".md")):
            filepath = os.path.join(dirpath, filename)
            
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                
                if old_text in content:
                    new_content = content.replace(old_text, new_text)
                    
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(new_content)
                    
                    modified_files.append(filepath)
            except (IOError, UnicodeDecodeError) as e:
                print(f"⚠️ Error processing {filepath}: {str(e)}")
                continue

    return modified_files


def print_modified_files_report(modified_files: List[str]) -> None:
    """Print a report of modified files."""
    print("\nModified files:")
    if modified_files:
        for filepath in modified_files:
            print(f"✅ {filepath}")
    else:
        print("No occurrences found.")


if __name__ == "__main__":
    # Example usage
    modified = replace_text_in_md_files(
        root_dir="PATH/to/your/notes",  # ← Replace with the correct path
        old_text="[[System/HUB/hub-tec]]",
        new_text="[[hub-tec]]"
    )
    print_modified_files_report(modified)