import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_produto():
    janela = tk.Toplevel()
    janela.title("Gerenciar Produtos")
    janela.geometry("1000x500")

    def carregar_lojas():
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT LojaID, NomeLoja FROM amazon.loja ORDER BY NomeLoja")
            lojas = cur.fetchall()
            cb_loja['values'] = [f"{l[0]} - {l[1]}" for l in lojas]
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if filtro:
                cur.execute("""
                    SELECT * FROM amazon.produto 
                    WHERE CAST(ProdutoID AS TEXT) LIKE %s OR TipoProduto ILIKE %s OR NomeProduto ILIKE %s
                    ORDER BY ProdutoID
                """, (f"{filtro}%",f"{filtro}%",f"{filtro}%"))
            else:
                cur.execute("SELECT * FROM amazon.produto ORDER BY ProdutoID")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos():
        cb_tipo.set("")
        entry_nome.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_avaliacao.delete(0, tk.END)
        cb_loja.set("")
        tree.selection_remove(tree.selection())

    def inserir_produto():
        tipo = cb_tipo.get()
        nome = entry_nome.get()
        descricao = entry_desc.get()
        preco = entry_preco.get()
        avaliacao = entry_avaliacao.get()
        loja = cb_loja.get()

        if not (tipo and nome and preco and loja):
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return

        try:
            loja_id = int(loja.split(" - ")[0])
        except:
            messagebox.showwarning("Erro", "Selecione uma loja válida.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.produto 
                (TipoProduto, NomeProduto, Descricao, Preco, AvaliacaoGeral, LojaID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tipo, nome, descricao, preco, avaliacao, loja_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_produto():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return
        produto_id = tree.item(item)["values"][0]

        tipo = cb_tipo.get()
        nome = entry_nome.get()
        descricao = entry_desc.get()
        preco = entry_preco.get()
        avaliacao = entry_avaliacao.get()
        loja = cb_loja.get()

        try:
            loja_id = int(loja.split(" - ")[0])
        except:
            messagebox.showwarning("Erro", "Selecione uma loja válida.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.produto 
                SET TipoProduto = %s, NomeProduto = %s, Descricao = %s,
                    Preco = %s, AvaliacaoGeral = %s, LojaID = %s
                WHERE ProdutoID = %s
            """, (tipo, nome, descricao, preco, avaliacao, loja_id, produto_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_produto():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para deletar.")
            return
        produto_id = tree.item(item)["values"][0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.produto WHERE ProdutoID = %s", (produto_id,))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_produtos(event=None):
        termo = entry_filtro.get()
        carregar_dados(termo)

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item)["values"]
            cb_tipo.set(valores[1])
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, valores[2])
            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[3])
            entry_preco.delete(0, tk.END)
            entry_preco.insert(0, valores[4])
            entry_avaliacao.delete(0, tk.END)
            entry_avaliacao.insert(0, valores[5])
            cb_loja.set(f"{valores[6]}")

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Tipo de Produto:").grid(row=0, column=0)
    cb_tipo = ttk.Combobox(form_frame, values=["Eletrônico", "Roupas", "Livros", "Brinquedos", "Outros"], width=25)
    cb_tipo.grid(row=0, column=1)

    tk.Label(form_frame, text="Nome do Produto:").grid(row=0, column=2)
    entry_nome = tk.Entry(form_frame, width=28)
    entry_nome.grid(row=0, column=3)

    tk.Label(form_frame, text="Descrição:").grid(row=1, column=0)
    entry_desc = tk.Entry(form_frame, width=28)
    entry_desc.grid(row=1, column=1)

    tk.Label(form_frame, text="Preço:").grid(row=1, column=2)
    entry_preco = tk.Entry(form_frame, width=28)
    entry_preco.grid(row=1, column=3)

    tk.Label(form_frame, text="Avaliação Geral:").grid(row=2, column=0)
    entry_avaliacao = tk.Entry(form_frame, width=28)
    entry_avaliacao.grid(row=2, column=1)

    tk.Label(form_frame, text="Loja:").grid(row=2, column=2)
    cb_loja = ttk.Combobox(form_frame, width=25)
    cb_loja.grid(row=2, column=3)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Produto", command=inserir_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionado", command=atualizar_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por ID:").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", filtrar_produtos)
    tk.Button(filtro_frame, text="Buscar", command=filtrar_produtos).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("ProdutoID", "TipoProduto", "NomeProduto", "Descricao", "Preco", "AvaliacaoGeral", "LojaID")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=140 if col != "Descricao" else 200)
    tree.bind("<<TreeviewSelect>>", preencher_campos)
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_lojas()
    carregar_dados()
    janela.mainloop()
