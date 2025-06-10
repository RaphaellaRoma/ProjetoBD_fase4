# Menu principal estilizado com 3 colunas
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from cliente_crud import janela_cliente
from pedido_crud import janela_pedido
from produto_crud import janela_produto
from transportadora_crud import janela_transportadora
from loja_crud import janela_loja
from cli_loja import janela_cli_loja
from cli_prod import janela_cli_prod
# O nome do arquivo foi deduzido da conversa anterior, ajuste se necessário
from ped_prod_crud import janela_itens_pedido 
from ped_quant_crud import janela_ped_quant

def abrir_cliente(): janela_cliente()
def abrir_pedido(): janela_pedido()
def abrir_produto(): janela_produto()
def abrir_transportadora(): janela_transportadora()
def abrir_loja(): janela_loja()
def abrir_cli_loja(): janela_cli_loja()
def abrir_cli_prod(): janela_cli_prod()

def abrir_ped_prod(): 
    janela_itens_pedido()

def abrir_ped_quant():
    janela_ped_quant()

root = tk.Tk()
root.title("Sistema de Gerenciamento - Amazon")
root.geometry("950x550") # Aumentei um pouco a altura para o novo botão

# === Logo ===
imagem = Image.open("amazon_logo.png")
imagem = imagem.resize((335, 130))
logo = ImageTk.PhotoImage(imagem)
tk.Label(root, image=logo).pack(pady=(10, 0))

# === Título ===
tk.Label(root, text="Sistema de Gerenciamento", font=("Segoe UI", 20, "bold"), fg="#17191B").pack(pady=5)
tk.Label(root, text="Escolha a tabela que deseja gerenciar ( inserir, deletar, atualizar, filtrar ):", font=("Segoe UI", 14), fg="#17191B").pack(pady=5)

# === Estilo de Botão ===
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
    font=("Segoe UI", 13),
    padding=10,
    width=28, # Aumentei a largura para caber os novos textos
    relief="flat",
    background="#232F3E",
    foreground="white"
)
style.map("TButton",
    background=[("active", "#EC8E00")]
)

# === Criar botão (sem empacotar) ===
def criar_botao(texto, comando):
    return ttk.Button(btn_frame, text=texto, command=comando, style="TButton")

# === Frame dos botões (3 colunas) ===
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

# === Lista com textos e comandos (ATUALIZADA) ===
botoes_info = [
    ("Clientes", abrir_cliente),
    ("Lojas", abrir_loja),
    ("Transportadoras", abrir_transportadora),
    ("Produtos", abrir_produto),
    ("Pedidos", abrir_pedido),
    ("Itens do Pedido (Pedido-Produto)", abrir_ped_prod),
    ("Quantidade do Pedido", abrir_ped_quant),
    ("Avaliações (cliente-loja)", abrir_cli_loja),
    ("Avaliações (cliente-produto)", abrir_cli_prod),
]

# === Criar e posicionar botões ===
for i, (texto, comando) in enumerate(botoes_info):
    row = i // 3
    col = i % 3
    btn = criar_botao(texto, comando)
    btn.grid(row=row, column=col, padx=15, pady=10)

root.mainloop()