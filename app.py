import streamlit as st
import random
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Hasher

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

# ----------------------------------------------------
# CARREGAR USUÁRIOS
# ----------------------------------------------------

with open("users.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# ----------------------------------------------------
# CADASTRO DE USUÁRIO
# ----------------------------------------------------

st.sidebar.subheader("🆕 Criar conta")

novo_user = st.sidebar.text_input("Novo usuário")
novo_nome = st.sidebar.text_input("Nome completo")
nova_senha = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Cadastrar"):
    if novo_user and nova_senha:
        if novo_user in config["credentials"]["usernames"]:
            st.sidebar.error("Usuário já existe")
        else:
            hashed = Hasher([nova_senha]).generate()[0]
            config["credentials"]["usernames"][novo_user] = {
                "name": novo_nome,
                "password": hashed
            }
            with open("users.yaml", "w") as file:
                yaml.dump(config, file)
            st.sidebar.success("Conta criada! Faça login.")
    else:
        st.sidebar.warning("Preencha todos os campos")

# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

nome, status, usuario = authenticator.login(
    location="main",
    key="login_form"
)

if status is False:
    st.error("Usuário ou senha incorretos")
    st.stop()

if status is None:
    st.warning("Faça login para continuar")
    st.stop()

authenticator.logout("Sair", "sidebar", key="logout_btn")
st.success(f"Bem-vindo, {nome} 👋")

# ----------------------------------------------------
# RANKING GLOBAL
# ----------------------------------------------------

if not os.path.exists("ranking.csv"):
    pd.DataFrame(columns=["usuario","xp"]).to_csv("ranking.csv", index=False)

# ----------------------------------------------------
# BANCO DE CASOS
# ----------------------------------------------------

base_casos = [
("Dor torácica opressiva.", ["IAM","Ansiedade","DRGE","Pneumonia"], "IAM","Síndrome coronariana.","HEART"),
("Dispneia e edema.", ["ICC","TEP","Asma","DPOC"], "ICC","Insuficiência cardíaca.","Framingham"),
("Déficit neurológico súbito.", ["AVC","Tumor","Epilepsia","Enxaqueca"], "AVC","Evento vascular.","NIHSS"),
("Febre e rigidez de nuca.", ["Meningite","AVC","Enxaqueca","Tumor"], "Meningite","Infecção SNC.","Punção"),
]

casos = []
idades = [30,45,60,70]
sexos = ["Homem","Mulher"]
contextos = ["há 3 dias.","súbito hoje.","progressivo."]

for i in range(200):
    b = random.choice(base_casos)
    ops = b[1].copy()
    random.shuffle(ops)

    casos.append({
        "enunciado": f"{random.choice(sexos)}, {random.choice(idades)} anos, {b[0]} {random.choice(contextos)}",
        "opcoes": ops,
        "correta": b[2],
        "explicacao": b[3],
        "score": b[4]
    })

# ----------------------------------------------------
# ESTADO
# ----------------------------------------------------

if "caso" not in st.session_state:
    st.session_state.caso = random.choice(casos)
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "respondido" not in st.session_state:
    st.session_state.respondido = False
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

# ----------------------------------------------------
# PROGRESSO
# ----------------------------------------------------

st.progress(min(st.session_state.total/20,1.0))
st.caption(f"⭐ XP: {st.session_state.xp}")

# ----------------------------------------------------
# CASO
# ----------------------------------------------------

caso = st.session_state.caso
st.write(caso["enunciado"])

resposta = st.radio("Resposta:", caso["opcoes"])

if not st.session_state.respondido:
    if st.button("Responder"):
        st.session_state.total += 1
        st.session_state.respondido = True
        if resposta == caso["correta"]:
            st.session_state.xp += 10
            st.success("Correto! +10 XP")
        else:
            st.error("Incorreto")

# ----------------------------------------------------
# FEEDBACK
# ----------------------------------------------------

if st.session_state.respondido:
    st.write(caso["explicacao"])

    if st.button("Próximo"):
        st.session_state.caso = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if st.button("Finalizar"):
        st.session_state.finalizado = True

# ----------------------------------------------------
# FINALIZAÇÃO + RANKING
# ----------------------------------------------------

if st.session_state.finalizado:

    df = pd.read_csv("ranking.csv")

    df = pd.concat([
        df,
        pd.DataFrame([{
            "usuario": usuario,
            "xp": st.session_state.xp
        }])
    ])

    df.to_csv("ranking.csv", index=False)

    st.subheader("🏆 Ranking Global")
    top = df.sort_values("xp", ascending=False).head(10)

    for _, row in top.iterrows():
        st.write(f"{row['usuario']} — {row['xp']} XP")

    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
