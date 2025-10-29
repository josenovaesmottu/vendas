import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import warnings

# Silencia warnings e esconde detalhes de erros no Streamlit
warnings.filterwarnings("ignore")
st.set_option('client.showErrorDetails', False)

# ==============================
# CONFIGURAÇÕES
# ==============================
st.set_page_config(page_title="Dashboard de Retiradas", page_icon="🟢", layout="wide")
st.title("🟢🏍️  Acompanhamento de Retiradas — Mottu")

filiais = {
    "Mottu Abaetetuba": 282, "Mottu Alagoinhas": 110, "Mottu Ananindeua": 122, "Mottu Anápolis": 58,
    "Mottu Aparecida de Goiânia": 123, "Mottu Aracaju": 29, "Mottu Aracati": 274, "Mottu Arapiraca": 52,
    "Mottu Araçatuba": 109, "Mottu Avaré": 454, "Mottu Barreiras": 259, "Mottu Bauru": 175,
    "Mottu Bayeux": 384, "Mottu Belo Horizonte": 3, "Mottu Belém": 18, "Mottu Blumenau": 356,
    "Mottu Boa Vista": 61, "Mottu Bragança": 238, "Mottu Brasília": 10, "Mottu Vila Leopoldina": 477,
    "Mottu Cabo Frio": 283, "Mottu Camaçari": 173, "Mottu Campina Grande": 38, "Mottu Campinas": 7,
    "Mottu Campo Grande": 31, "Mottu Campos dos Goytacazes": 285, "Mottu Caruaru": 39, "Mottu Cascavel": 397,
    "Mottu Castanhal": 365, "Mottu Caucaia": 458, "Mottu Caxias": 366, "Mottu Caxias do Sul": 69,
    "Mottu Colatina": 474, "Mottu Contagem": 53, "Mottu Crato": 295, "Mottu Criciúma": 51,
    "Mottu Cuiabá": 30, "Mottu Curitiba": 4, "Mottu Divinópolis": 174, "Mottu Dourados": 77,
    "Mottu Duque de Caxias": 469, "Mottu Eunápolis": 417, "Mottu Feira de Santana": 40, "Mottu Florianópolis": 32,
    "Mottu Fortaleza": 9, "Mottu Franca": 75, "Mottu Fátima": 114, "Mottu Goiânia": 15,
    "Mottu Governador Valadares": 76, "Mottu Guarulhos": 83, "Mottu Icoaraci": 404, "Mottu Imperatriz": 65,
    "Mottu Interlagos": 37, "Mottu Ipatinga": 55, "Mottu Ipiranga": 94, "Mottu Ipojuca": 267,
    "Mottu Itabuna": 116, "Mottu Itajaí": 111, "Mottu Itapetininga": 449, "Mottu Itapipoca": 357,
    "Mottu Jacarepaguá": 248, "Mottu Jandira": 41, "Mottu Jequié": 271, "Mottu Ji Paraná": 416,
    "Mottu Joinville": 56, "Mottu João Pessoa": 28, "Mottu Juazeiro": 45, "Mottu Juazeiro do Norte": 46,
    "Mottu Juiz de Fora": 95, "Mottu Jundiaí": 33, "Mottu Lagarto": 462, "Mottu Limão - Zona Norte": 36,
    "Mottu Linhares": 258, "Mottu Londrina": 49, "Mottu Macapá": 66, "Mottu Macaé": 266,
    "Mottu Maceió": 22, "Mottu Manaus": 5, "Mottu Marabá": 68, "Mottu Maracanaú": 180,
    "Mottu Maringá": 50, "Mottu Messejana": 402, "Mottu Mexico CDMX Cien Metros": 85,
    "Mottu Mexico CDMX Colegio Militar": 11, "Mottu Mexico CDMX Tlalpan": 71, "Mottu Mexico Cancún": 107,
    "Mottu Mexico Guadalajara": 47, "Mottu Mexico Guadalajara Centro": 113, "Mottu Mexico Los Reyes": 413,
    "Mottu Mexico Monterrey": 43, "Mottu Mexico Monterrey La Fe": 106, "Mottu Mexico Mérida": 249,
    "Mottu Mexico Puebla": 48, "Mottu Mexico Querétaro": 42, "Mottu Mexico Toluca": 459,
    "Mottu Mogi das Cruzes": 86, "Mottu Montes Claros": 57, "Mottu Mossoró": 67, "Mottu Natal": 27,
    "Mottu Niterói": 105, "Mottu Olinda": 84, "Mottu Palmas": 60, "Mottu Parauapebas": 79,
    "Mottu Parnamirim": 118, "Mottu Parnaíba": 115, "Mottu Patos": 300, "Mottu Pelotas": 203,
    "Mottu Petrolina": 309, "Mottu Pindamonhangaba": 311, "Mottu Piracicaba": 44, "Mottu Piçarreira": 183,
    "Mottu Ponta Grossa": 319, "Mottu Porto Alegre": 8, "Mottu Porto Seguro": 329, "Mottu Porto Velho": 59,
    "Mottu Pouso Alegre": 472, "Mottu Praia Grande": 82, "Mottu Presidente Prudente": 252,
    "Mottu Recife": 16, "Mottu Ribeirão Preto": 17, "Mottu Rio Branco": 62, "Mottu Rio Verde": 73,
    "Mottu Rondonópolis": 70, "Mottu Salvador": 6, "Mottu Santa Maria": 455, "Mottu Santarém": 81,
    "Mottu Santos": 24, "Mottu Serra": 19, "Mottu Sete Lagoas": 372, "Mottu Sobral": 74,
    "Mottu Sorocaba": 34, "Mottu São Bernardo": 23, "Mottu São Carlos": 64, "Mottu São José do Rio Preto": 63,
    "Mottu São José dos Campos": 20, "Mottu São Luís": 21, "Mottu São Miguel": 13, "Mottu Taboão": 35,
    "Mottu Teixeira de Freitas": 284, "Mottu Teresina": 26, "Mottu Toledo": 463, "Mottu Uberaba": 78,
    "Mottu Uberlândia": 25, "Mottu Valparaíso": 310, "Mottu Vila Isabel": 225, "Mottu Vila Velha": 72,
    "Mottu Vitória": 405, "Mottu Vitória da Conquista": 80, "Mottu Vitória de Santo Antão": 250,
    "Mottu Volta Redonda": 396, "Mottu Várzea Grande": 473, "Mottu Foz do Iguaçu": 511, "Mottu Passo Fundo": 522, "Mottu Sinop": 526,
    "Mottu Itumbiara": 537, "Mottu Lages": 527, "Mottu Patos de Minas": 509,
    "Mottu Cachoeiro de Itapemirim": 505, "Mottu Cariacica": 489, "Mottu Nossa Senhora do Socorro": 507,
    "Mottu Anápolis": 58, "Mottu MX Edomex Coacalco": 499,
    "Mottu México CDMX Iztapalapa": 87, "Mottu Campo Grande - RJ": 497,
    "Mottu São José do Ribamar": 513, "Mottu São Mateus": 514, "Mottu Ourinhos": 475, "Mottu Nova Iguaçu": 478, "Mottu Madureira": 476,
    "Mottu Poços de Caldas": 515, "Mottu Americana": 533,
    "Mottu Marília": 536, "Mottu Botucatu": 523, "Mottu Votuporanga": 542, "Mottu Varginha": 546, "Mottu Chapecó": 544,
    "Mottu Caxias": 366, "Mottu Ji Paraná": 416, "Mottu Itapetininga": 449,
    "Mottu Campos dos Goytacazes": 285, "Mottu Ponta Grossa": 319, "Mottu Cascavel": 397
}
regionais = {
    "Bruno": [31, 62, 66, 25, 68, 63, 81, 79, 38, 8, 3, 72, 19, 15, 118, 40, 39],
    "Flávio": [82, 24, 35, 94, 83, 36, 23, 41, 477, 37, 13, 86, 7, 33, 34, 44],
    "Francisco": [61, 5, 59, 30, 4, 29, 28, 26, 27, 6, 21, 114, 9, 84, 16, 122, 18, 17],
    "Júlio": [22, 52, 57, 67, 78, 116, 60, 65, 32, 111, 56, 10, 46, 45, 309, 53, 58, 123, 105, 183, 173, 180, 20, 75],
    "Leonardo": [55, 474, 259, 285, 300, 77, 511, 416, 522, 526, 537, 527, 509, 455, 505, 357, 463, 397, 174, 203, 417, 356, 372, 473, 319, 489, 462, 507, 476, 469, 478, 497, 396, 366, 513, 458, 267, 514, 449, 454, 475, 472, 515, 533, 536, 523, 542, 546, 544],
    "Lucas": [42, 48, 107, 249, 113, 47, 43, 106, 71, 499, 459, 87, 413, 85, 11],
    "Rogério": [69, 70, 73, 74, 76, 110, 115, 271, 274, 258, 329, 51, 95, 284, 252, 238, 80, 109, 49, 50, 310, 295, 405, 384, 225, 248, 266, 283, 402, 250, 365, 404, 282, 64, 175, 311]
}
id_para_nome = {v: k for k, v in filiais.items()}

# ==============================
# TOKEN
# ==============================
def retorna_token():
    username = st.secrets["MOTTU_USERNAME"]
    password = st.secrets["MOTTU_PASSWORD"]

    url = "https://sso.mottu.cloud/realms/Internal/protocol/openid-connect/token"
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": "admin-v3-frontend-client",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        r = requests.post(url, data=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception:
        pass
    # silencioso: sem mensagens na interface
    return None

# ==============================
# GET VENDAS
# ==============================
def get_vendas(lugar_id, token):
    url = "https://attendance-totem.mottu.cloud/v2/Attendance/GetHistoryByFilters"

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    start_date = agora.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_date = agora.replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "servicesSituationsCode": [9],
        "serviceTypeCategoryCode": 53,
        "branchCodes": [lugar_id],
        "page": 1,
        "quantityPerPage": 100000
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "text/plain",
        "Content-Type": "application/json",
        "branch-id": str(lugar_id)
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()

        json_data = r.json() or {}
        data = json_data.get("result") or json_data.get("dataResult") or {}
        services = data.get("services") or []

        validos = [s for s in services if isinstance(s, dict) and s.get("serviceTypeCode") not in (76, 85)]
        qtd_vendas = len(validos)

        return {
            "lugarId": lugar_id,
            "lugarNome": id_para_nome.get(lugar_id, f"ID {lugar_id}"),
            "vendasHoje": qtd_vendas,
            "erro": None
        }
    except Exception:
        # silencioso (sem logs)
        return {
            "lugarId": lugar_id,
            "lugarNome": id_para_nome.get(lugar_id, f"ID {lugar_id}"),
            "vendasHoje": 0,
            "erro": "erro silencioso"
        }

# ==============================
# INTERFACE
# ==============================
regional_sel = st.selectbox("Selecione a regional:", list(regionais.keys()))
intervalo = st.number_input("Atualizar automaticamente (minutos):", min_value=1, max_value=30, value=5)
st.caption("O dashboard atualiza automaticamente a cada intervalo definido ou manualmente.")

if st.button("🔄 Atualizar agora"):
    st.experimental_rerun()

# ==============================
# EXECUÇÃO
# ==============================
token = retorna_token()
if not token:
    st.stop()

lugar_ids = regionais.get(regional_sel, [])
if not lugar_ids:
    st.stop()

resultados = []
progress = st.progress(0)
for i, lid in enumerate(lugar_ids):
    res = get_vendas(lid, token)
    resultados.append(res)
    progress.progress((i + 1) / len(lugar_ids))
    time.sleep(0.1)

df = pd.DataFrame(resultados)
df = df.sort_values(by="vendasHoje", ascending=False)
df = df.set_index("lugarId")

hora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%H:%M:%S")

# ==============================
# EXIBIÇÃO
# ==============================
st.subheader(f"📍 Regional {regional_sel} — Atualizado às {hora_brasil}")

col1, col2 = st.columns(2)
col1.metric("Total de Vendas (hoje)", int(df["vendasHoje"].sum()))

st.dataframe(
    df[["lugarNome", "vendasHoje"]]
      .rename(columns={"lugarNome": "Filial", "vendasHoje": "Vendas (Hoje)"}),
    use_container_width=True,
    height=500,
)

st.caption("Para atualizar automaticamente, recarregue a página após o intervalo definido.")



