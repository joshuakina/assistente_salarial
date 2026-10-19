import streamlit as st
import pandas as pd
import requests

# Função para buscar dados da API do BACEN
def buscar_dados_bacen(codigo, data_inicio, data_fim):
    """Busca dados de uma série temporal do Banco Central
        Taxa SELIC (% a.m.): 432,
        IPCA - Inflação (% a.m.)" 433,
        PIB (% acumulado 4 trimestres): 4389,
        Taxa de Desocupação (%): 24369
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    params = {
        "formato": "json",
        "dataInicial": data_inicio,
        "dataFinal": data_fim
    }
    
    resposta = requests.get(url, params=params)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        df = pd.DataFrame(dados)
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        return df
    else:
        st.error(f"Erro ao buscar dados da série {codigo}")
        return None

# Título principal
st.title("Assistente Salarial Inteligente")
st.write("Simule o impacto da inflação (IPCA do Banco Central) no seu poder de compra com base em tempo real.")

salario_usuario = st.number_input("Digite o valor do seu salário atual (R$):", min_value=100.0, value=1000.0, step=100.0)
meses_atras = st.slider("Há quantos meses seu salário está sem reajuste?", min_value=1, max_value=60, value=24)

if st.button("Calcular Perda de Poder de Compra"):
    # Calcula data de início aproximada baseada nos meses escolhidos
    data_fim_calc = pd.Timestamp.today()
    data_inicio_calc = data_fim_calc - pd.DateOffset(months=meses_atras)
    
    # Busca dados do IPCA (código 433)
    df_ipca = buscar_dados_bacen(433, data_inicio_calc.strftime("%d/%m/%Y"), data_fim_calc.strftime("%d/%m/%Y"))
    
    if df_ipca is not None and not df_ipca.empty:
        # Soma a inflação composta do período
        # Fórmula de correção acumulada: (1 + i1/100) * (1 + i2/100) ... - 1
        fator_acumulado = (1 + df_ipca['valor'] / 100).prod() - 1
        inflacao_acumulada_pct = fator_acumulado * 100
        
        salario_necessario = salario_usuario * (1 + fator_acumulado)
        perda_estimada = salario_necessario - salario_usuario
        
        st.success("Dados obtidos com sucesso via API do Banco Central")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Inflação Acumulada no Período", f"{inflacao_acumulada_pct:.2f}%")
        with col_b:
            st.metric("Salário Necessário para Repor", f"R$ {salario_necessario:.2f}")
        with col_c:
            st.metric("Perda de Poder de Compra", f"R$ {perda_estimada:.2f}", delta_color="inverse")
            
        st.info(
                f"Com base nos dados oficiais do Banco Central (IPCA), nos últimos {meses_atras} meses "
                f"a inflação acumulada foi de **{inflacao_acumulada_pct:.2f}%**. "
                f"Isso significa que para comprar exatamente as mesmas coisas que você comprava antes com seus **{salario_usuario:.2f} reais**, "
                f"hoje você precisaria ganhar **{salario_necessario:.2f} reais**. Na prática, houve uma perda de poder de compra de **{perda_estimada:.2f} Reais** por mês.")
    else:
        st.error("Não foi possível calcular o índice para o período selecionado.")