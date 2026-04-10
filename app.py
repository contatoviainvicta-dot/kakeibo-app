import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------- BANCO ----------------

conn = sqlite3.connect("kakeibo.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    valor REAL,
    categoria TEXT,
    descricao TEXT,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE
)
""")

conn.commit()

# Inserir categorias padrão
categorias_padrao = ["sobrevivencia", "opcional", "cultura", "extra"]
for cat in categorias_padrao:
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (cat,))
conn.commit()

# ---------------- FUNÇÕES ----------------

def get_categorias():
    cursor.execute("SELECT nome FROM categorias")
    return [x[0] for x in cursor.fetchall()]

def add_categoria(nome):
    try:
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
    except:
        pass

def add_transacao(tipo, valor, categoria, descricao, data):
    cursor.execute("""
        INSERT INTO transacoes (tipo, valor, categoria, descricao, data)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, valor, categoria, descricao, data))
    conn.commit()

def get_transacoes():
    return pd.read_sql_query("SELECT * FROM transacoes", conn)

# ---------------- UI ----------------

st.set_page_config(page_title="Kakeibo PRO", layout="wide")

st.title("💰 Kakeibo PRO")

abas = st.tabs(["📊 Dashboard", "➕ Nova Transação", "⚙️ Categorias"])

df = get_transacoes()
categorias = get_categorias()

# ---------------- DASHBOARD ----------------

with abas[0]:
    st.header("Visão Geral")

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])
        df["mes"] = df["data"].dt.to_period("M")

        meses = sorted(df["mes"].astype(str).unique(), reverse=True)
        mes_sel = st.selectbox("Selecione o mês", meses)

        df_mes = df[df["mes"].astype(str) == mes_sel]

        receitas = df_mes[df_mes["tipo"] == "Receita"]["valor"].sum()
        despesas = df_mes[df_mes["tipo"] == "Despesa"]["valor"].sum()
        saldo = receitas - despesas

        col1, col2, col3 = st.columns(3)

        col1.metric("Receitas", f"R$ {receitas:.2f}")
        col2.metric("Despesas", f"R$ {despesas:.2f}")
        col3.metric("Saldo", f"R$ {saldo:.2f}")
# ---------------- SAÚDE FINANCEIRA ----------------

st.subheader("Saúde Financeira")

if receitas == 0:
    st.info("Sem receitas registradas")
else:
    taxa = (despesas / receitas) * 100

    st.write(f"Você gastou {taxa:.1f}% da sua renda")

    if taxa < 50:
        st.success("Excelente controle financeiro")
    elif taxa < 80:
        st.warning("Atenção: gastos moderados")
    else:
        st.error("Risco financeiro alto")
        st.subheader("Gastos por categoria")
        cat = df_mes[df_mes["tipo"] == "Despesa"].groupby("categoria")["valor"].sum()
        st.bar_chart(cat)

        st.subheader("Transações")
        st.dataframe(df_mes.sort_values("data", ascending=False))

    else:
        st.info("Nenhuma transação ainda.")

# ---------------- NOVA TRANSAÇÃO ----------------

with abas[1]:
    st.header("Adicionar Transação")

    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    valor = st.number_input("Valor", min_value=0.0, step=1.0)
    categoria = st.selectbox("Categoria", categorias)
    descricao = st.text_input("Descrição")
    data = st.date_input("Data")

    if st.button("Salvar"):
        add_transacao(tipo, valor, categoria, descricao, str(data))
        st.success("Transação salva com sucesso!")

# ---------------- CATEGORIAS ----------------

with abas[2]:
    st.header("Gerenciar Categorias")

    nova_cat = st.text_input("Nova categoria")

    if st.button("Adicionar categoria"):
        if nova_cat:
            add_categoria(nova_cat)
            st.success("Categoria adicionada!")

    st.write("Categorias atuais:")
    st.write(categorias)
