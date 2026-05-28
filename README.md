# 📌 Sistema de Gerenciamento de Chamados — Python + MySQL

## 📖 Descrição do Projeto

Este projeto consiste em um sistema de gerenciamento de chamados desenvolvido em Python com integração ao banco de dados MySQL.

O objetivo do sistema é simular um ambiente interno de suporte técnico de T.I., permitindo o cadastro de usuários, abertura de chamados, controle de status, consultas e geração de estatísticas.

O sistema funciona via terminal e utiliza integração real com banco de dados relacional.

---

# 🎯 Objetivo do Projeto

Desenvolver uma aplicação CRUD completa utilizando:

- Python
- MySQL
- Integração com banco de dados
- Estruturas condicionais e de repetição
- Tratamento de exceções
- Validação de dados
- Versionamento com Git e GitHub

---

# 🛠 Tecnologias Utilizadas

- Python 3
- MySQL Server
- mysql-connector-python
- Git/GitHub

---

# 📂 Estrutura do Projeto

```bash
Projeto/
│
├── main.py
├── banco.sql
├── README.md
└── assets/
```

---

# ⚙️ Funcionalidades

## 👤 Usuários
- Cadastro de usuários
- Listagem de usuários
- Busca por ID, nome e e-mail
- Exclusão de usuários

## 🎫 Chamados
- Abertura de chamados
- Listagem de chamados
- Busca por prioridade
- Busca por status
- Atualização de status
- Exclusão de chamados

## 📊 Estatísticas
- Quantidade de usuários
- Quantidade de chamados
- Chamados por status
- Chamados por prioridade
- Categoria mais acionada

---

# 🧠 Regras de Prioridade

A prioridade dos chamados é definida através dos níveis de:

- Urgência
- Impacto

Os valores variam de:

| Valor | Nível |
|---|---|
| 1 | Baixo |
| 5 | Crítico |

O sistema utiliza essas informações para organizar os chamados automaticamente por prioridade.

---

# 🗄 Modelagem do Banco de Dados

O sistema utiliza três tabelas principais:

- usuarios
- categorias
- chamados

## Relacionamentos

- Um usuário pode possuir vários chamados
- Cada chamado pertence a uma categoria
- Ao excluir um usuário:
  - Os chamados permanecem registrados
  - O usuário associado torna-se NULL

---

# ✅ Validações Implementadas

- Campos obrigatórios
- Validação de e-mail
- Apenas números para telefone
- Controle de valores mínimos e máximos
- Tratamento de entradas inválidas

---

# 🚀 Como Executar o Projeto

## 1️⃣ Instalar dependências

```bash
pip install mysql-connector-python
```

---

## 2️⃣ Configurar o banco de dados

Criar o banco MySQL e executar o script SQL:

```sql
SOURCE banco.sql;
```

---

## 3️⃣ Configurar conexão

No arquivo principal:

```python
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SUA_SENHA",
    database="SEU_BANCO"
)
```

---

## 4️⃣ Executar o sistema

```bash
python main.py
```

---

# 📌 Organização no GitHub

O projeto segue os requisitos de versionamento utilizando:

- Branch principal: `main`
- Histórico de commits individuais
- GitHub Projects para organização das tarefas
- TAG final de entrega (`v1.0`)

---

# 📋 GitHub Projects

O quadro do GitHub Projects foi organizado utilizando as colunas:

- Backlog
- Em andamento
- Em revisão
- Concluído

Cada funcionalidade do sistema foi separada em tarefas individuais contendo:
- Responsável
- Status
- Progresso da implementação

---

# 🏷 Versionamento

A entrega final do projeto será marcada utilizando uma TAG:

```bash
v1.0
```

A TAG apontará para a versão estável contendo:
- Código-fonte
- README completo
- Script SQL
- Documentação mínima exigida

---

# 👨‍💻 Integrantes da Equipe

- Leonardo Santos
- William da Silva Rocha - 26006208
- Gabriel Henrique - 26000755
- Lorenzo Dias Lanzoni - 26005161
- Pedro Beirigo - 26010891

---

# 📚 Conceitos Aplicados

- CRUD
- SQL
- JOIN
- Relacionamentos
- Estruturas de repetição
- Estruturas condicionais
- Tratamento de exceções
- Modularização
- Integração Python + MySQL

---

# ✅ Status do Projeto

✔ Funcional  
✔ Integrado ao MySQL  
✔ CRUD completo  
✔ Estatísticas implementadas  
✔ Menu interativo  
✔ Validações implementadas  

---

# 🖥 Demonstração do Fluxo Principal

O sistema permite executar o seguinte fluxo:

1. Cadastro de usuário
2. Abertura de chamado
3. Consulta de chamados
4. Atualização de status
5. Visualização de estatísticas

---

# 📖 Considerações Finais

O projeto foi desenvolvido com foco acadêmico para prática de desenvolvimento backend, integração com banco de dados relacionais e utilização de boas práticas de organização e versionamento utilizando GitHub.
