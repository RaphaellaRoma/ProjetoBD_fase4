import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_produto():
    janela = tk.Toplevel()
    janela.title("Gerenciar Produtos")
    janela.geometry("900x500")

    # --- FUNÇÕES DE LÓGICA ---

    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            query = "SELECT * FROM amazon.produto"
            params = ()

            if filtro:
                filtro_texto = f"%{filtro}%"
                query += """
                    WHERE CAST(produtoid AS TEXT) LIKE %s 
                    OR nomeproduto ILIKE %s 
                    OR tipoproduto ILIKE %s 
                    OR descricao ILIKE %s
                """
                params = (f"{filtro}%", filtro_texto, filtro_texto, filtro_texto)
            
            query += " ORDER BY produtoid"
            cur.execute(query, params)
            
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", str(e))

    def inserir_produto():
        nome = entry_nome.get()
        tipo = entry_tipo.get()
        descricao_val = entry_descricao.get()
        preco_val = entry_preco.get() 
        loja_id = entry_loja_id.get()

        if not all([nome, tipo, preco_val, loja_id]):
            messagebox.showwarning("Atenção", "Preencha pelo menos Nome, Tipo, Preço e LojaID.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.produto (nomeproduto, tipoproduto, descricao, preco, lojaid)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, tipo, descricao_val, float(preco_val), int(loja_id)))
            conn.commit()
            cur.close()
            conn.close()
            limpar_campos()
            carregar_dados()
            messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Inserir", str(e))

    def deletar_produto():
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para deletar.")
            return
        
        produto_id = tree.item(item_selecionado)["values"][0]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o produto ID {produto_id}?"):
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM amazon.produto WHERE produtoid = %s", (produto_id,))
                conn.commit()
                cur.close()
                conn.close()
                limpar_campos()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro ao Deletar", str(e))

    def atualizar_produto():
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto da lista para atualizar.")
            return

        nome = entry_nome.get()
        tipo = entry_tipo.get()
        descricao_val = entry_descricao.get()
        preco_val = entry_preco.get()
        loja_id = entry_loja_id.get()

        if not all([nome, tipo, preco_val, loja_id]):
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos para atualizar.")
            return

        produto_id = tree.item(item_selecionado)["values"][0]

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.produto 
                SET nomeproduto = %s, tipoproduto = %s, descricao = %s, preco = %s, lojaid = %s
                WHERE produtoid = %s
            """, (nome, tipo, descricao_val, float(preco_val), int(loja_id), produto_id))
            conn.commit()
            cur.close()
            conn.close()
            limpar_campos()
            carregar_dados()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Atualizar", str(e))

    def preencher_campos(event):
        limpar_campos(limpar_selecao=False)
        item_selecionado = tree.selection()
        if not item_selecionado:
            return
        valores = tree.item(item_selecionado)["values"]
        entry_nome.insert(0, valores[1])
        entry_tipo.insert(0, valores[2])
        entry_descricao.insert(0, valores[3])
        entry_preco.insert(0, valores[4])
        entry_loja_id.insert(0, valores[6])

    def limpar_campos(limpar_selecao=True):
        entry_nome.delete(0, tk.END)
        entry_tipo.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_loja_id.delete(0, tk.END)
        entry_nome.focus()
        if limpar_selecao and tree.selection():
            tree.selection_remove(tree.selection()[0])

    # --- INTERFACE GRÁFICA (UI) ---

    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(form_frame)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(form_frame, text="Tipo:").grid(row=0, column=2, padx=5, pady=5)
    entry_tipo = tk.Entry(form_frame)
    entry_tipo.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
    entry_descricao = tk.Entry(form_frame)
    entry_descricao.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(form_frame, text="Preço:").grid(row=1, column=2, padx=5, pady=5)
    entry_preco = tk.Entry(form_frame)
    entry_preco.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Loja ID:").grid(row=2, column=0, padx=5, pady=5)
    entry_loja_id = tk.Entry(form_frame)
    entry_loja_id.grid(row=2, column=1, padx=5, pady=5)

    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Inserir Produto", command=inserir_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionado", command=atualizar_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)
    tk.Label(filtro_frame, text="Filtrar por Nome ou ID:").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", lambda event: carregar_dados(entry_filtro.get()))

    tree_frame = tk.Frame(janela)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    colunas = ("produtoid", "nomeproduto", "tipoproduto", "descricao", "preco", "avaliaçãogeral", "lojaid")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    
    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120, anchor='w')
    
    tree.pack(expand=True, fill=tk.BOTH)
    
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    carregar_dados()