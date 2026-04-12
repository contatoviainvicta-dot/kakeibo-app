import streamlit as st
import random
import pandas as pd
import os
import pandas as pd
import os

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.title("🩺 ClinicMind PRO")
st.subheader("Treinador de Raciocínio Clínico")

# ----------------------------------------------------
# IDENTIFICAÇÃO DO JOGADOR
# ----------------------------------------------------

if "jogador" not in st.session_state:
    st.session_state.jogador = ""

if not st.session_state.jogador:
    nome = st.text_input("Seu nome:")
    if nome:
        st.session_state.jogador = nome
        st.rerun()
    else:
        st.stop()
# ----------------------------------------------------
# LOGIN NATIVO (STREAMLIT CLOUD)
# ----------------------------------------------------

if not st.user.is_logged_in:
    st.warning("Faça login no Streamlit para continuar.")
    st.stop()

usuario = st.user.email
st.success(f"Logado como: {usuario}")

# ----------------------------------------------------
# RANKING GLOBAL
# ----------------------------------------------------

if not os.path.exists("ranking.csv"):
    pd.DataFrame(columns=["usuario", "xp"]).to_csv("ranking.csv", index=False)

# ----------------------------------------------------
# BANCO DE CASOS
# ----------------------------------------------------

base_casos = [
    ("Dor torácica opressiva.", ["IAM","Ansiedade","DRGE","Pneumonia"], "IAM","Síndrome coronariana."),
    ("Dispneia e edema.", ["ICC","TEP","Asma","DPOC"], "ICC","Insuficiência cardíaca."),
    ("Déficit neurológico súbito.", ["AVC","Tumor","Epilepsia","Enxaqueca"], "AVC","Evento vascular."),
    ("Febre e rigidez de nuca.", ["Meningite","AVC","Enxaqueca","Tumor"], "Meningite","Infecção SNC."),
]

casos = []

idades = [30, 45, 60, 70]
sexos = ["Homem", "Mulher"]
contextos = ["há 3 dias.", "súbito hoje.", "progressivo."]

for _ in range(200):
    base = random.choice(base_casos)
    opcoes = base[1].copy()
    random.shuffle(opcoes)

    casos.append({
        "enunciado": f"{random.choice(sexos)}, {random.choice(idades)} anos, {base[0]} {random.choice(contextos)}",
        "opcoes": opcoes,
        "correta": base[2],
        "explicacao": base[3]
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

st.progress(min(st.session_state.total / 20, 1.0))
st.caption(f"⭐ XP atual: {st.session_state.xp}")

# ----------------------------------------------------
# CASO CLÍNICO
# ----------------------------------------------------

caso = st.session_state.caso
st.markdown("---")
st.write(caso["enunciado"])

resposta = st.radio("Qual o diagnóstico mais provável?", caso["opcoes"])

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
    st.info(f"Resposta correta: {caso['correta']}")
    st.write(caso["explicacao"])

    col1, col2 = st.columns(2)

    if col1.button("Próximo caso"):
        st.session_state.caso = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if col2.button("Finalizar sessão"):
        st.session_state.finalizado = True

# ----------------------------------------------------
# FINALIZAÇÃO + RANKING
# ----------------------------------------------------
# ----------------------------------------------------
# RANKING PERSISTENTE
# ----------------------------------------------------

if not os.path.exists("ranking.csv"):
    pd.DataFrame(columns=["nome", "xp"]).to_csv("ranking.csv", index=False)
# ----------------------------------------------------
# RESULTADO & RANKING
# ----------------------------------------------------

if st.session_state.finalizado:

    st.markdown("---")
    st.header("📊 Resultado Final")

    total = st.session_state.total
    pontos = st.session_state.pontos
    acuracia = (pontos / (total * 10)) * 100 if total > 0 else 0

    st.metric("Casos respondidos", total)
    st.metric("Pontuação", pontos)
    st.metric("Acurácia", f"{acuracia:.1f}%")

    # salva no ranking global
    df = pd.read_csv("ranking.csv")

    df = pd.concat([
        df,
        pd.DataFrame([{
            "nome": st.session_state.jogador,
            "xp": st.session_state.xp
        }])
    ])

    df.to_csv("ranking.csv", index=False)

    st.subheader("🏆 Ranking Global")

    top = df.sort_values("xp", ascending=False).head(10)

    for i, row in enumerate(top.itertuples(), 1):
        st.write(f"{i}. {row.nome} — {row.xp} XP")

    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
