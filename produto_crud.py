import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_produto():
    janela = tk.Toplevel()
    janela.title("Gerenciar Produtos")
    janela.geometry("900x500")

    # Função para carregar os dados na tabela (Treeview)
    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if filtro:
                # Filtrar por ID ou Nome do Produto
                cur.execute("""
                    SELECT * FROM amazon.produto 
                    WHERE CAST(ProdutoID AS TEXT) LIKE %s OR NomeProduto ILIKE %s
                """, (f"{filtro}%", f"%{filtro}%"))
            else:
                cur.execute("SELECT * FROM amazon.produto ORDER BY ProdutoID")
            
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", str(e))

    # Função para inserir um novo produto
    def inserir_produto():
        nome = entry_nome.get()
        tipo = entry_tipo.get()
        descricao = entry_descricao.get()
        preco = entry_preco.get()
        loja_id = entry_loja_id.get()

        if not all([nome, tipo, preco, loja_id]):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (Nome, Tipo, Preço, LojaID).")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.produto (NomeProduto, TipoProduto, Descrição, Preço, LojaID)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, tipo, descricao, float(preco), int(loja_id)))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados() # Recarrega a lista de produtos
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro ao Inserir", str(e))

    # Função para deletar um produto selecionado
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
                cur.execute("DELETE FROM amazon.produto WHERE ProdutoID = %s", (produto_id,))
                conn.commit()
                cur.close()
                conn.close()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o produto. Verifique se ele não está associado a um pedido.\n\nDetalhes: {e}")


    # Função para limpar os campos do formulário
    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_tipo.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_loja_id.delete(0, tk.END)

    # === Formulário de Inserção/Edição ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    entry_nome = tk.Entry(form_frame, width=40)
    entry_nome.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

    tk.Label(form_frame, text="Tipo:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
    entry_tipo = tk.Entry(form_frame)
    entry_tipo.grid(row=0, column=3, sticky="ew", padx=5, pady=2)

    tk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    entry_descricao = tk.Entry(form_frame)
    entry_descricao.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
    
    tk.Label(form_frame, text="Preço:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
    entry_preco = tk.Entry(form_frame)
    entry_preco.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

    tk.Label(form_frame, text="Loja ID:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    entry_loja_id = tk.Entry(form_frame)
    entry_loja_id.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Inserir Produto", command=inserir_produto).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_produto).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10, fill="x", padx=10)
    tk.Label(filtro_frame, text="Filtrar por Nome ou ID:").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
    entry_filtro.bind("<KeyRelease>", lambda event: carregar_dados(entry_filtro.get()))

    # === Tabela (Treeview) ===
    tree_frame = tk.Frame(janela)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    colunas = ("ProdutoID", "NomeProduto", "TipoProduto", "Descrição", "Preço", "AvaliaçãoGeral", "LojaID")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    
    # Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='w')
    
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_dados()
    janela.mainloop()