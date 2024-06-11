import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import sys
import customtkinter as ctk

base = 'Win32GUI' if sys.platform == 'win32' else None

def baixar_imagens_principais_anuncio(url_anuncio, pasta_destino):
    response = requests.get(url_anuncio)
    soup = BeautifulSoup(response.content, "html.parser")
    
    elementos_imagem = soup.find_all("img", class_="slide__image usedmodel-showcase__slide-image")
    
    for img in elementos_imagem:
        #URL da imagem
        url_imagem = img["src"]
        
        response_imagem = requests.get(url_imagem)
        
        #Nome do arquivo da URL
        nome_arquivo = url_imagem.split("/")[-1]
        
        #Arquivo de destino
        caminho_destino = os.path.join(pasta_destino, nome_arquivo)
        
        #Salva a imagem no arquivo de destino
        with open(caminho_destino, "wb") as arquivo:
            arquivo.write(response_imagem.content)
        
        print(f"Imagem baixada: {caminho_destino}")
        
        #formato WebP
        if nome_arquivo.lower().endswith('.webp'):
            #imagem para JPEG
            imagem = Image.open(caminho_destino).convert("RGB")
            novo_nome_arquivo = os.path.splitext(nome_arquivo)[0] + '.jpg'
            caminho_destino_jpg = os.path.join(pasta_destino, novo_nome_arquivo)
            imagem.save(caminho_destino_jpg, "JPEG")
            
            #Remove a imagem original
            os.remove(caminho_destino)
            
            print(f"Imagem convertida para JPEG: {caminho_destino_jpg}")

def excluir_imagens(pasta_destino):
    #Verifica se a pasta de destino existe
    if os.path.exists(pasta_destino):
        #Lista todos os arquivos na pasta
        arquivos = os.listdir(pasta_destino)
        #Exclui cada arquivo encontrado
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

def limpar_url():
    url_anuncio_entry.delete(0, tk.END)

def baixar_imagens():
    url_anuncio = url_anuncio_entry.get()
    pasta_destino = pasta_destino_entry.get()
    baixar_imagens_principais_anuncio(url_anuncio, pasta_destino)

def excluir_imagens_pasta():
    pasta_destino = pasta_destino_entry.get()
    excluir_imagens(pasta_destino)

#Cria a janela principal
window = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
window.title("Qi Fotors")
window.geometry("600x500")

#Label e Entry para a URL do anúncio
url_anuncio_label = ctk.CTkLabel(window, text="URL do site do carro",font=("",20))
url_anuncio_label.pack(padx=10, pady=10)
url_anuncio_entry = ctk.CTkEntry(window, width=500)
url_anuncio_entry.pack(padx=10, pady=10)

#Botão para limpar a URL
limpar_url_button = ctk.CTkButton(window, text="Limpar URL", command=limpar_url,fg_color="#5e2d29")
limpar_url_button.pack(padx=10, pady=10)

#Label e Entry para a pasta de destino
pasta_destino_label = ctk.CTkLabel(window, text="Pasta de destino", font=("",20))
pasta_destino_label.pack(padx=10, pady=10)
pasta_destino_entry = ctk.CTkEntry(window, width=500)
pasta_destino_entry.pack(padx=10, pady=10)
selecionar_pasta_destino_button = ctk.CTkButton(window, text="Selecionar Pasta", command=selecionar_pasta_destino,fg_color="#23328e")
selecionar_pasta_destino_button.pack(padx=10, pady=10)

#Botão para baixar as imagens
baixar_imagens_button = ctk.CTkButton(window, text="Baixar Imagens", command=baixar_imagens,fg_color="#23328e")
baixar_imagens_button.pack(padx=10, pady=10)

#Botão para excluir as imagens
excluir_imagens_button = ctk.CTkButton(window, text="Excluir Imagens", command=excluir_imagens_pasta,fg_color="#5e2d29")
excluir_imagens_button.pack(padx=10, pady=10)

#Inicia o loop de eventos da janela
window.mainloop()