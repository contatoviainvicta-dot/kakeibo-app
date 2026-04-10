import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.title("🩺 ClinicMind PRO")
st.subheader("Treinador de Raciocínio Clínico")

# ---------------- CASOS ----------------

casos = [
    {
        "nivel": "Fácil",
        "enunciado": "Paciente com febre, tosse produtiva e dor torácica.",
        "opcoes": ["Pneumonia", "Asma", "IAM", "Ansiedade"],
        "correta": "Pneumonia",
        "explicacao": "Febre + secreção indicam infecção pulmonar.",
        "score": "CURB-65 poderia ser aplicado para avaliar gravidade."
    },
    {
        "nivel": "Médio",
        "enunciado": "Paciente com dor torácica súbita, sudorese e náusea.",
        "opcoes": ["IAM", "Pneumonia", "Ansiedade", "DRGE"],
        "correta": "IAM",
        "explicacao": "Dor torácica típica com sintomas autonômicos.",
        "score": "Escore HEART pode ser usado para estratificação."
    },
    {
        "nivel": "Difícil",
        "enunciado": "Paciente com dispneia, edema de membros inferiores e ortopneia.",
        "opcoes": ["ICC", "Asma", "Pneumonia", "TEP"],
        "correta": "ICC",
        "explicacao": "Clássico quadro de insuficiência cardíaca congestiva.",
        "score": "BNP e critérios de Framingham ajudam no diagnóstico."
    }
]

# ---------------- ESTADO ----------------

if "pontos" not in st.session_state:
    st.session_state.pontos = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "erros" not in st.session_state:
    st.session_state.erros = {}

# ---------------- SELEÇÃO DE CASO ----------------

caso = random.choice(casos)

st.markdown("---")
st.write(f"**Nível:** {caso['nivel']}")
st.write(f"**Caso:** {caso['enunciado']}")

# ---------------- RESPOSTA ----------------

resposta = st.radio("Escolha o diagnóstico:", caso["opcoes"])

if st.button("Responder"):

    st.session_state.total += 1

    if resposta == caso["correta"]:
        st.session_state.pontos += 10

        st.success("✅ Correto!")
        st.write(f"**Explicação:** {caso['explicacao']}")
        st.info(f"📊 Score clínico: {caso['score']}")

    else:
        st.error("❌ Incorreto")

        st.write(f"**Resposta correta:** {caso['correta']}")
        st.write(f"**Explicação:** {caso['explicacao']}")
        st.info(f"📊 Score clínico: {caso['score']}")

        # registrar erro
        erro = caso["correta"]
        st.session_state.erros[erro] = st.session_state.erros.get(erro, 0) + 1

# ---------------- ESTATÍSTICAS ----------------

st.markdown("---")
st.subheader("📊 Desempenho")

st.write(f"Pontos: {st.session_state.pontos}")
st.write(f"Casos respondidos: {st.session_state.total}")

if st.session_state.total > 0:
    acuracia = (st.session_state.pontos / (st.session_state.total * 10)) * 100
    st.write(f"Acurácia: {acuracia:.1f}%")

# ---------------- ERROS ----------------

st.subheader("❗ Principais erros")

if st.session_state.erros:
    for erro, freq in st.session_state.erros.items():
        st.write(f"{erro}: {freq} erros")
else:
    st.write("Sem erros ainda 👏")
