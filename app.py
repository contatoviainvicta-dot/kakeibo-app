import streamlit as st
import random

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.markdown("""
# 🩺 ClinicMind PRO
### 🧠 Treinador de Raciocínio Clínico
""")

# ----------------------------------------------------
# BANCO BASE DE CASOS (CLÍNICA MÉDICA)
# ----------------------------------------------------

base_casos = [

# CARDIOLOGIA (10)
("Homem 62a, dor torácica opressiva 40min.", ["IAM","DRGE","Ansiedade","Pneumonia"], "IAM", "Dor típica + duração.", "HEART"),
("Dispneia aos esforços + edema MMII.", ["ICC","TEP","Asma","DPOC"], "ICC", "Sinais de congestão.", "Framingham"),
("Síncope durante esforço.", ["Estenose aórtica","IAM","Arritmia","Ansiedade"], "Estenose aórtica", "Baixo débito em esforço.", "Eco"),
("Palpitação irregular e fadiga.", ["FA","Flutter","TV","BAV"], "FA", "Ritmo irregular.", "ECG"),
("Dor torácica que piora ao inspirar.", ["Pericardite","IAM","TEP","Ansiedade"], "Pericardite", "Dor ventilatório-dependente.", "ECG"),
("HAS + cefaleia intensa.", ["Crise hipertensiva","AVC","IAM","Enxaqueca"], "Crise hipertensiva", "PA muito elevada.", "Clínico"),
("Dor torácica + sudorese + náusea.", ["IAM","Ansiedade","Pneumonia","TEP"], "IAM", "Síndrome coronariana.", "HEART"),
("Edema agudo pulmonar.", ["ICC","TEP","Pneumonia","Asma"], "ICC", "Congestão aguda.", "BNP"),
("Claudicação ao caminhar.", ["DAOP","TVP","Artrite","Neuropatia"], "DAOP", "Isquemia periférica.", "ITB"),
("Hipotensão + taquicardia após IAM.", ["Choque cardiogênico","Sepse","TEP","Arritmia"], "Choque cardiogênico", "Falência de bomba.", "Clínico"),

# PNEUMOLOGIA (8)
("Febre + tosse + estertores.", ["Pneumonia","TEP","Asma","ICC"], "Pneumonia", "Infecção pulmonar.", "CURB-65"),
("Dispneia súbita + taquicardia.", ["TEP","Pneumonia","Asma","DPOC"], "TEP", "Embolia pulmonar.", "Wells"),
("Tabagista + tosse crônica.", ["DPOC","Asma","TB","Pneumonia"], "DPOC", "Doença obstrutiva.", "Espirometria"),
("Sibilância recorrente.", ["Asma","DPOC","TEP","ICC"], "Asma", "Broncoespasmo.", "Clínico"),
("Hemoptise + emagrecimento.", ["TB","Câncer","Pneumonia","DPOC"], "TB", "Sintomas constitucionais.", "BAAR"),
("Dispneia progressiva + baqueteamento.", ["Fibrose pulmonar","Asma","DPOC","TEP"], "Fibrose pulmonar", "Doença intersticial.", "TC"),
("Tosse + febre + dor torácica.", ["Pneumonia","TEP","ICC","Asma"], "Pneumonia", "Quadro infeccioso.", "RX"),
("Piora súbita em DPOC.", ["Exacerbação DPOC","IAM","TEP","Pneumonia"], "Exacerbação DPOC", "Descompensação.", "Gasometria"),

# NEUROLOGIA (7)
("Déficit focal súbito.", ["AVC","Epilepsia","Tumor","Enxaqueca"], "AVC", "Instalação aguda.", "NIHSS"),
("Cefaleia súbita intensa.", ["HSA","Enxaqueca","Meningite","AVC"], "HSA", "Pior dor da vida.", "TC"),
("Crise convulsiva.", ["Epilepsia","AVC","Tumor","Hipoglicemia"], "Epilepsia", "Crise típica.", "EEG"),
("Rigidez + tremor repouso.", ["Parkinson","AVC","Ataxia","Demência"], "Parkinson", "Síndrome extrapiramidal.", "Clínico"),
("Febre + confusão + rigidez.", ["Meningite","AVC","Delirium","Sepse"], "Meningite", "Infecção SNC.", "Punção"),
("Rebaixamento nível consciência.", ["AVC","Hipoglicemia","Sepse","Intoxicação"], "Hipoglicemia", "Glicose baixa.", "Glicemia"),
("Tontura + nistagmo.", ["Vertigem periférica","AVC","Enxaqueca","Epilepsia"], "Vertigem periférica", "Vestibular.", "Clínico"),

# INFECTOLOGIA (7)
("Febre + hipotensão.", ["Sepse","IAM","TEP","ICC"], "Sepse", "Resposta inflamatória.", "SOFA"),
("Febre + disúria.", ["ITU","Sepse","Pielonefrite","Prostatite"], "ITU", "Infecção urinária.", "EAS"),
("Febre + dor lombar.", ["Pielonefrite","ITU","Sepse","Cálculo"], "Pielonefrite", "Infecção renal.", "Urocultura"),
("Febre + icterícia.", ["Hepatite","Colangite","Sepse","Lepto"], "Colangite", "Tríade de Charcot.", "Clínico"),
("Febre + exantema.", ["Dengue","Sarampo","Zika","Chikungunya"], "Dengue", "Arbovirose.", "Clínico"),
("Tosse + febre prolongada.", ["TB","Pneumonia","Câncer","DPOC"], "TB", "Doença crônica.", "BAAR"),
("Febre + sopro novo.", ["Endocardite","Sepse","IAM","TEP"], "Endocardite", "Infecção valvar.", "Duke"),

# GASTROENTEROLOGIA (8)
("Dor epigástrica em queimação.", ["Gastrite","IAM","Úlcera","Pancreatite"], "Gastrite", "Dispepsia.", "Clínico"),
("Dor intensa em barra.", ["Pancreatite","IAM","Colecistite","Gastrite"], "Pancreatite", "Lipase elevada.", "Ranson"),
("Dor FID + febre.", ["Apendicite","Diverticulite","ITU","Cólica"], "Apendicite", "Dor migratória.", "Alvarado"),
("Icterícia + dor + febre.", ["Colangite","Hepatite","Cirrose","Colecistite"], "Colangite", "Infecção biliar.", "Clínico"),
("Ascite + cirrose.", ["Hipertensão portal","ICC","TB","Câncer"], "Hipertensão portal", "Complicação cirrose.", "Paracentese"),
("Hematoquezia.", ["HDB","Hemorroida","Câncer","DII"], "HDB", "Sangramento baixo.", "Colonoscopia"),
("Melena.", ["HDA","Úlcera","Câncer","Varizes"], "HDA", "Sangue digerido.", "Endoscopia"),
("Diarreia crônica.", ["DII","SII","Infecção","Câncer"], "DII", "Inflamatória.", "Colonoscopia"),

# ENDOCRINOLOGIA (5)
("Poliúria + polidipsia.", ["DM","DI","Hipoglicemia","ITU"], "DM", "Hiperglicemia.", "HbA1c"),
("Sudorese + tremor.", ["Hipoglicemia","Hipertireoidismo","Ansiedade","Sepse"], "Hipoglicemia", "Baixa glicose.", "Glicemia"),
("Ganho peso + estrias.", ["Cushing","DM","Obesidade","Hipotireoidismo"], "Cushing", "Hipercortisolismo.", "Cortisol"),
("Perda peso + taquicardia.", ["Hipertireoidismo","DM","Ansiedade","ICC"], "Hipertireoidismo", "Excesso T3/T4.", "TSH"),
("Hipotensão + hiponatremia.", ["Addison","SIADH","Sepse","IRC"], "Addison", "Insuficiência adrenal.", "Cortisol"),
]

# ----------------------------------------------------
# GERAÇÃO DE 200 CASOS
# ----------------------------------------------------

casos = []

idades = [25, 32, 45, 58, 63, 71, 79]
sexos = ["Homem", "Mulher"]
contextos = [
    "com piora há 3 dias.",
    "com início súbito hoje.",
    "progressivo há semanas.",
    "associado a mal-estar.",
    "com hipertensão prévia.",
    "diabético de longa data.",
    "tabagista crônico."
]

for i in range(200):
    base = random.choice(base_casos)

    opcoes = base[1].copy()
    random.shuffle(opcoes)

    enunciado = f"{random.choice(sexos)}, {random.choice(idades)} anos, {base[0]} {random.choice(contextos)}"

    casos.append({
        "id": i,
        "nivel": random.choice(["Interno","R1","R3"]),
        "enunciado": enunciado,
        "opcoes": opcoes,
        "correta": base[2],
        "explicacao": base[3],
        "score": base[4]
    })

# ----------------------------------------------------
# ESTADO GLOBAL
# ----------------------------------------------------

if "caso_atual" not in st.session_state:
    st.session_state.caso_atual = random.choice(casos)

if "pontos" not in st.session_state:
    st.session_state.pontos = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "ranking" not in st.session_state:
    st.session_state.ranking = []

if "erros" not in st.session_state:
    st.session_state.erros = {}

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

# ----------------------------------------------------
# PROGRESSO & XP
# ----------------------------------------------------

meta = 20
prog = st.session_state.total / meta

st.progress(min(prog, 1.0))
st.caption(f"{st.session_state.total} / {meta} casos")
st.caption(f"⭐ XP atual: {st.session_state.xp}")

# ----------------------------------------------------
# CASO
# ----------------------------------------------------

caso = st.session_state.caso_atual

st.markdown("---")
st.write(f"**Nível:** {caso['nivel']}")
st.write(caso["enunciado"])

resposta = st.radio(
    "Qual o diagnóstico mais provável?",
    caso["opcoes"],
    key="resposta_radio"
)

# ----------------------------------------------------
# RESPONDER
# ----------------------------------------------------

if not st.session_state.respondido:
    if st.button("Responder"):
        st.session_state.total += 1
        st.session_state.respondido = True

        if st.session_state.resposta_radio == caso["correta"]:
            st.session_state.pontos += 10
            st.session_state.xp += 10
            st.success("Correto! +10 XP")
        else:
            st.error("Incorreto")
            st.session_state.erros[caso["correta"]] = st.session_state.erros.get(caso["correta"], 0) + 1

# ----------------------------------------------------
# FEEDBACK
# ----------------------------------------------------

if st.session_state.respondido:

    st.write(f"**Resposta correta:** {caso['correta']}")
    st.write(caso["explicacao"])
    st.info(f"Score clínico: {caso['score']}")

    col1, col2 = st.columns(2)

    if col1.button("Próximo caso"):
        st.session_state.caso_atual = random.choice(casos)
        st.session_state.respondido = False
        st.rerun()

    if col2.button("Finalizar sessão"):
        st.session_state.finalizado = True

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

    nome = st.text_input("Digite seu nome para o ranking:")

    if nome:
        st.session_state.ranking.append({
            "nome": nome,
            "xp": st.session_state.xp
        })

        st.session_state.ranking = sorted(
            st.session_state.ranking,
            key=lambda x: x["xp"],
            reverse=True
        )[:5]

    st.subheader("🏆 Ranking")

    if st.session_state.ranking:
        for i, player in enumerate(st.session_state.ranking, 1):
            st.write(f"{i}. {player['nome']} — {player['xp']} XP")
    else:
        st.write("Sem jogadores ainda.")

    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
