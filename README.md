# Assistente Salarial Inteligente

Aplicação web didática que estima como a inflação acumulada afeta o poder de
compra de um salário. A pessoa informa o salário atual e há quantos meses não
recebe reajuste; ao clicar no botão, o programa consulta dados mensais do IPCA
na API do Banco Central do Brasil (BCB) e apresenta uma estimativa de salário
necessário para comprar hoje o equivalente ao que esse salário comprava no
início do período.

> **Importante:** esta é uma simulação educativa, não uma recomendação
> financeira, trabalhista ou jurídica. O resultado não determina reajuste
> obrigatório, aumento devido, salário de mercado nem a inflação pessoal de
> cada pessoa.

## O que a aplicação faz

1. Mostra um campo para informar o salário atual em reais.
2. Permite escolher um período de 1 a 60 meses sem reajuste.
3. Quando o botão é acionado, busca as observações mensais da série 433 do
   Sistema Gerenciador de Séries Temporais (SGS) do Banco Central.
4. Com essas observações, calcula a inflação acumulada por composição
   (inflação sobre inflação).
5. Exibe a inflação acumulada, o salário estimado para preservar o poder de
   compra e a diferença em relação ao salário informado.

Os dados são consultados quando o botão é clicado. O IPCA é divulgado
periodicamente e pode não ter um valor publicado para o mês mais recente.
Portanto, “dados em tempo real” não significa necessariamente que exista um
índice para todos os meses até hoje.

## Conceitos financeiros em linguagem simples

- **Inflação:** aumento generalizado dos preços ao longo do tempo. Quando os
  preços sobem, a mesma quantia de dinheiro costuma comprar menos.
- **IPCA:** Índice Nacional de Preços ao Consumidor Amplo. É um indicador de
  inflação calculado pelo IBGE e usado como referência oficial para acompanhar
  a variação de preços no Brasil. A série 433 consultada pelo programa contém
  a variação mensal do IPCA, em porcentagem.
- **Poder de compra:** quantidade de bens e serviços que uma quantia permite
  comprar. Se os preços aumentam e a renda não muda, o poder de compra tende
  a diminuir.
- **Salário nominal:** valor em reais que aparece no pagamento, sem descontar
  o efeito da inflação.
- **Salário necessário para reposição:** estimativa do valor que, após a
  inflação do período, compraria uma cesta equivalente à que o salário
  informado comprava no começo daquele período. Não é necessariamente um
  reajuste concedido ou garantido.
- **Inflação composta:** as variações mensais são multiplicadas, e não apenas
  somadas. Por exemplo, dois meses com inflação de 1% resultam em
  `(1 + 1/100) × (1 + 1/100) - 1 = 2,01%` de inflação acumulada.
- **BCB/BACEN:** Banco Central do Brasil, instituição responsável, entre
  outras atividades, por manter e disponibilizar séries de dados econômicos.
- **SGS:** Sistema Gerenciador de Séries Temporais do Banco Central, de onde a
  API usada pelo programa fornece os valores históricos.

### Como interpretar o resultado

Se o salário informado for R$ 1.000,00 e a inflação encontrada no período for
10%, a estimativa de reposição será R$ 1.100,00. A diferença de R$ 100,00 é
mostrada como perda estimada de poder de compra em reais por mês em relação ao
salário informado.

É uma aproximação baseada no IPCA geral. A inflação sentida por uma família
pode ser diferente, porque seus gastos e hábitos de consumo podem não ser
iguais à composição média do índice. O cálculo também depende das observações
mensais que a API retornar para as datas selecionadas.

## Como o código funciona

O programa está concentrado em [`app.py`](./app.py).

### Bibliotecas importadas

- **Streamlit (`streamlit`):** cria a página web e seus componentes, como
  campos, botão, mensagens e indicadores.
- **Pandas (`pandas`):** organiza os dados retornados pela API em uma tabela e
  ajuda a converter datas e números.
- **Plotly Express (`plotly.express`):** biblioteca para criar gráficos. Está
  importada no código, mas atualmente não é utilizada; a aplicação não exibe
  gráficos.
- **Requests (`requests`):** envia uma solicitação HTTP para a API do Banco
  Central.

### Busca de dados: `buscar_dados_bacen`

A função recebe um código de série e duas datas:

1. Monta o endereço da API SGS com o código recebido.
2. Envia as datas inicial e final e pede a resposta no formato JSON.
3. Se a resposta HTTP for bem-sucedida (código 200), transforma os registros
   recebidos em uma tabela Pandas.
4. Converte a coluna de data do formato `dia/mês/ano` para datas reconhecidas
   pelo programa e a coluna de valor para número.
5. Retorna a tabela. Se o servidor responder com um código diferente de 200,
   exibe uma mensagem de erro e retorna `None`.

O código menciona estas séries em uma descrição da função:

| Código SGS | Indicador descrito no código | Uso nesta versão |
|---|---|---|
| 432 | Taxa SELIC (% ao mês) | Apenas mencionado; não é consultado pela interface |
| 433 | IPCA (% ao mês) | Consultado pelo simulador |
| 4389 | PIB (% acumulado em quatro trimestres) | Apenas mencionado; não é consultado pela interface |
| 24369 | Taxa de desocupação (%) | Apenas mencionado; não é consultado pela interface |

### Interface e cálculo

- `st.title` e `st.write` exibem o título e a apresentação.
- `st.divider` e `st.subheader` separam e identificam a área do simulador.
- `st.number_input` recebe o salário. Nesta versão, o mínimo é R$ 100,00, o
  valor inicial é R$ 1.000,00 e o passo dos botões é R$ 100,00.
- `st.slider` escolhe o período entre 1 e 60 meses. O valor inicial é 24.
- O bloco `if st.button(...)` só executa a consulta e o cálculo depois que a
  pessoa clica no botão.
- `pd.Timestamp.today()` obtém a data atual e `pd.DateOffset` calcula uma
  data aproximada de início do período. As datas são formatadas como
  `dia/mês/ano` para a API.
- O programa busca a série 433. Se a tabela recebida existir e não estiver
  vazia, calcula o fator acumulado multiplicando `(1 + valor mensal / 100)`
  para cada observação e subtraindo 1 ao final.
- Multiplica o salário pelo fator acumulado mais 1 para estimar o salário de
  reposição; subtrai o salário original para obter a diferença estimada.
- `st.success`, `st.columns`, `st.metric` e `st.info` apresentam os valores.
  Se não houver observações utilizáveis, `st.error` informa que não foi
  possível fazer o cálculo.

### Siglas e termos de programação

- **API (Application Programming Interface):** uma forma padronizada para um
  programa solicitar dados ou serviços de outro. Aqui, o aplicativo pede
  dados ao Banco Central.
- **HTTP:** protocolo usado para a comunicação entre aplicações na web. Uma
  resposta com código `200` indica que a solicitação foi atendida com sucesso.
- **JSON (JavaScript Object Notation):** formato textual comum para troca de
  dados entre sistemas. A API devolve os registros nesse formato.
- **DataFrame:** tabela de dados do Pandas, com linhas e colunas.
- **`None`:** valor especial do Python que representa ausência de um objeto
  de resultado, usado aqui quando a resposta HTTP não é bem-sucedida.
- **`if`:** estrutura condicional; executa um bloco apenas quando uma
  condição é verdadeira.
- **Função:** trecho de código nomeado e reutilizável. Neste caso,
  `buscar_dados_bacen` concentra a consulta e a preparação dos dados.

## MCP e LLM: o que está simulado

O título de uma seção do código menciona **MCP** e **LLM**:

- **MCP (Model Context Protocol):** protocolo para conectar modelos de
  inteligência artificial a ferramentas e fontes de contexto.
- **LLM (Large Language Model, ou grande modelo de linguagem):** modelo de
  inteligência artificial treinado para compreender e gerar texto.

Apesar desses nomes aparecerem no título e no texto do botão, a implementação
atual **não se conecta a um servidor MCP nem a um LLM**. O botão chama
diretamente a função Python que consulta a API do Banco Central e calcula os
valores. Portanto, “simulando MCP” é apenas uma descrição da interface, não
uma integração implementada.

## Requisitos

- Python instalado no computador.
- Acesso à internet para consultar a API do Banco Central.
- As bibliotecas Python `streamlit`, `pandas`, `plotly` e `requests`.

Este repositório não inclui atualmente um arquivo de dependências como
`requirements.txt`; a instalação abaixo informa explicitamente as bibliotecas
usadas pelo código.

## Instalação e execução no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit pandas plotly requests
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador. Se a ativação do ambiente virtual
for bloqueada pela política do PowerShell, consulte a política configurada no
seu computador ou execute os comandos de instalação e execução com o Python
do ambiente virtual sem ativá-lo:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit pandas plotly requests
.\.venv\Scripts\streamlit.exe run app.py
```

## Limitações conhecidas

- Só o IPCA (série 433) é usado no cálculo apresentado.
- Os demais indicadores listados no código não aparecem como opções nem são
  exibidos pela interface atual.
- Não há gráficos na interface, apesar de Plotly estar importado.
- Não há integração com MCP ou LLM.
- A estimativa usa o índice geral de preços, não os gastos individuais da
  pessoa.
- O intervalo é aproximado a partir da data atual e da quantidade de meses; a
  disponibilidade e o período efetivo dependem das observações mensais
  devolvidas pela API.
- O aplicativo precisa de conexão com a internet para consultar os dados.
- A consulta HTTP não define um tempo limite e erros de conexão podem
  interromper a execução, pois a versão atual não trata exceções de rede.
