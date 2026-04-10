import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.markdown("""
# 🩺 ClinicMind PRO  
### 🧠 Treinador de Raciocínio Clínico
""")
# ---------------- PROGRESSO ----------------

if st.session_state.total > 0:
    progresso = st.session_state.total / 20
    st.progress(min(progresso, 1.0))
    st.caption(f"📈 Progresso: {st.session_state.total} casos respondidos")
 
# ---------------- BANCO DE CASOS (50 BASE) ----------------

base_casos = [

# CARDIO
("Dor torácica opressiva, sudorese, náusea.",
 ["IAM","Ansiedade","DRGE","Pneumonia"],
 "IAM",
 "Quadro típico de síndrome coronariana aguda.",
 "HEART"),

("Dispneia, ortopneia e edema.",
 ["ICC","TEP","Asma","DPOC"],
 "ICC",
 "Insuficiência cardíaca.",
 "Framingham"),

("Síncope ao esforço.",
 ["Estenose aórtica","IAM","Arritmia","Ansiedade"],
 "Estenose aórtica",
 "Tríade clássica.",
 "Eco"),

("Palpitação irregular.",
 ["FA","IAM","TV","Bradicardia"],
 "FA",
 "Fibrilação atrial.",
 "CHA2DS2-VASc"),

("Dor torácica ventilatório-dependente.",
 ["Pericardite","IAM","TEP","Ansiedade"],
 "Pericardite",
 "Melhora ao inclinar.",
 "ECG"),

# PNEUMO
("Febre, tosse produtiva.",
 ["Pneumonia","Asma","TEP","ICC"],
 "Pneumonia",
 "Infecção pulmonar.",
 "CURB-65"),

("Dispneia súbita + taquicardia.",
 ["TEP","Pneumonia","Asma","DPOC"],
 "TEP",
 "Embolia pulmonar.",
 "Wells"),

("Tosse crônica + tabagismo.",
 ["DPOC","Asma","Pneumonia","Câncer"],
 "DPOC",
 "Doença obstrutiva.",
 "Espirometria"),

("Sibilância episódica.",
 ["Asma","DPOC","TEP","ICC"],
 "Asma",
 "Broncoconstrição.",
 "Clínico"),

("Hemoptise + perda de peso.",
 ["Câncer","TB","Pneumonia","DPOC"],
 "Câncer",
 "Neoplasia pulmonar.",
 "TC"),

# NEURO
("Déficit súbito.",
 ["AVC","Tumor","Epilepsia","Enxaqueca"],
 "AVC",
 "Instalação abrupta.",
 "NIHSS"),

("Cefaleia trovoada.",
 ["HSA","Enxaqueca","Meningite","AVC"],
 "HSA",
 "Hemorragia.",
 "TC"),

("Convulsão.",
 ["Epilepsia","AVC","Tumor","Hipoglicemia"],
 "Epilepsia",
 "Crise típica.",
 "EEG"),

("Tremor repouso.",
 ["Parkinson","AVC","Demência","Ataxia"],
 "Parkinson",
 "Extrapiramidal.",
 "Clínico"),

("Febre + rigidez nuca.",
 ["Meningite","AVC","Enxaqueca","Tumor"],
 "Meningite",
 "Tríade clássica.",
 "Punção"),

# INFECTO
("Febre + hipotensão.",
 ["Sepse","Choque cardiogênico","Anafilaxia","TEP"],
 "Sepse",
 "Disfunção orgânica.",
 "SOFA"),

("Febre + dor lombar.",
 ["Pielonefrite","ITU","Sepse","Dengue"],
 "Pielonefrite",
 "Infecção renal.",
 "Urocultura"),

("Febre + exantema.",
 ["Dengue","Zika","Chikungunya","Sepse"],
 "Dengue",
 "Arbovirose.",
 "Clínico"),

("Cavitação pulmonar.",
 ["TB","Pneumonia","Câncer","TEP"],
 "TB",
 "BAAR.",
 "BAAR"),

("Febre + sopro.",
 ["Endocardite","Sepse","IAM","TEP"],
 "Endocardite",
 "Infecção valvar.",
 "Duke"),

# GASTRO
("Dor epigástrica.",
 ["Gastrite","Úlcera","IAM","Pancreatite"],
 "Gastrite",
 "Inflamação.",
 "Endoscopia"),

("Dor FID.",
 ["Apendicite","Diverticulite","Colecistite","Pancreatite"],
 "Apendicite",
 "Clássico.",
 "Alvarado"),

("Dor irradiada dorso.",
 ["Pancreatite","IAM","Gastrite","Úlcera"],
 "Pancreatite",
 "Lipase.",
 "Ranson"),

("Icterícia + febre.",
 ["Colangite","Hepatite","Colecistite","Cirrose"],
 "Colangite",
 "Charcot.",
 "Clínico"),

("Hematoquezia.",
 ["HDB","Hemorroida","Câncer","Úlcera"],
 "HDB",
 "Sangramento baixo.",
 "Colonoscopia"),

# ENDO
("Poliúria + polidipsia.",
 ["DM","DI","Hipoglicemia","Sepse"],
 "DM",
 "Hiperglicemia.",
 "HbA1c"),

("Hipoglicemia.",
 ["Hipoglicemia","DM","Sepse","AVC"],
 "Hipoglicemia",
 "Baixa glicose.",
 "Glicemia"),

("Hipotensão + hipercalemia.",
 ["Addison","Cushing","SIADH","DM"],
 "Addison",
 "Insuficiência adrenal.",
 "Cortisol"),

("Ganho peso + estrias.",
 ["Cushing","DM","Obesidade","Hipotireoidismo"],
 "Cushing",
 "Hipercortisolismo.",
 "Cortisol"),

("Perda peso + taquicardia.",
 ["Hipertireoidismo","DM","Ansiedade","ICC"],
 "Hipertireoidismo",
 "Excesso hormonal.",
 "TSH"),

# PEDIATRIA
("Febre + exantema.",
 ["Sarampo","Rubéola","Dengue","Varicela"],
 "Sarampo",
 "Viral.",
 "Clínico"),

("Estridor.",
 ["Laringite","Asma","Pneumonia","Bronquite"],
 "Laringite",
 "Croup.",
 "Clínico"),

("Língua em morango.",
 ["Kawasaki","Sarampo","Sepse","Varicela"],
 "Kawasaki",
 "Vasculite.",
 "Clínico"),

("Diarreia + desidratação.",
 ["Gastroenterite","Sepse","DM","ITU"],
 "Gastroenterite",
 "Intestinal.",
 "Clínico"),

("Convulsão febril.",
 ["Convulsão febril","Epilepsia","Meningite","AVC"],
 "Convulsão febril",
 "Benigna.",
 "Clínico"),
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

# ---------------- CASO ----------------

caso = st.session_state.caso_atual

st.markdown("---")
st.write(f"**Nível:** {caso['nivel']}")
st.write(caso["enunciado"])

resposta = st.radio(
    "Qual o diagnóstico mais provável?",
    caso["opcoes"],
    key="resposta_radio"
)

# ---------------- RESPONDER ----------------

if not st.session_state.respondido:
    if st.button("Responder"):

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

# ---------------- RESULTADO ----------------

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
