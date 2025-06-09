import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar 

def janela_cli_loja():
    janela = tk.Toplevel()
    janela.title("Gerenciar Cliente Avalia Loja")
    janela.geometry("900x500")

    def carregar_clientes_lojas():
        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("SELECT ClienteID, NomeCliente FROM amazon.cliente ORDER BY NomeCliente")
            clientes = cur.fetchall()
            cb_cliente['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

            cur.execute("SELECT LojaID, NomeLoja FROM amazon.loja ORDER BY NomeLoja")
            lojas = cur.fetchall()
            cb_loja['values'] = [f"{t[0]} - {t[1]}" for t in lojas]

            cb_filtro_cliente['values'] = cb_cliente['values']
            cb_filtro_loja['values'] = cb_loja['values']

            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dados(cliente_id=None, loja_id=None):
        for item in tree.get_children():
            tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            if cliente_id and loja_id:
                cur.execute("""
                    SELECT * FROM amazon.cli_avalia_loja 
                    WHERE clienteid = %s AND lojaid = %s
                """, (cliente_id, loja_id))
            elif cliente_id:
                cur.execute("SELECT * FROM amazon.cli_avalia_loja WHERE clienteid = %s", (cliente_id,))
            elif loja_id:
                cur.execute("SELECT * FROM amazon.cli_avalia_loja WHERE lojaid = %s", (loja_id,))
            else:
                cur.execute("SELECT * FROM amazon.cli_avalia_loja")
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
        loja = cb_loja.get()

        if not (nota or data or cliente or loja):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            cliente_id = int(cliente.split(" - ")[0])
            loja_id = int(loja.split(" - ")[0])
        except Exception:
            messagebox.showwarning("Erro", "Selecione cliente e loja válidos.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO amazon.cli_avalia_loja 
                (ClienteID, LojaID, nota, data, comentario)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, loja_id, nota, data, comentario))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_avaliacao():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma avaliação para deletar.")
            return
        cliente_id = tree.item(item)["values"][0]
        loja_id = tree.item(item)["values"][1]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM amazon.cli_avalia_loja WHERE clienteid = %s AND LojaID = %s", (cliente_id, loja_id))
            conn.commit()
            cur.close()
            conn.close()
            carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def filtrar_avaliacoes():
        cliente = cb_filtro_cliente.get()
        loja = cb_filtro_loja.get()

        cliente_id = None
        loja_id = None

        if cliente:
            try:
                cliente_id = int(cliente.split(" - ")[0])
            except:
                pass
        if loja:
            try:
                loja_id = int(loja.split(" - ")[0])
            except:
                pass

        carregar_dados(cliente_id, loja_id)

    # === Formulário ===
    form_frame = tk.Frame(janela)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Cliente:").grid(row=0, column=0)
    cb_cliente = ttk.Combobox(form_frame, width=25)
    cb_cliente.grid(row=0, column=1)

    tk.Label(form_frame, text="Loja:").grid(row=0, column=2)
    cb_loja = ttk.Combobox(form_frame, width=25)
    cb_loja.grid(row=0, column=3)

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
    tk.Button(btn_frame, text="Deletar Selecionado", command=deletar_avaliacao).pack(side=tk.LEFT, padx=10)

    # === Filtro ===
    filtro_frame = tk.Frame(janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por Cliente:").pack(side=tk.LEFT)
    cb_filtro_cliente = ttk.Combobox(filtro_frame, width=30)
    cb_filtro_cliente.pack(side=tk.LEFT, padx=5)

    tk.Label(filtro_frame, text="Filtrar por Loja:").pack(side=tk.LEFT)
    cb_filtro_loja = ttk.Combobox(filtro_frame, width=30)
    cb_filtro_loja.pack(side=tk.LEFT, padx=5)

    tk.Button(filtro_frame, text="Buscar", command=lambda: filtrar_avaliacoes()).pack(side=tk.LEFT)

    # === Tabela ===
    colunas = ("ClienteID", "LojaID", "nota", "data", "comentario")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill=tk.BOTH)

    carregar_clientes_lojas()
    carregar_dados()
    janela.mainloop()