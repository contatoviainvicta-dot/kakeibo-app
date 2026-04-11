import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.markdown("""
# 🩺 Escola Superior de Ciencias da Saude
### 🧠 Rodizio: clinica medica
""")

st.markdown("""
# 🩺 ClinicMind PRO  
### 🧠 Treinador de Raciocínio Clínico
""")
# ---------------- BANCO DE CASOS ----------------

base_casos = [
("Dor torácica opressiva, sudorese.", ["IAM","Ansiedade","DRGE","Pneumonia"], "IAM","Síndrome coronariana.","HEART"),
("Dispneia + edema.", ["ICC","TEP","Asma","DPOC"], "ICC","Insuficiência cardíaca.","Framingham"),
("Síncope esforço.", ["Estenose aórtica","IAM","Arritmia","Ansiedade"], "Estenose aórtica","Clássico.","Eco"),
("Palpitação irregular.", ["FA","IAM","TV","Bradicardia"], "FA","Arritmia.","CHA2DS2"),
("Dor ventilatório-dependente.", ["Pericardite","IAM","TEP","Ansiedade"], "Pericardite","Melhora ao inclinar.","ECG"),
("Febre + tosse.", ["Pneumonia","Asma","TEP","ICC"], "Pneumonia","Infecção.","CURB"),
("Dispneia súbita.", ["TEP","Pneumonia","Asma","DPOC"], "TEP","Embolia.","Wells"),
("Tosse crônica.", ["DPOC","Asma","Pneumonia","Câncer"], "DPOC","Obstrutiva.","Espiro"),
("Sibilância.", ["Asma","DPOC","TEP","ICC"], "Asma","Reversível.","Clínico"),
("Hemoptise + emagrecimento.", ["Câncer","TB","Pneumonia","DPOC"], "Câncer","Neoplasia.","TC"),
("Déficit súbito.", ["AVC","Tumor","Epilepsia","Enxaqueca"], "AVC","Agudo.","NIHSS"),
("Cefaleia trovoada.", ["HSA","Enxaqueca","Meningite","AVC"], "HSA","Hemorragia.","TC"),
("Convulsão.", ["Epilepsia","AVC","Tumor","Hipoglicemia"], "Epilepsia","Crise.","EEG"),
("Tremor repouso.", ["Parkinson","AVC","Demência","Ataxia"], "Parkinson","Extrapiramidal.","Clínico"),
("Febre + rigidez.", ["Meningite","AVC","Enxaqueca","Tumor"], "Meningite","Tríade.","Punção"),
]

# ---------------- EXPANSÃO ----------------

casos = []
for i in range(100):
    base = random.choice(base_casos)
    opcoes = base[1].copy()
    random.shuffle(opcoes)

    casos.append({
        "id": i,
        "nivel": random.choice(["Interno","R1","R3"]),
        "enunciado": f"Caso {i+1}: {base[0]}",
        "opcoes": opcoes,
        "correta": base[2],
        "explicacao": base[3],
        "score": base[4]
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

if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

# ---------------- PROGRESSO DINÂMICO ----------------

meta = 20
progresso = st.session_state.total / meta

st.progress(min(progresso, 1.0))

if progresso < 0.3:
    st.caption("🚀 Começando... mantenha o ritmo!")
elif progresso < 0.7:
    st.caption("🔥 Bom progresso! Continue!")
elif progresso < 1.0:
    st.caption("⚡ Quase lá! Últimos casos!")
else:
    st.caption("🏆 Meta atingida! Excelente!")

st.caption(f"{st.session_state.total} / {meta} casos")

# ---------------- CASO ----------------

caso = st.session_state.caso_atual

st.markdown("---")
st.markdown(f"""
### 📋 Caso clínico
{caso['enunciado']}
""")

resposta = st.radio(
    "🧠 Qual o diagnóstico mais provável?",
    caso["opcoes"],
    key="resposta_radio"
)

# ---------------- RESPONDER ----------------

if not st.session_state.respondido:
    if st.button("🚀 Confirmar resposta"):

        st.session_state.total += 1
        st.session_state.respondido = True

        resposta = st.session_state.resposta_radio

        if resposta == caso["correta"]:
            st.session_state.pontos += 10
            st.success("✅ Correto!")
        else:
            st.error("❌ Incorreto")
            erro = caso["correta"]
            st.session_state.erros[erro] = st.session_state.erros.get(erro, 0) + 1

# ---------------- FEEDBACK ----------------

if st.session_state.respondido:
    st.markdown(f"""
### ✅ Resposta correta:
**{caso['correta']}**
""")

    st.markdown(f"""
### 📖 Explicação
{caso.get('explicacao','')}
""")

    st.info(f"📊 Score clínico: {caso.get('score','N/A')}")

    col1, col2 = st.columns(2)

    if col1.button("➡️ Próximo caso"):
        st.session_state.caso_atual = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if col2.button("⛔ Finalizar sessão"):
        st.session_state.finalizado = True

# ---------------- RESULTADO ----------------

if st.session_state.finalizado:

    st.markdown("---")
    st.header("📊 Resultado Final")

    total = st.session_state.total
    pontos = st.session_state.pontos

    acuracia = (pontos / (total * 10)) * 100 if total > 0 else 0

    st.metric("Casos respondidos", total)
    st.metric("Pontuação", pontos)
    st.metric("Acurácia", f"{acuracia:.1f}%")

    st.subheader("❗ Principais erros")

    if st.session_state.erros:
        for erro, freq in st.session_state.erros.items():
            st.write(f"{erro}: {freq} erros")
    else:
        st.write("Sem erros 👏")

    if st.button("🔄 Reiniciar sessão"):
        st.session_state.clear()
        st.rerun()
