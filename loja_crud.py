import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar

def janela_loja():
    janela = tk.Toplevel()
    janela.title("Gerenciar Lojas")
    janela.geometry("800x500")

    def carregar_dados(filtro=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if filtro:
                cur.execute("""
                    SELECT * FROM amazon.loja 
                    WHERE CAST(lojaid AS TEXT) LIKE %s OR NomeLoja ILIKE %s
                """, (f"{filtro}%", f"%{filtro}%"))
            else:
                cur.execute("SELECT * FROM amazon.loja")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def inserir_loja():
        nome = entry_nome.get()
        tipo = entry_tipo.get()
        rua = entry_rua.get()
        numero = entry_numero.get()
        avaliacao = entry_avaliacao.get()

        if not (nome):
            messagebox.showwarning("Atenção", "Preencha pelo menos Nome")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.loja (NomeLoja, TipoLoja, Rua, Numero, AvaliacaoGeral)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, tipo, rua, numero, avaliacao))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_loja():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma loja para deletar.")
            return
        loja_id = tree.item(item)["values"][0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.loja WHERE LojaID = %s", (loja_id,))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_lojas():
        termo = entry_filtro.get()
        carregar_dados(termo)

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(form_frame)
    entry_nome.grid(row=0, column=1)

    tk.Label(form_frame, text="Tipo:").grid(row=0, column=2)
    entry_tipo = tk.Entry(form_frame)
    entry_tipo.grid(row=0, column=3)

    tk.Label(form_frame, text="Rua:").grid(row=1, column=0)
    entry_rua = tk.Entry(form_frame)
    entry_rua.grid(row=1, column=1)

    tk.Label(form_frame, text="Número:").grid(row=1, column=2)
    entry_numero = tk.Entry(form_frame)
    entry_numero.grid(row=1, column=3)

    tk.Label(form_frame, text="Avaliação Geral:").grid(row=2, column=0)
    entry_avaliacao = tk.Entry(form_frame)
    entry_avaliacao.grid(row=2, column=1)

    # === Botões ===
    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Inserir Loja", command=inserir_loja).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_loja).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar (Nome ou ID):").pack(side=tk.LEFT)
    entry_filtro = tk.Entry(filtro_frame)
    entry_filtro.pack(side=tk.LEFT, padx=5)
    entry_filtro.bind("<KeyRelease>", lambda event: filtrar_lojas())  # Filtro automático
    tk.Button(filtro_frame, text="Buscar", command=filtrar_lojas).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("LojaID", "NomeLoja", "TipoLoja", "Rua", "Numero", "Avaliação Geral")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_dados()
    janela.mainloop()