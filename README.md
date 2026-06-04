# 📌 Sistema de Gerenciamento de Chamados — Python + MySQL

## 📖 Descrição do Projeto

Este projeto consiste em um sistema de gerenciamento de chamados desenvolvido em Python com integração ao banco de dados MySQL.

O objetivo do sistema é simular um ambiente interno de suporte técnico de T.I., permitindo o cadastro de usuários, abertura de chamados, consultas, atualização de status e geração de estatísticas.

O sistema funciona por meio de um menu interativo em terminal e utiliza integração real com banco de dados relacional.

---

# 🎯 Objetivo do Projeto

Desenvolver uma aplicação CRUD completa utilizando:

* Python
* MySQL
* Integração com banco de dados
* Estruturas condicionais e de repetição
* Tratamento de exceções
* Validação de dados
* Versionamento com Git e GitHub

---

# 🛠 Tecnologias Utilizadas

* Python 3
* MySQL Server
* mysql-connector-python
* Git
* GitHub

---

# 📂 Estrutura do Projeto

```bash
Projeto/
│
├── sistema.py
├── bdTabelas.sql
└── README.md
```

---

# ⚙️ Funcionalidades

## 👤 Usuários

* Cadastro de usuários
* Listagem de usuários cadastrados
* Busca de usuários por ID
* Busca de usuários por nome
* Busca de usuários por e-mail
* Exclusão de usuários

## 🎫 Chamados

* Abertura de chamados
* Associação de chamados a usuários
* Associação de chamados a categorias
* Registro da descrição do problema
* Definição de urgência (1 a 5)
* Definição de impacto (1 a 5)
* Cálculo automático da prioridade
* Classificação automática do nível de prioridade
* Listagem de chamados
* Busca de chamados por prioridade
* Busca de chamados por status
* Atualização de status
* Exclusão de chamados

## 📊 Estatísticas

* Quantidade total de usuários cadastrados
* Quantidade total de chamados registrados
* Quantidade de chamados por status
* Quantidade de chamados por prioridade
* Categoria mais acionada

---

# 🧠 Regra de Prioridade

A prioridade dos chamados é calculada automaticamente pelo banco de dados utilizando os níveis de urgência e impacto informados durante a abertura do chamado.

Escala utilizada:

| Valor | Nível    |
| ----- | -------- |
| 1     | Baixo    |
| 2     | Moderado |
| 3     | Médio    |
| 4     | Alto     |
| 5     | Crítico  |

Fórmula utilizada:

Prioridade = (Urgência × 0,6) + (Impacto × 0,4)

A urgência possui peso de 60% no cálculo por representar a necessidade imediata de atendimento. O impacto possui peso de 40%, representando o alcance do problema.

Classificação automática da prioridade:

* Crítica: prioridade ≥ 4,2
* Alta: prioridade ≥ 3,2
* Média: prioridade ≥ 2,2
* Baixa: prioridade < 2,2

Os chamados são exibidos ordenados da maior para a menor prioridade.

---

# 🗄 Modelagem do Banco de Dados

O sistema utiliza três tabelas principais:

## usuarios

Armazena os dados dos usuários que registram chamados.

Campos principais:

* id
* nome
* email
* telefone

## categorias

Armazena as categorias disponíveis para classificação dos chamados.

Campos principais:

* id
* nome

Categorias cadastradas inicialmente:

* Sistema com falha
* Acesso bloqueado
* Impressora com erro
* Internet sem conexão

## chamados

Armazena os chamados registrados no sistema.

Campos principais:

* id
* usuario_id
* categoria_id
* descricao
* urgencia
* impacto
* prioridade
* nivel_prioridade
* status
* data_abertura

### Relacionamentos

* Um usuário pode possuir vários chamados.
* Uma categoria pode estar associada a vários chamados.
* Cada chamado pertence a um usuário e a uma categoria.
* Ao excluir um usuário, os chamados permanecem registrados e o campo usuario_id é definido como NULL (ON DELETE SET NULL), preservando o histórico das solicitações.

---

# ✅ Validações Implementadas

* Campos obrigatórios
* Validação de e-mail
* Telefone contendo apenas números
* Controle de valores mínimos e máximos
* Validação de IDs informados pelo usuário
* Tratamento de entradas inválidas
* Tratamento de exceções

---

# 🚀 Como Executar o Projeto

## 1️⃣ Instalar dependências

```bash
pip install mysql-connector-python
```

## 2️⃣ Criar o banco de dados

Criar um banco de dados MySQL e executar o script SQL:

```sql
SOURCE banco.sql;
```

## 3️⃣ Configurar a conexão

No arquivo main.py:

```python
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SUA_SENHA",
    database="SEU_BANCO"
)
```

## 4️⃣ Executar o sistema

```bash
python main.py
```

---

# 📌 Organização no GitHub

O projeto utiliza:

* Branch principal: main
* Histórico de commits da equipe
* GitHub Projects para gerenciamento das tarefas
* TAG final de entrega

---

# 📋 GitHub Projects

O quadro do GitHub Projects foi organizado utilizando as colunas:

* Backlog
* Em andamento
* Em revisão
* Concluído

As funcionalidades foram divididas em tarefas contendo:

* Responsável
* Status
* Progresso da implementação

---

# 🏷 Versionamento

A entrega final do projeto será identificada pela TAG:

```bash
v1.0
```

A TAG aponta para a versão estável contendo:

* Código-fonte
* Script SQL
* README
* Documentação exigida

---

# 🖥 Demonstração do Fluxo Principal

Fluxo principal do sistema:

1. Cadastro de usuário
2. Abertura de chamado
3. Consulta de chamados
4. Busca por prioridade ou status
5. Atualização de status
6. Visualização de estatísticas

---

# 📚 Conceitos Aplicados

* CRUD
* SQL
* JOIN
* Relacionamentos
* Estruturas condicionais
* Estruturas de repetição
* Tratamento de exceções
* Modularização
* Integração Python + MySQL

---

# 👨‍💻 Integrantes da Equipe

* Gabriel Henrique - 26000755
* Leonardo Santos - 26006146
* Lorenzo Dias Lanzoni - 26005161
* Pedro Beirigo - 26010891
* William da Silva Rocha - 26006208

---

# 📖 Considerações Finais

O projeto foi desenvolvido com foco acadêmico para aplicação prática de conceitos de programação, banco de dados relacionais e desenvolvimento de sistemas utilizando Python e MySQL.

A solução implementa operações CRUD completas, consultas, controle de status, estatísticas e cálculo automático de prioridade, atendendo aos requisitos propostos para o trabalho.
