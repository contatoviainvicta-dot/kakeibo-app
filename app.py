import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.title("🩺 ClinicMind PRO")
st.subheader("Treinador de Raciocínio Clínico")

# ---------------- BANCO DE CASOS (RESIDÊNCIA) ----------------

base_casos = [

# CARDIO
("Paciente com dor torácica, ECG com supra ST em D2, D3 e aVF.",
 ["IAM inferior","Pericardite","TEP","Angina estável"],
 "IAM inferior",
 "Supra em derivações inferiores indica infarto inferior.",
 "HEART + ECG + troponina"),

("Dispneia + BNP elevado + ortopneia.",
 ["ICC descompensada","TEP","Asma","Pneumonia"],
 "ICC descompensada",
 "BNP elevado indica sobrecarga cardíaca.",
 "Framingham"),

# PNEUMO
("Dispneia súbita + hipoxemia + taquicardia.",
 ["TEP","Pneumonia","DPOC","Asma"],
 "TEP",
 "Quadro típico de embolia pulmonar.",
 "Wells"),

("Tabagista com perda de peso + hemoptise.",
 ["Câncer de pulmão","DPOC","Pneumonia","Tuberculose"],
 "Câncer de pulmão",
 "Sinais clássicos de neoplasia pulmonar.",
 "TC de tórax"),

# NEURO
("Déficit neurológico súbito com menos de 4h de evolução.",
 ["AVC isquêmico","AVC hemorrágico","Crise epiléptica","Tumor"],
 "AVC isquêmico",
 "Janela terapêutica para trombólise.",
 "NIHSS"),

("Cefaleia súbita intensa + rigidez de nuca.",
 ["HSA","Meningite","AVC","Enxaqueca"],
 "HSA",
 "Cefaleia em trovoada + meningismo.",
 "TC sem contraste"),

# INFECTO
("Febre + hipotensão + lactato elevado.",
 ["Sepse","Choque cardiogênico","Anafilaxia","TEP"],
 "Sepse",
 "Disfunção orgânica por infecção.",
 "SOFA"),

("Febre + tosse + cavitação pulmonar.",
 ["Tuberculose","Pneumonia","Câncer","TEP"],
 "Tuberculose",
 "Cavitação pulmonar típica.",
 "BAAR"),

# GASTRO
("Dor em fossa ilíaca direita + sinal de Blumberg.",
 ["Apendicite","Colecistite","Pancreatite","Diverticulite"],
 "Apendicite",
 "Sinal clássico de irritação peritoneal.",
 "Alvarado"),

("Dor epigástrica irradiada para dorso + lipase elevada.",
 ["Pancreatite","IAM","Gastrite","Úlcera"],
 "Pancreatite",
 "Lipase elevada confirma pancreatite.",
 "Ranson"),

# ENDO
("Hipotensão + hiponatremia + hipercalemia.",
 ["Addison","Cushing","DM","SIADH"],
 "Addison",
 "Insuficiência adrenal.",
 "Cortisol"),

("Hiperglicemia + cetose + acidose.",
 ["Cetoacidose diabética","Estado hiperosmolar","Sepse","AVC"],
 "Cetoacidose diabética",
 "Tríade clássica.",
 "Gasometria"),

# OBST
("Gestante com PA elevada + proteinúria.",
 ["Pré-eclâmpsia","Eclâmpsia","HAS","Sepse"],
 "Pré-eclâmpsia",
 "Critérios diagnósticos clássicos.",
 "PA + proteína"),

# PEDIATRIA
("Febre + descamação de extremidades + língua em morango.",
 ["Kawasaki","Sarampo","Rubéola","Varicela"],
 "Kawasaki",
 "Vasculite pediátrica.",
 "Critérios clínicos"),
]

# EXPANDIR PARA 100 CASOS
casos = []
for i in range(100):
    base = random.choice(base_casos)
    casos.append({
        "id": i,
        "nivel": random.choice(["Interno","R1","R3"]),
        "enunciado": f"Caso {i+1}: {base[0]}",
        "opcoes": base[1],
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

# ---------------- CASO ----------------

caso = st.session_state.caso_atual

st.markdown("---")
st.write(f"**Nível:** {caso['nivel']}")
st.write(caso["enunciado"])

resposta = st.radio("Qual o diagnóstico mais provável?", caso["opcoes"])

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

    col1, col2 = st.columns(2)

    if col1.button("➡️ Próximo caso"):
        st.session_state.caso_atual = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if col2.button("⛔ Finalizar sessão"):
        st.session_state.finalizado = True

# ---------------- RESULTADO FINAL ----------------

if st.session_state.finalizado:

    st.markdown("---")
    st.header("📊 Resultado Final")

    total = st.session_state.total
    pontos = st.session_state.pontos

    acuracia = (pontos / (total * 10)) * 100 if total > 0 else 0

    st.write(f"Casos respondidos: {total}")
    st.write(f"Pontos: {pontos}")
    st.write(f"Acurácia: {acuracia:.1f}%")

    st.subheader("❗ Principais erros")

    if st.session_state.erros:
        for erro, freq in st.session_state.erros.items():
            st.write(f"{erro}: {freq} erros")
    else:
        st.write("Sem erros 👏")

    if st.button("🔄 Reiniciar sessão"):
        st.session_state.clear()
        st.rerun()
