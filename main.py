# Menu principal
import tkinter as tk
from cliente_crud import janela_cliente
from pedido_crud import janela_pedido
from produto_crud import janela_produto
from transportadora_crud import janela_transportadora
from loja_crud import janela_loja
from cli_loja import janela_cli_loja
from ped_prod_crud import janela_itens_pedido
# from ped_quant_crud import janela_ped_quant
from consultas import janela_consultas

def abrir_cliente():
    janela_cliente()

def abrir_pedido():
    janela_pedido()

def abrir_produto():
    janela_produto()

def abrir_transportadora():
    janela_transportadora()

def abrir_loja():
    janela_loja()

def abrir_cli_loja():
    janela_cli_loja()

def abrir_consultas():
    janela_consultas()

def abrir_ped_prod(): 
    janela_itens_pedido()

# def abrir_ped_quant():
#     janela_ped_quant()

root = tk.Tk()
root.title("Sistema de Gerenciamento - Amazon")
root.geometry("400x500")

tk.Label(root, text="Menu Principal", font=("Arial", 16)).pack(pady=20)

btn_produto = tk.Button(root, text="Gerenciar Produtos", command=abrir_produto, width=30)
btn_produto.pack(pady=10)

btn_cliente = tk.Button(root, text="Gerenciar Clientes", command=abrir_cliente, width=30)
btn_cliente.pack(pady=10)

btn_pedido = tk.Button(root, text="Adicionar Pedido", command=abrir_pedido, width=30)
btn_pedido.pack(pady=10)

btn_ped_prod = tk.Button(root, text="Gerenciar Itens do Pedido", command=abrir_ped_prod, width=30)
btn_ped_prod.pack(pady=10) 

# btn_ped_quant = tk.Button(root, text="Gerenciar Quantidade do Pedido", command=abrir_ped_quant, width=30)
# btn_ped_quant.pack(pady=10)

btn_pedido = tk.Button(root, text="Gerenciar Transportadora", command=abrir_transportadora, width=30)
btn_pedido.pack(pady=10)

btn_pedido = tk.Button(root, text="Gerenciar Loja", command=abrir_loja, width=30)
btn_pedido.pack(pady=10)

btn_pedido = tk.Button(root, text="Gerenciar Cliente Avalia Loja", command=abrir_cli_loja, width=30)
btn_pedido.pack(pady=10)

btn_consultas = tk.Button(root, text="Consultas SQL", command=abrir_consultas, width=30)
btn_consultas.pack(pady=10)


root.mainloop()
