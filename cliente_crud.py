import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_cliente():
    janela = tk.Toplevel()
    janela.title("Gerenciar Clientes")
    janela.geometry("800x500")

    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if filtro:
                cur.execute("""
                    SELECT * FROM amazon.cliente 
                    WHERE CAST(ClienteID AS TEXT) LIKE %s OR NomeCliente ILIKE %s
                    ORDER BY NomeCliente
                """, (f"{filtro}%", f"%{filtro}%"))
            else:
                cur.execute("""
                    SELECT * FROM amazon.cliente
                    ORDER BY ClienteID
                """)
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def inserir_cliente():
        nome = entry_nome.get()
        assinatura = var_assinatura.get()
        rua = entry_rua.get()
        numero = entry_numero.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if not (nome and email and senha):
            messagebox.showwarning("Atenção", "Preencha pelo menos Nome, Email e Senha")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.cliente (NomeCliente, TerAssinaturaPrime, Rua, Numero, Email, Senha)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, assinatura, rua, numero, email, senha))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente inserido com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para deletar.")
            return
        cliente_id = tree.item(item)["values"][0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.cliente WHERE ClienteID = %s", (cliente_id,))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            messagebox.showinfo("Sucesso", "Cliente deletado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_clientes():
        termo = entry_filtro.get()
        carregar_dados(termo)

    def preencher_campos(event):
        item = tree.selection()
        if not item:
            return
        valores = tree.item(item)["values"]
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])

        var_assinatura.set(valores[2])
        entry_rua.delete(0, tk.END)
        entry_rua.insert(0, valores[3])

        entry_numero.delete(0, tk.END)
        entry_numero.insert(0, valores[4])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, valores[5])

        entry_senha.delete(0, tk.END)
        entry_senha.insert(0, valores[6])

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        var_assinatura.set(False)
        entry_rua.delete(0, tk.END)
        entry_numero.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        tree.selection_remove(tree.selection())


    def atualizar_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")
            return

        cliente_id = tree.item(item)["values"][0]
        nome = entry_nome.get()
        assinatura = var_assinatura.get()
        rua = entry_rua.get()
        numero = entry_numero.get()
        email = entry_email.get()
        senha = entry_senha.get()

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE amazon.cliente
                SET NomeCliente=%s, TerAssinaturaPrime=%s, Rua=%s, Numero=%s, Email=%s, Senha=%s
                WHERE ClienteID=%s
            """, (nome, assinatura, rua, numero, email, senha, cliente_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(form_frame)
    entry_nome.grid(row=0, column=1)

    tk.Label(form_frame, text="Assinatura Prime:").grid(row=0, column=2)
    var_assinatura = tk.BooleanVar()
    check_assinatura = tk.Checkbutton(form_frame, variable=var_assinatura)
    check_assinatura.grid(row=0, column=3)

    tk.Label(form_frame, text="Rua:").grid(row=1, column=0)
    entry_rua = tk.Entry(form_frame)
    entry_rua.grid(row=1, column=1)

    tk.Label(form_frame, text="Número:").grid(row=1, column=2)
    entry_numero = tk.Entry(form_frame)
    entry_numero.grid(row=1, column=3)

    tk.Label(form_frame, text="Email:").grid(row=2, column=0)
    entry_email = tk.Entry(form_frame)
    entry_email.grid(row=2, column=1)

    tk.Label(form_frame, text="Senha:").grid(row=2, column=2)
    entry_senha = tk.Entry(form_frame, show="*")
    entry_senha.grid(row=2, column=3)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Cliente", command=inserir_cliente).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_cliente).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Atualizar Selecionado", command=atualizar_cliente).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Limpar Campos", command=limpar_campos).pack(side=tk.LEFT, padx=10)



    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar (Nome ou ID):").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", lambda event: filtrar_clientes())  # Filtro automático
    tk.Button(filtro_frame, text="Buscar", command=filtrar_clientes).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("ClienteID", "NomeCliente", "TerAssinaturaPrime", "Rua", "Numero", "Email", "Senha")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill=tk.BOTH)


    # VINCULA o clique para preencher os campos
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    carregar_dados()
    janela.mainloop()
