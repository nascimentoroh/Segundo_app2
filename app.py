import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. Base de Dados Interna (Mock Data)
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    dados = [
        {"Item": "Compra de Chapas de Aço", "Categoria": "Matéria-Prima", "Valor (R$)": 6500.00, "Prioridade": "Alta"},
        {"Item": "Pagamento Equipe de Solda", "Categoria": "Mão de Obra", "Valor (R$)": 5000.00, "Prioridade": "Alta"},
        {"Item": "Frete e Transporte Urbano", "Categoria": "Logística", "Valor (R$)": 1800.00, "Prioridade": "Média"},
        {"Item": "Conta de Energia Industrial", "Categoria": "Energia", "Valor (R$)": 2200.00, "Prioridade": "Alta"},
        {"Item": "Kits de Ferramentas Manuais", "Categoria": "Ferramentas", "Valor (R$)": 1200.00, "Prioridade": "Baixa"},
        {"Item": "Insumos Eletrônicos", "Categoria": "Matéria-Prima", "Valor (R$)": 3100.00, "Prioridade": "Média"},
        {"Item": "Consultoria Técnica Externa", "Categoria": "Mão de Obra", "Valor (R$)": 4000.00, "Prioridade": "Baixa"},
        {"Item": "Combustível Frota Própria", "Categoria": "Logística", "Valor (R$)": 1500.00, "Prioridade": "Média"},
        {"Item": "Manutenção Preventiva Máquinas", "Categoria": "Energia", "Valor (R$)": 2800.00, "Prioridade": "Média"},
        {"Item": "Substituição Brocas e Discos", "Categoria": "Ferramentas", "Valor (R$)": 950.00, "Prioridade": "Alta"},
    ]
    return pd.DataFrame(dados)

df_base = carregar_dados()

# -----------------------------------------------------------------------------
# 3. Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Configurações do Simulador")

# Controles de Entrada
orcamento_total = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
    format="R$ %.2f"
)

categorias_disponiveis = df_base["Categoria"].unique().tolist()

categorias_selecionadas = st.sidebar.multiselect(
    label="Filtrar por Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

# -----------------------------------------------------------------------------
# 4. Processamento dos Dados
# -----------------------------------------------------------------------------
# Filtragem do DataFrame
if categorias_selecionadas:
    df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]
else:
    df_filtrado = df_base.iloc[0:0]  # Retorna DataFrame vazio se nada for selecionado

# Cálculos Chave
gasto_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_filtrado

# -----------------------------------------------------------------------------
# 5. Área Principal (Main Page)
# -----------------------------------------------------------------------------
st.title("📊 Simulador de Custos e Orçamento")
st.markdown("Painel interativo para monitoramento de despesas operacionais e controle orçamentário.")

st.divider()

# Painel de Métricas Topo
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Orçamento Definido",
    value=f"R$ {orcamento_total:,.2f}"
)

col2.metric(
    label="Gasto Filtrado",
    value=f"R$ {gasto_filtrado:,.2f}"
)

col3.metric(
    label="Saldo Restante",
    value=f"R$ {saldo_restante:,.2f}",
    delta=f"R$ {saldo_restante:,.2f}",
    delta_color="normal"  # Verde se positivo, vermelho se negativo
)

st.write("")

# Alertas Dinâmicos
if gasto_filtrado <= orcamento_total:
    st.success(f"✅ **Projeto dentro da meta!** Você ainda possui **R$ {saldo_restante:,.2f}** de margem orçamentária.")
else:
    excedente = abs(saldo_restante)
    st.error(f"⚠️ **Atenção: Orçamento Excedido!** As despesas selecionadas ultrapassam a meta em **R$ {excedente:,.2f}**.")

st.divider()

# Layout em 2 colunas para Gráfico e Tabela
col_grafico, col_tabela = st.columns([1, 1])

with col_grafico:
    st.subheader("📈 Gastos por Categoria")
    if not df_filtrado.empty:
        # Agrupamento para o gráfico
        df_agrupado = df_filtrado.groupby("Categoria", as_index=False)["Valor (R$)"].sum()
        
        # Gráfico de barras nativo (horizontal via altair interno)
        st.bar_chart(
            df_agrupado,
            x="Categoria",
            y="Valor (R$)",
            use_container_width=True
        )
    else:
        st.info("Nenhuma categoria selecionada para exibir o gráfico.")

with col_tabela:
    st.subheader("📋 Detalhamento dos Itens")
    if not df_filtrado.empty:
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor (R\()": st.column_config.NumberColumn(format="R\) %.2f")
            }
        )
    else:
        st.warning("Selecione ao menos uma categoria na barra lateral para visualizar os itens.")
