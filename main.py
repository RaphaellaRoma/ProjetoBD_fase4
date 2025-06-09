# Menu principal
import tkinter as tk
from cliente_crud import janela_cliente
from pedido_crud import janela_pedido
from consultas import janela_consultas

def abrir_cliente():
    janela_cliente()

def abrir_pedido():
    janela_pedido()

def abrir_consultas():
    janela_consultas()

root = tk.Tk()
root.title("Sistema de Gerenciamento - Amazon")
root.geometry("400x300")

tk.Label(root, text="Menu Principal", font=("Arial", 16)).pack(pady=20)

btn_cliente = tk.Button(root, text="Gerenciar Clientes", command=abrir_cliente, width=30)
btn_cliente.pack(pady=10)

btn_pedido = tk.Button(root, text="Adicionar Pedido", command=abrir_pedido, width=30)
btn_pedido.pack(pady=10)

btn_consultas = tk.Button(root, text="Consultas SQL", command=abrir_consultas, width=30)
btn_consultas.pack(pady=10)

root.mainloop()
