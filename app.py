import streamlit as st
import random

st.set_page_config(page_title="ClinicMind PRO", layout="centered")

st.title("🩺 ClinicMind PRO")
st.subheader("Treinador de Raciocínio Clínico")

# ---------------- BANCO DE CASOS (RESIDÊNCIA) ----------------

base_casos = [

# ================= CARDIO =================

("Dor torácica opressiva, sudorese, náusea.",
 ["IAM","Ansiedade","DRGE","Pneumonia"],
 "IAM",
 "Quadro típico de síndrome coronariana aguda.",
 "HEART score"),

("Dispneia, ortopneia e edema MMII.",
 ["ICC","TEP","Asma","DPOC"],
 "ICC",
 "Clássico de insuficiência cardíaca.",
 "Framingham"),

("Síncope ao esforço em idoso.",
 ["Estenose aórtica","IAM","Arritmia","Ansiedade"],
 "Estenose aórtica",
 "Tríade: síncope, angina, dispneia.",
 "Ecocardiograma"),

("Palpitação + irregularidade no pulso.",
 ["FA","IAM","TV","Bradicardia"],
 "FA",
 "Fibrilação atrial típica.",
 "CHA2DS2-VASc"),

("Dor torácica ventilatório-dependente.",
 ["Pericardite","IAM","TEP","Ansiedade"],
 "Pericardite",
 "Dor que melhora ao inclinar.",
 "ECG difuso"),

# ================= PNEUMO =================

("Febre, tosse produtiva, dor torácica.",
 ["Pneumonia","Asma","TEP","ICC"],
 "Pneumonia",
 "Infecção pulmonar clássica.",
 "CURB-65"),

("Dispneia súbita, taquicardia.",
 ["TEP","Pneumonia","Asma","DPOC"],
 "TEP",
 "Embolia pulmonar.",
 "Wells"),

("Tosse crônica + tabagismo.",
 ["DPOC","Asma","Pneumonia","Câncer"],
 "DPOC",
 "Doença obstrutiva crônica.",
 "Espirometria"),

("Sibilância + dispneia episódica.",
 ["Asma","DPOC","TEP","ICC"],
 "Asma",
 "Broncoconstrição reversível.",
 "Clínico"),

("Hemoptise + perda de peso.",
 ["Câncer pulmão","TB","Pneumonia","DPOC"],
 "Câncer pulmão",
 "Neoplasia pulmonar.",
 "TC"),

# ================= NEURO =================

("Déficit motor súbito.",
 ["AVC","Tumor","Epilepsia","Enxaqueca"],
 "AVC",
 "Instalação abrupta.",
 "NIHSS"),

("Cefaleia intensa súbita.",
 ["HSA","Enxaqueca","Meningite","AVC"],
 "HSA",
 "Cefaleia em trovoada.",
 "TC"),

("Convulsão tônico-clônica.",
 ["Epilepsia","AVC","Tumor","Hipoglicemia"],
 "Epilepsia",
 "Crise típica.",
 "EEG"),

("Rigidez + tremor de repouso.",
 ["Parkinson","AVC","Demência","Ataxia"],
 "Parkinson",
 "Síndrome extrapiramidal.",
 "Clínico"),

("Confusão + febre + rigidez nuca.",
 ["Meningite","AVC","Enxaqueca","Tumor"],
 "Meningite",
 "Tríade clássica.",
 "Punção lombar"),

# ================= INFECTO =================

("Febre + hipotensão + lactato elevado.",
 ["Sepse","Choque cardiogênico","Anafilaxia","TEP"],
 "Sepse",
 "Disfunção orgânica.",
 "SOFA"),

("Febre + dor lombar + disúria.",
 ["Pielonefrite","ITU","Sepse","Dengue"],
 "Pielonefrite",
 "Infecção renal.",
 "Urocultura"),

("Febre + exantema + mialgia.",
 ["Dengue","Zika","Chikungunya","Sepse"],
 "Dengue",
 "Arbovirose.",
 "Clínico"),

("Tosse + cavitação pulmonar.",
 ["Tuberculose","Pneumonia","Câncer","TEP"],
 "Tuberculose",
 "BAAR positivo.",
 "BAAR"),

("Febre prolongada + sopro novo.",
 ["Endocardite","Sepse","IAM","TEP"],
 "Endocardite",
 "Infecção valvar.",
 "Duke"),

# ================= GASTRO =================

("Dor epigástrica pós-prandial.",
 ["Gastrite","Úlcera","IAM","Pancreatite"],
 "Gastrite",
 "Inflamação gástrica.",
 "Endoscopia"),

("Dor FID + febre.",
 ["Apendicite","Diverticulite","Colecistite","Pancreatite"],
 "Apendicite",
 "Quadro típico.",
 "Alvarado"),

("Dor epigástrica irradiada dorso.",
 ["Pancreatite","IAM","Gastrite","Úlcera"],
 "Pancreatite",
 "Amilase/lipase.",
 "Ranson"),

("Icterícia + dor + febre.",
 ["Colangite","Hepatite","Colecistite","Cirrose"],
 "Colangite",
 "Tríade de Charcot.",
 "Clínico"),

("Hematoquezia.",
 ["Hemorragia baixa","Hemorroida","Câncer","Úlcera"],
 "Hemorragia baixa",
 "Sangramento distal.",
 "Colonoscopia"),

# ================= ENDO =================

("Poliúria + polidipsia.",
 ["DM","DI","Hipoglicemia","Sepse"],
 "DM",
 "Hiperglicemia.",
 "HbA1c"),

("Hipoglicemia + sudorese.",
 ["Hipoglicemia","DM","Sepse","AVC"],
 "Hipoglicemia",
 "Baixa glicose.",
 "Glicemia"),

("Hipotensão + hipercalemia.",
 ["Addison","Cushing","SIADH","DM"],
 "Addison",
 "Insuficiência adrenal.",
 "Cortisol"),

("Ganho de peso + estrias.",
 ["Cushing","DM","Obesidade","Hipotireoidismo"],
 "Cushing",
 "Hipercortisolismo.",
 "Cortisol"),

("Perda peso + taquicardia.",
 ["Hipertireoidismo","DM","Ansiedade","ICC"],
 "Hipertireoidismo",
 "Excesso hormonal.",
 "TSH"),

# ================= PEDIATRIA =================

("Febre + exantema + conjuntivite.",
 ["Sarampo","Rubéola","Dengue","Varicela"],
 "Sarampo",
 "Doença viral.",
 "Clínico"),

("Estridor + tosse em criança.",
 ["Laringite","Asma","Pneumonia","Bronquite"],
 "Laringite",
 "Croup.",
 "Clínico"),

("Febre + língua em morango.",
 ["Kawasaki","Sarampo","Sepse","Varicela"],
 "Kawasaki",
 "Vasculite.",
 "Clínico"),

("Diarreia + desidratação.",
 ["Gastroenterite","Sepse","DM","ITU"],
 "Gastroenterite",
 "Infecção intestinal.",
 "Clínico"),

("Febre + convulsão.",
 ["Convulsão febril","Epilepsia","Meningite","AVC"],
 "Convulsão febril",
 "Comum em criança.",
 "Clínico"),

# ================= OBST =================

("Beta-hCG positivo.",
 ["Gravidez","Mioma","Cisto","Endometriose"],
 "Gravidez",
 "Confirmação.",
 "Beta-hCG"),

("Sangramento no 1º trimestre.",
 ["Abortamento","Gravidez normal","Cisto","Mioma"],
 "Abortamento",
 "Perda gestacional.",
 "USG"),

("PA alta + proteinúria.",
 ["Pré-eclâmpsia","HAS","Eclâmpsia","Sepse"],
 "Pré-eclâmpsia",
 "Critério diagnóstico.",
 "PA"),

("Convulsão na gestante.",
 ["Eclâmpsia","Epilepsia","AVC","Sepse"],
 "Eclâmpsia",
 "Complicação.",
 "Clínico"),

("Dor pélvica + atraso menstrual.",
 ["Ectópica","Gravidez normal","Cisto","Mioma"],
 "Ectópica",
 "Gravidez fora do útero.",
 "USG"),
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

# ---------------- CASO ----------------

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
