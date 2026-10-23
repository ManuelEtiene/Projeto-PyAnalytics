import pandas as pd
import streamlit as st

# Configuração da página em modo 'wide'
st.set_page_config(
    page_title="Portal de Saúde - Araranguá", page_icon="🏥", layout="wide"
)

# Estilo visual personalizado (Banner semelhante ao Portal de Saúde)
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #0052cc 0%, #003380 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    .main-header p {
        color: #d0e1fd;
        font-size: 1.05rem;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0052cc;
        margin-bottom: 15px;
    }
    </style>
    <div class="main-header">
        <h1>🏥 Portal de Saúde de Araranguá</h1>
        <p>Transparência e acompanhamento analítico de vacinação e indicadores municipais.</p>
    </div>
""",
    unsafe_allow_html=True,
)


# Carregar os dados com cache
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/vacinas_analitico.csv")
    return df


df = carregar_dados()

# --- BARRA LATERAL (Filtros e Categorias estilo Portal) ---
st.sidebar.header("🔍 Filtros Avançados")

colunas_texto = df.select_dtypes(include=["object"]).columns.tolist()

# Filtro de categoria principal (se houver colunas de texto)
categoria_filtro = None
if colunas_texto:
    col_cat = st.sidebar.selectbox(
        "Agrupar por Categoria:", colunas_texto, index=0
    )
    opcoes = ["Todas"] + list(df[col_cat].dropna().unique()[:20])
    escolha = st.sidebar.selectbox(f"Filtrar {col_cat}:", opcoes)
    if escolha != "Todas":
        df = df[df[col_cat] == escolha]

st.sidebar.divider()
st.sidebar.info(
    "💡 Dica: Utilize as abas ao lado para navegar entre a visão geral, gráficos e os dados detalhados."
)

# --- CORPO PRINCIPAL COM ABAS (Tabs) ---
tab_geral, tab_graficos, tab_tabela = st.tabs(
    ["📊 Visão Geral", "📈 Gráficos Analíticos", "📋 Dados Detalhados"]
)

with tab_geral:
    # Métricas principais em destaque
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            label="Total de Registos",
            value=f"{df.shape[0]:,}".replace(",", "."),
        )
    with c2:
        st.metric(label="Total de Colunas", value=df.shape[1])
    with c3:
        if colunas_texto:
            st.metric(
                label="Categorias Únicas",
                value=df[colunas_texto[0]].nunique(),
            )

    st.divider()

    st.markdown("### 📌 Resumo Executivo")
    st.write(
        "Bem-vindo ao painel analítico. Este ambiente foi estruturado para "
        "permitir o acompanhamento detalhado dos indicadores de saúde do município com alto desempenho."
    )

    # Exemplo de cartão visual
    st.markdown(
        """
        <div class="card">
            <h4>💡 Estado Atual do Filtro</h4>
            <p>A exibir dados filtrados com base nas seleções ativas na barra lateral. Utilize as abas superiores para alternar para os gráficos detalhados.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with tab_graficos:
    st.subheader("📈 Análise de Distribuição")
    if colunas_texto:
        col_graf = st.selectbox(
            "Selecione o campo para gerar o gráfico de barras:",
            colunas_texto,
            key="graf_sel",
        )
        if col_graf:
            contagem = df[col_graf].value_counts().head(10)
            st.bar_chart(contagem)
    else:
        st.warning(
            "Não foram encontradas colunas categóricas suficientes para gráficos."
        )

with tab_tabela:
    st.subheader("📋 Tabela de Registos Brutos")
    st.dataframe(df, use_container_width=True)