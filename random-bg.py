deimport requests
import random
import json
from bs4 import BeautifulSoup

def get_random_wallhaven_image():
    # URL do toplist do Wallhaven (pode ajustar a página ou categoria se desejar)
    url = "https://wallhaven.cc/random"
    
    try:
        # Fazer requisição à página
        response = requests.get(url)
        response.raise_for_status()
        
        # Parsear o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todos os links das thumbnails
        thumbnails = soup.find_all('a', class_='preview')
        
        if not thumbnails:
            print("Nenhuma imagem encontrada na página.")
            return None
        
        # Escolher uma imagem aleatória
        random_thumbnail = random.choice(thumbnails)
        wallpaper_url = random_thumbnail['href']
        
        # Obter a página da imagem para pegar a URL completa
        wallpaper_response = requests.get(wallpaper_url)
        wallpaper_response.raise_for_status()
        
        wallpaper_soup = BeautifulSoup(wallpaper_response.text, 'html.parser')
        image_element = wallpaper_soup.find('img', id='wallpaper')
        
        if not image_element:
            print("Não foi possível encontrar a imagem na página do wallpaper.")
            return None
        
        image_url = image_element['src']
        return image_url
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o Wallhaven: {e}")
        return None

def update_obsidian_background(json_path, new_image_url):
    try:
        # Ler o arquivo JSON existente
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Atualizar a URL da imagem
        data['imageUrl'] = new_image_url
        
        # Escrever de volta no arquivo
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"Arquivo {json_path} atualizado com sucesso!")
        return True
    
    except Exception as e:
        print(f"Erro ao atualizar o arquivo JSON: {e}")
        return False

if __name__ == "__main__":
    # Caminho para o arquivo data.json (ajuste conforme necessário)
    json_path = r"C:\Users\desktop\Documents\Thoughts\.obsidian\plugins\background-image\data.json"
    
    print("Buscando uma nova imagem no Wallhaven...")
    new_image_url = get_random_wallhaven_image()
    
    if new_image_url:
        print(f"Nova imagem encontrada: {new_image_url}")
        success = update_obsidian_background(json_path, new_image_url)
        
        if success:
            print("Background atualizado com sucesso!")
        else:
            print("Falha ao atualizar o background.")
    else:
        print("Não foi possível obter uma nova imagem.")