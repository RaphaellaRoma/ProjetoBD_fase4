import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_pedido():
    janela = tk.Toplevel()
    janela.title("Gerenciar Pedidos")
    janela.geometry("900x500")

    def carregar_clientes_transportadoras():
        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("SELECT ClienteID, NomeCliente FROM amazon.cliente ORDER BY NomeCliente")
            clientes = cur.fetchall()
            cb_cliente['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

            cur.execute("SELECT TransportadoraID, NomeTransportadora FROM amazon.transportadora ORDER BY NomeTransportadora")
            transportadoras = cur.fetchall()
            cb_transportadora['values'] = [f"{t[0]} - {t[1]}" for t in transportadoras]

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
                    SELECT * FROM amazon.pedido 
                    WHERE CAST(PedidoID AS TEXT) LIKE %s
                    ORDER BY PedidoID
                """, (f"{filtro}%",))
            else:
                cur.execute("SELECT * FROM amazon.pedido ORDER BY PedidoID")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos():
        entry_formapag.set("")
        entry_desc.delete(0, tk.END)
        entry_subtotal.delete(0, tk.END)
        entry_taxa.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        cb_cliente.set("")
        cb_transportadora.set("")
        tree.selection_remove(tree.selection())

    def inserir_pedido():
        formapag = entry_formapag.get()
        desconto = entry_desc.get()
        subtotal = entry_subtotal.get()
        taxa = entry_taxa.get()
        data = entry_data.get()
        cliente = cb_cliente.get()
        transportadora = cb_transportadora.get()

        if not (formapag and subtotal and data and cliente and transportadora):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            cliente_id = int(cliente.split(" - ")[0])
            transportadora_id = int(transportadora.split(" - ")[0])
        except Exception:
            messagebox.showwarning("Erro", "Selecione cliente e transportadora válidos.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.pedido 
                (FormaDePagam, Desconto, Subtotal, TaxaEntrega, DataPedFeito, ClienteID, TransportadoraID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (formapag, desconto, subtotal, taxa, data, cliente_id, transportadora_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_pedido():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pedido para atualizar.")
            return
        pedido_id = tree.item(item)["values"][0]

        formapag = entry_formapag.get()
        desconto = entry_desc.get()
        subtotal = entry_subtotal.get()
        taxa = entry_taxa.get()
        data = entry_data.get()
        cliente = cb_cliente.get()
        transportadora = cb_transportadora.get()

        try:
            cliente_id = int(cliente.split(" - ")[0])
            transportadora_id = int(transportadora.split(" - ")[0])
        except Exception:
            messagebox.showwarning("Erro", "Selecione cliente e transportadora válidos.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.pedido 
                SET FormaDePagam = %s, Desconto = %s, Subtotal = %s, TaxaEntrega = %s,
                    DataPedFeito = %s, ClienteID = %s, TransportadoraID = %s
                WHERE PedidoID = %s
            """, (formapag, desconto, subtotal, taxa, data, cliente_id, transportadora_id, pedido_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_pedido():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pedido para deletar.")
            return
        pedido_id = tree.item(item)["values"][0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.pedido WHERE PedidoID = %s", (pedido_id,))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_pedidos(event=None):
        termo = entry_filtro.get()
        carregar_dados(termo)

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item)["values"]
            entry_formapag.set(valores[1])
            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[2])
            entry_subtotal.delete(0, tk.END)
            entry_subtotal.insert(0, valores[3])
            entry_taxa.delete(0, tk.END)
            entry_taxa.insert(0, valores[4])
            entry_data.delete(0, tk.END)
            entry_data.insert(0, valores[5])
            cb_cliente.set(f"{valores[6]}")  # cliente_id
            cb_transportadora.set(f"{valores[7]}")  # transportadora_id

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Forma de Pagamento:").grid(row=0, column=0)
    entry_formapag = ttk.Combobox(form_frame, values=["Boleto", "Pix", "Cartão"], state="readonly", width=25)
    entry_formapag.grid(row=0, column=1)

    tk.Label(form_frame, text="Desconto:").grid(row=0, column=2)
    entry_desc = tk.Entry(form_frame, width=28)
    entry_desc.grid(row=0, column=3)

    tk.Label(form_frame, text="Subtotal:").grid(row=1, column=0)
    entry_subtotal = tk.Entry(form_frame, width=28)
    entry_subtotal.grid(row=1, column=1)

    tk.Label(form_frame, text="Taxa de Entrega:").grid(row=1, column=2)
    entry_taxa = tk.Entry(form_frame, width=28)
    entry_taxa.grid(row=1, column=3)

    tk.Label(form_frame, text="Data Pedido (YYYY-MM-DD):").grid(row=2, column=0)
    entry_data = tk.Entry(form_frame, width=28)
    entry_data.grid(row=2, column=1)

    tk.Label(form_frame, text="Cliente:").grid(row=3, column=0)
    cb_cliente = ttk.Combobox(form_frame, width=25)
    cb_cliente.grid(row=3, column=1)

    tk.Label(form_frame, text="Transportadora:").grid(row=3, column=2)
    cb_transportadora = ttk.Combobox(form_frame, width=25)
    cb_transportadora.grid(row=3, column=3)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Pedido", command=inserir_pedido).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionado", command=atualizar_pedido).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_pedido).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por ID:").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", filtrar_pedidos)
    tk.Button(filtro_frame, text="Buscar", command=filtrar_pedidos).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("PedidoID", "FormaDePagam", "Desconto", "Subtotal", "TaxaEntrega", "DataPedFeito", "ClienteID", "TransportadoraID")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.bind("<<TreeviewSelect>>", preencher_campos)
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_clientes_transportadoras()
    carregar_dados()
    janela.mainloop()
