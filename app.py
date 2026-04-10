import streamlit as st

st.set_page_config(page_title="ClinicMind", layout="centered")

st.title("🩺 ClinicMind - Treino de Raciocínio Clínico")

# ---------------- CASO ----------------

st.header("Caso Clínico")

st.write("""
Paciente masculino, 65 anos, apresenta febre, tosse produtiva e dor torácica há 3 dias.
""")

# ---------------- PERGUNTA ----------------

resposta = st.radio(
    "Qual o diagnóstico mais provável?",
    ["Pneumonia", "Asma", "Infarto agudo do miocárdio", "Ansiedade"]
)

# ---------------- RESPOSTA ----------------

if st.button("Responder"):

    if resposta == "Pneumonia":
        st.success("✅ Correto!")
        st.write("Quadro típico de infecção pulmonar com febre e expectoração.")
    else:
        st.error("❌ Incorreto")
        st.write("Reveja: presença de febre e secreção sugere infecção, não condição cardíaca ou psiquiátrica.")

# ---------------- EVOLUÇÃO ----------------

st.markdown("---")
st.subheader("Por que isso importa?")

st.write("""
O reconhecimento rápido de pneumonia permite início precoce de antibiótico e reduz mortalidade.
""")
