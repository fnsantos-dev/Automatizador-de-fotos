import requests
import os
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

def baixar_imagens_principais_anuncio(url_anuncio, pasta_destino):
    # Faz a solicitação HTTP para obter o conteúdo da página do anúncio
    response = requests.get(url_anuncio)
    soup = BeautifulSoup(response.content, "html.parser")
    
    elementos_imagem = soup.find_all("img", class_="slide__image usedmodel-showcase__slide-image")
    
    for img in elementos_imagem:
        # Obtém a URL da imagem
        url_imagem = img["src"]
        
        response_imagem = requests.get(url_imagem)
        
        # Obtém o nome do arquivo da URL
        nome_arquivo = url_imagem.split("/")[-1]
        
        # Define o caminho completo do arquivo de destino
        caminho_destino = os.path.join(pasta_destino, nome_arquivo)
        
        # Salva a imagem no arquivo de destino
        with open(caminho_destino, "wb") as arquivo:
            arquivo.write(response_imagem.content)
        
        print(f"Imagem baixada: {caminho_destino}")

def excluir_imagens(pasta_destino):
    # Verifica se a pasta de destino existe
    if os.path.exists(pasta_destino):
        # Lista todos os arquivos na pasta
        arquivos = os.listdir(pasta_destino)
        
        # Exclui cada arquivo encontrado
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_destino, arquivo)
            os.remove(caminho_arquivo)
        
        print("Imagens excluídas com sucesso.")
    else:
        print("A pasta de destino não existe.")

def selecionar_pasta_destino():
    pasta_destino = filedialog.askdirectory()
    pasta_destino_entry.delete(0, tk.END)
    pasta_destino_entry.insert(0, pasta_destino)

def baixar_imagens():
    url_anuncio = url_anuncio_entry.get()
    pasta_destino = pasta_destino_entry.get()
    baixar_imagens_principais_anuncio(url_anuncio, pasta_destino)

def excluir_imagens_pasta():
    pasta_destino = pasta_destino_entry.get()
    excluir_imagens(pasta_destino)

# Cria a janela principal
window = tk.Tk(baseName=base)
window.title("Baixar Imagens")
window.geometry("400x200")

# Label e Entry para a URL do anúncio
url_anuncio_label = tk.Label(window, text="URL do site do carro:")
url_anuncio_label.pack()
url_anuncio_entry = tk.Entry(window, width=40)
url_anuncio_entry.pack()

# Label e Entry para a pasta de destino
pasta_destino_label = tk.Label(window, text="Pasta de destino:")
pasta_destino_label.pack()
pasta_destino_entry = tk.Entry(window, width=40)
pasta_destino_entry.pack()
selecionar_pasta_destino_button = tk.Button(window, text="Selecionar Pasta", command=selecionar_pasta_destino)
selecionar_pasta_destino_button.pack()

# Botão para baixar as imagens
baixar_imagens_button = tk.Button(window, text="Baixar Imagens", command=baixar_imagens)
baixar_imagens_button.pack()

# Botão para excluir as imagens
excluir_imagens_button = tk.Button(window, text="Excluir Imagens", command=excluir_imagens_pasta)
excluir_imagens_button.pack()

# Inicia o loop de eventos da janela
window.mainloop()