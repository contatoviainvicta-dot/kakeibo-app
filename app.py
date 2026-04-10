import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.title("🩺 ClinicMind PRO")
st.subheader("Treinador de Raciocínio Clínico")

# ---------------- BANCO DE CASOS ----------------

casos = []

# Gerando vários casos automaticamente (simulação)
for i in range(1, 101):
    casos.append({
        "id": i,
        "nivel": random.choice(["Fácil", "Médio", "Difícil"]),
        "enunciado": f"Paciente {i} com sintomas clínicos variados (caso simulado).",
        "opcoes": ["Diagnóstico A", "Diagnóstico B", "Diagnóstico C", "Diagnóstico D"],
        "correta": "Diagnóstico A",
        "explicacao": "Explicação detalhada do caso clínico com raciocínio diagnóstico.",
        "score": "Aplicar escore clínico relevante conforme contexto."
    })

# ---------------- ESTADO ----------------

if "caso_atual" not in st.session_state:
    st.session_state.caso_atual = random.choice(casos)

if "pontos" not in st.session_state:
    st.session_state.pontos = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "erros" not in st.session_state:
    st.session_state.erros = {}

if "respondido" not in st.session_state:
    st.session_state.respondido = False

# ---------------- MOSTRAR CASO ----------------

caso = st.session_state.caso_atual

st.markdown("---")
st.write(f"**Nível:** {caso['nivel']}")
st.write(f"**Caso:** {caso['enunciado']}")

resposta = st.radio("Escolha o diagnóstico:", caso["opcoes"])

# ---------------- RESPONDER ----------------

if not st.session_state.respondido:
    if st.button("Responder"):

        st.session_state.total += 1
        st.session_state.respondido = True

        if resposta == caso["correta"]:
            st.session_state.pontos += 10
            st.success("✅ Correto!")
        else:
            st.error("❌ Incorreto")
            erro = caso["correta"]
            st.session_state.erros[erro] = st.session_state.erros.get(erro, 0) + 1

# ---------------- FEEDBACK ----------------

if st.session_state.respondido:
    st.write(f"**Resposta correta:** {caso['correta']}")
    st.write(f"**Explicação:** {caso['explicacao']}")
    st.info(f"📊 Score clínico: {caso['score']}")

    # ---------------- CONTINUAR OU PARAR ----------------

    col1, col2 = st.columns(2)

    if col1.button("➡️ Próximo caso"):
        st.session_state.caso_atual = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if col2.button("⛔ Finalizar sessão"):
        st.session_state.finalizado = True

# ---------------- RESULTADO FINAL ----------------

if "finalizado" in st.session_state and st.session_state.finalizado:

    st.markdown("---")
    st.header("📊 Resultado Final")

    total = st.session_state.total
    pontos = st.session_state.pontos

    if total > 0:
        acuracia = (pontos / (total * 10)) * 100
    else:
        acuracia = 0

    st.write(f"Casos respondidos: {total}")
    st.write(f"Pontos: {pontos}")
    st.write(f"Acurácia: {acuracia:.1f}%")

    st.subheader("❗ Principais erros")

    if st.session_state.erros:
        for erro, freq in st.session_state.erros.items():
            st.write(f"{erro}: {freq} erros")
    else:
        st.write("Sem erros 👏")

    if st.button("🔄 Reiniciar"):
        st.session_state.clear()
        st.rerun()
