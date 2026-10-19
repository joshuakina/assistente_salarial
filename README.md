# Assistente Salarial Inteligente

## Introdução

Este programa mostra quanto o seu salário perdeu de valor por causa da inflação.

Você informa:

- o valor do seu salário atual;  
- há quantos meses ele está sem reajuste.

O programa busca a inflação oficial do Brasil (índice **IPCA**) no site do **Banco Central** e calcula:

- a inflação acumulada no período;  
- o salário que você precisaria ganhar hoje para manter o mesmo poder de compra;  
- quanto você perdeu em reais.

O programa abre como uma página web simples, com campos para preencher e um botão para calcular.

---

## Requisitos

Para usar o programa, você precisa de:

- **Python 3.9 ou mais novo** (linguagem em que o programa foi escrito) → [https\://www\.python.org/downloads/](https://www.python.org/downloads/)

Para conferir se o Python e o Git estão instalados, abra o terminal e digite:

```sh
python --version
```

&nbsp;

Se aparecer um número de versão nos dois, está tudo certo.

---

## Como montar o ambiente

Siga os passos na ordem.

**Passo 1\.** Crie uma pasta para o projeto e entre nela:

```sh
mkdir assistente-salarial
cd assistente-salarial
```

&nbsp;

**Passo 2\.** Salve o código do programa nesta pasta com o nome `app.py`.

**Passo 3\.** Crie um ambiente virtual (um espaço isolado só para este projeto, que evita conflitos com outros programas Python do seu computador):

```sh
python -m venv venv
```

&nbsp;

**Passo 4\.** Ative o ambiente virtual:

- Windows:

```sh
venv\Scripts\activate
```

- Mac ou Linux:

```sh
source venv/bin/activate
```

Quando funcionar, aparecerá `(venv)` no início da linha do terminal.

**Passo 5\.** Instale as bibliotecas necessárias (ver seção 5):

## Arquivo requirements.txt

```
streamlit
pandas
requests
```

&nbsp;

O que cada biblioteca faz:

| Biblioteca | Função |
| :---- | :---- |
| `streamlit` | Cria a página web com campos, botão e resultados |
| `pandas` | Organiza os dados em tabela e faz os cálculos |
| `requests` | Faz a consulta à internet para buscar os dados do Banco Central |

&nbsp;

---

```sh
pip install -r requirements.txt
```

&nbsp;

**Passo 6\.** Execute o programa:

```sh
streamlit run app.py
```

&nbsp;

O navegador abrirá automaticamente. Se não abrir, acesse: [http\://localhost:8501](http://localhost:8501)

Para fechar o programa, volte ao terminal e pressione `Ctrl + C`.

---

## Explicação do código

O código tem três partes.

### Parte 1: Importações

Carrega as três bibliotecas descritas do requirements.

### Parte 2: Função `buscar_dados_bacen`

Responsável por buscar dados no Banco Central.

1. Recebe três informações: o **código da série**, a **data inicial** e a **data final**.  
2. Monta o endereço da API do Banco Central com esses dados.  
3. Faz a consulta pela internet.  
4. Se a consulta der certo, transforma a resposta em tabela, converte a coluna `data` para formato de data e a coluna `valor` para número.  
5. Se der errado, mostra uma mensagem de erro na tela.

Códigos de séries do Banco Central citados no código:

| Código | Indicador |
| :---- | :---- |
| 432 | Taxa Selic (% ao mês) |
| 433 | IPCA, a inflação (% ao mês) |
| 4389 | PIB (% acumulado em 4 trimestres) |
| 24369 | Taxa de desocupação (%) |

&nbsp;

Neste programa, apenas o código **433 (IPCA)** é usado.

### Parte 3: Tela e cálculo

1. **Título e texto**: mostram o nome do programa e uma breve descrição.  
2. **Campo de salário**: aceita valor mínimo de R$100,00,comvalorinicialdeR$ 1.000,00.  
3. **Controle deslizante**: permite escolher de 1 a 60 meses sem reajuste, com valor inicial de 24\.  
4. **Botão "Calcular Perda de Poder de Compra"**: ao ser clicado, executa os passos abaixo.  
   1. Define a data final como o dia de hoje.  
   2. Define a data inicial subtraindo os meses escolhidos da data de hoje.  
   3. Busca o IPCA mensal desse período.  
   4. Calcula a inflação acumulada (ver seção 8).  
   5. Calcula o salário necessário e a perda em reais.  
   6. Exibe três indicadores e um texto explicativo.  
   7. Se não houver dados, mostra uma mensagem de erro.

---

## 7\. O que o código faz (passo a passo para o usuário)

1. Você abre a página do programa.  
2. Digita o seu salário atual.  
3. Escolhe há quantos meses está sem reajuste.  
4. Clica no botão de calcular.  
5. O programa consulta o Banco Central.  
6. A tela mostra três resultados:  
   - **Inflação Acumulada no Período**: o quanto os preços subiram em porcentagem.  
   - **Salário Necessário para Repor**: quanto você precisaria ganhar hoje para comprar o mesmo que comprava antes.  
   - **Perda de Poder de Compra**: a diferença, em reais, entre o salário necessário e o salário que você tem.  
7. Um texto final resume os resultados em linguagem simples.

**Limitações importantes:**

- O IPCA de um mês só é divulgado no mês seguinte. Por isso, o período calculado pode não incluir o mês mais recente.  
- O resultado é uma **estimativa** baseada na média de preços do país. A inflação que você sente pode ser diferente, dependendo do que você consome.  
- O programa precisa de internet. Sem conexão, ou se o site do Banco Central estiver fora do ar, o cálculo não funciona.

---

## 8\. Conceitos financeiros explicados

### Inflação

É o aumento geral dos preços de produtos e serviços ao longo do tempo. Quando há inflação, com o mesmo dinheiro você compra menos coisas.

### IPCA

Sigla de **Índice Nacional de Preços ao Consumidor Amplo**. É o índice oficial de inflação do Brasil, calculado pelo IBGE. O Banco Central disponibiliza os valores mensais na série de código 433\. Cada valor mostra quanto os preços subiram naquele mês, em porcentagem.

### Poder de compra

É a quantidade de produtos e serviços que você consegue comprar com o seu dinheiro. Se os preços sobem e o salário continua igual, o poder de compra diminui.

### Reajuste salarial

É o aumento do salário. Um reajuste igual à inflação mantém o poder de compra. Um reajuste menor que a inflação, ou nenhum reajuste, reduz o poder de compra.

### Inflação acumulada

É o aumento total dos preços em vários meses seguidos. Ela **não é a soma** das inflações de cada mês. Cada mês é calculado sobre os preços já reajustados no mês anterior. Esse método é chamado de **cálculo composto**.

Fórmula usada no código:

```
Inflação acumulada = (1 + i1/100) × (1 + i2/100) × ... × (1 + in/100) − 1
```

&nbsp;

Onde `i1, i2, ..., in` são os IPCAs de cada mês.

**Exemplo:** dois meses com inflação de 0,50% e 0,40%.

- Soma simples: 0,50 \+ 0,40 \= 0,90%  
- Cálculo composto: 1,005 × 1,004 \= 1,00902, ou seja, **0,902%**

A diferença é pequena em poucos meses, mas cresce em períodos longos.

### Salário necessário para repor

É o salário atual corrigido pela inflação acumulada:

```
Salário necessário = Salário atual × (1 + inflação acumulada)
```

&nbsp;

**Exemplo:** salário de R$1.000,00 e inflação acumuladade 10%.Salário necessário = 1.000 × 1,10 = **R$ 1.100,00\*\*

### Perda de poder de compra

É a diferença entre o salário necessário e o salário atual:

```
Perda = Salário necessário − Salário atual
```

&nbsp;

No exemplo acima: 1.100 − 1.000 \= **R\$ 100,00**. Esse é o valor que falta no seu salário para comprar o mesmo que você comprava antes.

### Selic, PIB e desocupação (citados no código)

Esses indicadores aparecem apenas como referência nos comentários da função e **não entram no cálculo atual**:

- **Selic**: taxa básica de juros da economia, definida pelo Banco Central.  
- **PIB**: soma de tudo o que o país produz, usada para medir o crescimento da economia.  
- **Taxa de desocupação**: porcentagem de pessoas que procuram trabalho e não encontram.

---

## Estrutura final do projeto

```
assistente-salarial/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

&nbsp;