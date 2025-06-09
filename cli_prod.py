import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar 

def janela_cli_prod():
    janela = tk.Toplevel()
    janela.title("Gerenciar Cliente Avalia Produto")
    janela.geometry("900x500")

    def carregar_clientes_produtos():
        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("SELECT ClienteID, NomeCliente FROM amazon.cliente ORDER BY NomeCliente")
            clientes = cur.fetchall()
            cb_cliente['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

            cur.execute("SELECT ProdutoID, NomeProduto FROM amazon.produto ORDER BY NomeProduto")
            produtos = cur.fetchall()
            cb_produto['values'] = [f"{p[0]} - {p[1]}" for p in produtos]

            cb_filtro_cliente['values'] = cb_cliente['values']
            cb_filtro_produto['values'] = cb_produto['values']

            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dados(cliente_id=None, produto_id=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if cliente_id and produto_id:
                cur.execute("""
                    SELECT * FROM amazon.cli_avalia_prod 
                    WHERE clienteid = %s AND produtoid = %s
                """, (cliente_id, produto_id))
            elif cliente_id:
                cur.execute("SELECT * FROM amazon.cli_avalia_prod WHERE clienteid = %s", (cliente_id,))
            elif produto_id:
                cur.execute("SELECT * FROM amazon.cli_avalia_prod WHERE produtoid = %s", (produto_id,))
            else:
                cur.execute("SELECT * FROM amazon.cli_avalia_prod")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def inserir_avaliacao():
        nota = entry_nota.get()
        data = entry_data.get()
        comentario = entry_comentario.get()
        cliente = cb_cliente.get()
        produto = cb_produto.get()

        if not (nota and data and cliente and produto):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            cliente_id = int(cliente.split(" - ")[0])
            produto_id = int(produto.split(" - ")[0])
        except:
            messagebox.showwarning("Erro", "Selecione cliente e produto válidos.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.cli_avalia_prod 
                (ClienteID, ProdutoID, nota, data, comentario)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, produto_id, nota, data, comentario))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Avaliação inserida com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_avaliacao():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma avaliação para deletar.")
            return
        cliente_id = tree.item(item)["values"][0]
        produto_id = tree.item(item)["values"][1]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.cli_avalia_prod WHERE clienteid = %s AND produtoID = %s", (cliente_id, produto_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Avaliação deletada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_avaliacao():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma avaliação para atualizar.")
            return

        try:
            cliente_id = int(cb_cliente.get().split(" - ")[0])
            produto_id = int(cb_produto.get().split(" - ")[0])
        except:
            messagebox.showwarning("Erro", "Selecione cliente e produto válidos.")
            return

        nota = entry_nota.get()
        data = entry_data.get()
        comentario = entry_comentario.get()

        if not (nota and data):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.cli_avalia_prod 
                SET nota = %s, data = %s, comentario = %s
                WHERE clienteid = %s AND produtoid = %s
            """, (nota, data, comentario, cliente_id, produto_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Avaliação atualizada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_avaliacoes():
        cliente = cb_filtro_cliente.get()
        produto = cb_filtro_produto.get()

        cliente_id = None 
        produto_id = None

        if cliente:
            try:
                cliente_id = int(cliente.split(" - ")[0])
            except:
                pass
        if produto:
            try:
                produto_id = int(produto.split(" - ")[0])
            except:
                pass

        carregar_dados(cliente_id, produto_id)

    def preencher_campos(event):
        item = tree.selection()
        if not item:
            return
        valores = tree.item(item)["values"]
        cb_cliente.set(f"{valores[0]}") 
        cb_produto.set(f"{valores[1]}")    
        entry_nota.delete(0, tk.END)
        entry_nota.insert(0, valores[2])
        entry_data.delete(0, tk.END)
        entry_data.insert(0, valores[3])
        entry_comentario.delete(0, tk.END)
        entry_comentario.insert(0, valores[4])

    def limpar_campos():
        cb_cliente.set("")
        cb_produto.set("")
        entry_nota.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        entry_comentario.delete(0, tk.END)
        cb_filtro_cliente.set("")
        cb_filtro_produto.set("")
        tree.selection_remove(tree.selection())

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Cliente:").grid(row=0, column=0)
    cb_cliente = ttk.Combobox(form_frame, width=25)
    cb_cliente.grid(row=0, column=1)

    tk.Label(form_frame, text="Produto:").grid(row=0, column=2)
    cb_produto = ttk.Combobox(form_frame, width=25)
    cb_produto.grid(row=0, column=3)

    tk.Label(form_frame, text="Nota:").grid(row=1, column=0)
    entry_nota = tk.Entry(form_frame, width=28)
    entry_nota.grid(row=1, column=1)

    tk.Label(form_frame, text="Data Pedido (YYYY-MM-DD):").grid(row=1, column=2)
    entry_data = tk.Entry(form_frame, width=28)
    entry_data.grid(row=1, column=3)

    tk.Label(form_frame, text="Comentário:").grid(row=2, column=0)
    entry_comentario = tk.Entry(form_frame, width=28)
    entry_comentario.grid(row=2, column=1)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Avaliação", command=inserir_avaliacao).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionado", command=atualizar_avaliacao).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_avaliacao).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por Cliente:").pack(side=tk.LEFT)
    cb_filtro_cliente = ttk.Combobox(filtro_frame, width=30)
    cb_filtro_cliente.pack(side=tk.LEFT, padx=5)

    tk.Label(filtro_frame, text="Filtrar por Produto:").pack(side=tk.LEFT)
    cb_filtro_produto = ttk.Combobox(filtro_frame, width=30)
    cb_filtro_produto.pack(side=tk.LEFT, padx=5)

    tk.Button(filtro_frame, text="Buscar", command=filtrar_avaliacoes).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("ClienteID", "ProdutoID", "nota", "data", "comentario")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill=tk.BOTH)

    # Bind para preencher os campos ao selecionar uma linha
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    carregar_clientes_produtos()
    carregar_dados()
    janela.mainloop()
