import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar 

def janela_itens_pedido():
    janela = tk.Toplevel()
    janela.title("Gerenciar Itens do Pedido")
    janela.geometry("900x550")

    # --- Funções de Lógica (Adaptadas para a estrutura de 2 tabelas) ---
    
    def carregar_listas_dropdown():
        """Carrega as listas de pedidos e produtos para os comboboxes."""
        try:
            conn = conectar()
            cur = conn.cursor()
            
            # --- Alteração para Pedidos ---
            cur.execute("SELECT pedidoid, clienteid FROM amazon.pedido ORDER BY pedidoid")
            pedidos = cur.fetchall()
            
            # Lista para o formulário (continua igual)
            valores_pedidos = [f"{p[0]} - (Cliente {p[1]})" for p in pedidos]
            cb_pedido['values'] = valores_pedidos
            
            # NOVA LISTA - Apenas com os IDs dos pedidos para o filtro
            valores_filtro_pedidos = [p[0] for p in pedidos]
            cb_filtro_pedido['values'] = valores_filtro_pedidos # Atribui a nova lista ao filtro

            # --- Carrega Produtos (sem alteração) ---
            cur.execute("SELECT produtoid, nomeproduto FROM amazon.produto ORDER BY nomeproduto")
            produtos = cur.fetchall()
            valores_produtos = [f"{p[0]} - {p[1]}" for p in produtos]
            cb_produto['values'] = valores_produtos
            cb_filtro_produto['values'] = valores_produtos # Aqui pode manter, pois o formato é útil

            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar dados iniciais: {e}")

    def carregar_tabela(pedido_id=None, produto_id=None):
        """Carrega a tabela principal com os itens do pedido."""
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            
            # Query simplificada para buscar apenas da tabela de associação
            query = "SELECT pp.pedidoid, pp.produtoid FROM amazon.pedido_produto AS pp"
            
            params = []
            conditions = []
            if pedido_id:
                conditions.append("pp.pedidoid = %s")
                params.append(pedido_id)
            if produto_id:
                conditions.append("pp.produtoid = %s")
                params.append(produto_id)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY pp.pedidoid, pp.produtoid"
            cur.execute(query, tuple(params))
            
            for row in cur.fetchall():
                # Insere apenas os dois valores na tabela
                tree.insert("", "end", values=row) 
                
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Itens", str(e))

    def adicionar_item():
        """Adiciona um link produto-pedido."""
        pedido_str = cb_pedido.get()
        produto_str = cb_produto.get()
        
        if not (pedido_str and produto_str): # Checa apenas pedido e produto
            messagebox.showwarning("Atenção", "Selecione um Pedido e um Produto.")
            return
        try:
            pedido_id = int(pedido_str.split(" - ")[0])
            produto_id = int(produto_str.split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showwarning("Erro de Formato", "Pedido ou Produto inválidos.")
            return
        
        try:
            conn = conectar()
            cur = conn.cursor()
            # Insere apenas o link entre produto e pedido
            cur.execute("INSERT INTO amazon.pedido_produto (pedidoid, produtoid) VALUES (%s, %s)", (pedido_id, produto_id))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto inserido no pedido!") # Mensagem simplificada
            
            cur.close()
            conn.close()
            limpar_campos()
            carregar_tabela()
        except Exception as e:
            messagebox.showerror("Erro de Inserção", f"Não foi possível inserir o produto no pedido.\nVerifique se este produto já não está neste pedido.\n\nDetalhes: {e}")

    def remover_item():
        """Remove apenas o link entre o produto e o pedido."""
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item da lista para remover.")
            return
        valores = tree.item(item_selecionado)["values"]
        pedido_id, produto_id = valores[0], valores[1]
        
        # Mensagem de confirmação ajustada
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o produto {produto_id} do pedido {pedido_id}?"):
            try:
                # O resto da função continua igual...
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM amazon.pedido_produto WHERE pedidoid = %s AND produtoid = %s", (pedido_id, produto_id))
                conn.commit()
                cur.close()
                conn.close()
                limpar_campos()
                carregar_tabela()
            except Exception as e:
                messagebox.showerror("Erro ao Remover", str(e))

    # def atualizar_quantidade():
    #     """Atualiza a quantidade GERAL do pedido, não de um item específico."""
    #     pedido_str = cb_pedido.get()
    #     quantidade_str = entry_quantidade.get()
    #     if not (pedido_str and quantidade_str):
    #         messagebox.showwarning("Aviso", "Para atualizar, selecione um pedido e informe a nova quantidade.")
    #         return
    #     try:
    #         pedido_id = int(pedido_str.split(" - ")[0])
    #         qtde = int(quantidade_str)
    #     except (ValueError, IndexError):
    #         messagebox.showwarning("Erro de Formato", "Pedido ou Quantidade inválidos.")
    #         return

    #     try:
    #         conn = conectar()
    #         cur = conn.cursor()
    #         # Atualiza a quantidade na tabela de quantidade
    #         cur.execute("UPDATE amazon.pedido_quantidade SET quantiadeprod = %s WHERE pedidoid = %s", (qtde, pedido_id))
    #         if cur.rowcount == 0:
    #             # Se nenhum registro foi atualizado (porque não existia), insere.
    #             cur.execute("INSERT INTO amazon.pedido_quantidade (pedidoid, quantiadeprod) VALUES (%s, %s)", (pedido_id, qtde))

    #         conn.commit()
    #         cur.close()
    #         conn.close()
    #         limpar_campos()
    #         carregar_tabela()
    #         messagebox.showinfo("Sucesso", f"Quantidade geral do pedido {pedido_id} atualizada para {qtde}.")
    #     except Exception as e:
    #         messagebox.showerror("Erro ao Atualizar", str(e))

    # --- Funções da Interface ---
    def filtrar_itens():
        pedido_str = cb_filtro_pedido.get()
        produto = cb_filtro_produto.get()

        pedido_id = int(pedido_str) if pedido_str else None
        
        produto_id = int(produto.split(" - ")[0]) if produto else None
        carregar_tabela(pedido_id, produto_id)

    def preencher_campos_selecao(event):
        item_selecionado = tree.selection()
        if not item_selecionado:
            return
        
        limpar_campos(limpar_selecao=False)
        valores = tree.item(item_selecionado)["values"]
        
        pedido_texto = next((p for p in cb_pedido['values'] if p.startswith(f"{valores[0]} -")), "")
        produto_texto = next((p for p in cb_produto['values'] if p.startswith(f"{valores[1]} -")), "")
        
        cb_pedido.set(pedido_texto)
        cb_produto.set(produto_texto)
        # entry_quantidade.insert(0, valores[2])

    def limpar_campos(limpar_selecao=True):
        cb_pedido.set("")
        cb_produto.set("")
        # entry_quantidade.delete(0, tk.END)
        cb_filtro_pedido.set("")
        cb_filtro_produto.set("")
        if limpar_selecao and tree.selection():
            tree.selection_remove(tree.selection()[0])

    # --- Interface Gráfica (UI) - Padronizada ---
    
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Pedido:").grid(row=0, column=0, padx=5, pady=5)
    cb_pedido = ttk.Combobox(form_frame, width=30)
    cb_pedido.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(form_frame, text="Produto:").grid(row=0, column=2, padx=5, pady=5)
    cb_produto = ttk.Combobox(form_frame, width=35)
    cb_produto.grid(row=0, column=3, padx=5, pady=5)
    
    # tk.Label(form_frame, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
    # entry_quantidade = tk.Entry(form_frame, width=33)
    # entry_quantidade.grid(row=1, column=1, padx=5, pady=5)
    
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Adicionar Item", command=adicionar_item).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Remover Item", command=remover_item).pack(side=tk.LEFT, padx=10)
    # tk.Button(btn_frame, text="Atualizar Quantidade", command=atualizar_quantidade).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)
    
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)
    
    tk.Label(filtro_frame, text="Filtrar por Pedido:").pack(side=tk.LEFT)
    cb_filtro_pedido = ttk.Combobox(filtro_frame, width=30)
    cb_filtro_pedido.pack(side=tk.LEFT, padx=5)
    
    tk.Label(filtro_frame, text="Produto:").pack(side=tk.LEFT)
    cb_filtro_produto = ttk.Combobox(filtro_frame, width=35)
    cb_filtro_produto.pack(side=tk.LEFT, padx=5)
    
    tk.Button(filtro_frame, text="Buscar", command=filtrar_itens).pack(side=tk.LEFT, padx=10)

    # Tabela de visualização
    tree_frame = tk.Frame(janela, padx=10, pady=10)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    colunas = ("PedidoID", "ProdutoID") # , "Quantidade"
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    tree.heading("PedidoID", text="ID do Pedido")
    tree.heading("ProdutoID", text="ID do Produto")
    # tree.heading("Quantidade", text="Quantidade (Geral do Pedido)")
    tree.column("PedidoID", width=150, anchor='center')
    tree.column("ProdutoID", width=150, anchor='center')
    # tree.column("Quantidade", width=200, anchor='center')
    
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(expand=True, fill=tk.BOTH)
    
    tree.bind("<<TreeviewSelect>>", preencher_campos_selecao)
    
    # Carregamento inicial
    carregar_listas_dropdown()
    carregar_tabela()