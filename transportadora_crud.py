import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_transportadora():
    janela = tk.Toplevel()
    janela.title("Gerenciar Transportadoras")
    janela.geometry("900x500")

    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if filtro:
                cur.execute("""
                    SELECT * FROM amazon.transportadora 
                    WHERE CAST(TransportadoraID AS TEXT) LIKE %s 
                    OR NomeTransportadora ILIKE %s
                    ORDER BY TransportadoraID
                """, (f"{filtro}%", f"%{filtro}%"))
            else:
                cur.execute("SELECT * FROM amazon.transportadora ORDER BY TransportadoraID")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_local.delete(0, tk.END)
        tree.selection_remove(tree.selection())

    def inserir_transportadora():
        nome = entry_nome.get()
        localizacao = entry_local.get()

        if not nome:
            messagebox.showwarning("Atenção", "Preencha pelo menos o nome da transportadora.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.transportadora (NomeTransportadora, Localizacao)
                VALUES (%s, %s)
            """, (nome, localizacao))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Transportadora inserida com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_transportadora():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma transportadora para atualizar.")
            return
        transportadora_id = tree.item(item)["values"][0]
        nome = entry_nome.get()
        localizacao = entry_local.get()

        if not nome:
            messagebox.showwarning("Atenção", "Nome da transportadora é obrigatório.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.transportadora 
                SET NomeTransportadora = %s, Localizacao = %s
                WHERE TransportadoraID = %s
            """, (nome, localizacao, transportadora_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Transportadora atualizada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_transportadora():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma transportadora para deletar.")
            return
        transportadora_id = tree.item(item)["values"][0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.transportadora WHERE TransportadoraID = %s", (transportadora_id,))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Transportadora deletada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_transportadoras(event=None):
        termo = entry_filtro.get()
        carregar_dados(termo)

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item)["values"]
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, valores[1])
            entry_local.delete(0, tk.END)
            entry_local.insert(0, valores[2])

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(form_frame)
    entry_nome.grid(row=0, column=1)

    tk.Label(form_frame, text="Localização:").grid(row=0, column=2)
    entry_local = tk.Entry(form_frame)
    entry_local.grid(row=0, column=3)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Transportadora", command=inserir_transportadora).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionada", command=atualizar_transportadora).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionada", command=deletar_transportadora).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar (Nome ou ID):").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", filtrar_transportadoras)
    tk.Button(filtro_frame, text="Buscar", command=filtrar_transportadoras).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("TransportadoraID", "NomeTransportadora", "Localizacao")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=200)
    tree.bind("<<TreeviewSelect>>", preencher_campos)
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_dados()
    janela.mainloop()
