import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_ped_quant():
    janela = tk.Toplevel()
    janela.title("Gerenciar Quantidade Geral do Pedido")
    janela.geometry("800x500")

    # --- Funções de Lógica ---

    def carregar_pedidos_dropdown():
        """Carrega a lista de pedidos existentes para o ComboBox."""
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT pedidoid, clienteid FROM amazon.pedido ORDER BY pedidoid DESC")
            pedidos = cur.fetchall()
            valores_pedidos = [f"{p[0]} - (Cliente {p[1]})" for p in pedidos]
            cb_pedido['values'] = valores_pedidos
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar a lista de pedidos: {e}")

    def carregar_tabela(filtro_id=None):
        """Carrega a tabela com os dados de pedido_quantidade."""
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            query = "SELECT pedidoid, quantiadeprod FROM amazon.pedido_quantidade"
            params = ()
            if filtro_id:
                query += " WHERE CAST(pedidoid AS TEXT) LIKE %s"
                params = (f"{filtro_id}%",)
            
            query += " ORDER BY pedidoid DESC"
            cur.execute(query, params)
            
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
                
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", str(e))

    def salvar_quantidade():
        """Insere uma nova quantidade ou atualiza uma existente (UPSERT)."""
        pedido_str = cb_pedido.get()
        quantidade_str = entry_quantidade.get()
        
        if not (pedido_str and quantidade_str):
            messagebox.showwarning("Atenção", "Selecione um Pedido e informe a Quantidade.")
            return
        try:
            pedido_id = int(pedido_str.split(" - ")[0])
            qtde = int(quantidade_str)
        except (ValueError, IndexError):
            messagebox.showwarning("Erro de Formato", "Pedido ou Quantidade inválidos.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            # 1. Tenta ATUALIZAR primeiro
            cur.execute("UPDATE amazon.pedido_quantidade SET quantiadeprod = %s WHERE pedidoid = %s", (qtde, pedido_id))
            
            # 2. Se nenhuma linha foi atualizada (rowcount=0), significa que não existia. Então, INSERE.
            if cur.rowcount == 0:
                cur.execute("INSERT INTO amazon.pedido_quantidade (pedidoid, quantiadeprod) VALUES (%s, %s)", (pedido_id, qtde))
                messagebox.showinfo("Sucesso", f"Quantidade para o pedido {pedido_id} inserida com sucesso!")
            else:
                messagebox.showinfo("Sucesso", f"Quantidade do pedido {pedido_id} atualizada com sucesso!")

            conn.commit()
            cur.close()
            conn.close()
            limpar_campos()
            carregar_tabela()
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", str(e))

    def remover_quantidade():
        """Remove a entrada de quantidade para um pedido."""
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item da lista para remover.")
            return
            
        pedido_id = tree.item(item_selecionado)["values"][0]
        
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a quantidade do pedido {pedido_id}?"):
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM amazon.pedido_quantidade WHERE pedidoid = %s", (pedido_id,))
                conn.commit()
                cur.close()
                conn.close()
                limpar_campos()
                carregar_tabela()
            except Exception as e:
                messagebox.showerror("Erro ao Remover", str(e))

    # --- Funções da Interface ---
    def preencher_campos(event):
        """Preenche os campos do formulário ao selecionar um item na tabela."""
        item_selecionado = tree.selection()
        if not item_selecionado: return
        
        limpar_campos(limpar_selecao=False)
        valores = tree.item(item_selecionado)["values"]
        
        pedido_id = valores[0]
        quantidade = valores[1]
        
        pedido_texto = next((p for p in cb_pedido['values'] if p.startswith(f"{pedido_id} -")), "")
        
        cb_pedido.set(pedido_texto)
        entry_quantidade.insert(0, quantidade)
        cb_pedido.config(state='disabled') # Impede a troca do pedido ao atualizar

    def limpar_campos(limpar_selecao=True):
        """Limpa os campos do formulário e a seleção da tabela."""
        cb_pedido.config(state='normal')
        cb_pedido.set("")
        entry_quantidade.delete(0, tk.END)
        entry_filtro.delete(0, tk.END)
        if limpar_selecao and tree.selection():
            tree.selection_remove(tree.selection()[0])
        carregar_tabela() # Recarrega a tabela sem filtro

    # --- Interface Gráfica (UI) ---
    
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Pedido:").grid(row=0, column=0, padx=5, pady=5)
    cb_pedido = ttk.Combobox(form_frame, width=35)
    cb_pedido.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(form_frame, text="Quantidade Geral:").grid(row=0, column=2, padx=5, pady=5)
    entry_quantidade = tk.Entry(form_frame)
    entry_quantidade.grid(row=0, column=3, padx=5, pady=5)
    
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Salvar Quantidade", command=salvar_quantidade).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Remover Quantidade", command=remover_quantidade).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)
    tk.Label(filtro_frame, text="Filtrar por ID do Pedido:").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", lambda event: carregar_tabela(entry_filtro.get()))
    
    tree_frame = tk.Frame(janela, padx=10, pady=10)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    colunas = ("pedidoid", "quantiadeprod")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    tree.heading("pedidoid", text="ID do Pedido")
    tree.heading("quantiadeprod", text="Quantidade Geral de Itens")
    tree.column("pedidoid", width=200, anchor='center')
    tree.column("quantiadeprod", width=300, anchor='center')

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(expand=True, fill=tk.BOTH)
    
    tree.bind("<<TreeviewSelect>>", preencher_campos)
    
    # Carregamento inicial
    carregar_pedidos_dropdown()
    carregar_tabela()