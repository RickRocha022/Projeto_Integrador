# 📌 Sistema de Gerenciamento de Chamados — Python + MySQL

## 📖 Sobre o Projeto
Este projeto é um sistema de gerenciamento de chamados desenvolvido em Python utilizando MySQL como banco de dados.  
O objetivo é simular um sistema interno de T.I., permitindo cadastrar usuários, abrir chamados, atualizar status, gerar estatísticas e organizar atendimentos de forma simples e prática.

O sistema funciona totalmente no terminal e possui:
- CRUD de usuários
- CRUD de chamados
- Sistema de prioridades
- Estatísticas automáticas
- Validações de entrada
- Integração com banco de dados MySQL
- Menu interativo estilizado

---

# 🛠 Tecnologias Utilizadas

- Python
- MySQL
- mysql.connector

---

# 📂 Estrutura do Projeto

```bash
Sistema/
│
├── main.py
├── banco.sql
└── README.md
```

---

# ⚙️ Funcionalidades

## 👤 Usuários
- Cadastrar usuários
- Listar usuários
- Buscar usuários por:
  - ID
  - Nome
  - E-mail
- Excluir usuários

---

## 🎫 Chamados
- Abrir chamados
- Listar chamados
- Buscar chamados por:
  - Prioridade
  - Status
- Atualizar status
- Excluir chamados

---

## 📊 Estatísticas
O sistema exibe:
- Quantidade de usuários cadastrados
- Quantidade total de chamados
- Chamados por status
- Chamados por prioridade
- Categoria mais acionada

---

# 🧠 Regras de Negócio

## 🔥 Sistema de Prioridade
A prioridade é calculada com base em:
- Urgência
- Impacto

### Escala:
| Valor | Significado |
|---|---|
| 1 | Baixo |
| 5 | Crítico |

---

# 🗄 Banco de Dados

O projeto utiliza:
- Tabela `usuarios`
- Tabela `categorias`
- Tabela `chamados`

Relacionamentos:
- Um usuário pode possuir vários chamados
- Um chamado pertence a uma categoria
- Ao excluir um usuário:
  - Os chamados permanecem no sistema
  - O usuário do chamado vira `NULL`

---

# ✅ Validações Implementadas

## 📌 Texto
- Não aceita vazio
- Aceita apenas letras

## 📌 Email
- Obrigatório conter `@`

## 📌 Inteiros
- Apenas números
- Controle de mínimo e máximo

## 📌 Telefone
- Apenas números

---

# 🎨 Interface do Menu

O sistema possui um menu organizado utilizando:
- Bordas Unicode
- Centralização de títulos
- Separação por categorias

Exemplo:

```bash
╔════════════════════════════════════╗
║      SISTEMA DE T.I. — MENU       ║
╠════════════════════════════════════╣
║             USUÁRIOS              ║
║  1 › Cadastrar usuário            ║
║  2 › Listar usuários              ║
╚════════════════════════════════════╝
```

---

# 🚀 Como Executar

## 1️⃣ Instalar dependências

```bash
pip install mysql-connector-python
```

---

## 2️⃣ Configurar o banco

No código:

```python
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SUA_SENHA",
    database="SEU_BANCO"
)
```

---

## 3️⃣ Executar

```bash
python main.py
```

---

# 📌 Conceitos Utilizados

O projeto trabalha diversos conceitos importantes:

- Funções
- Estruturas condicionais
- Loops
- Tratamento de exceções
- Modularização
- CRUD
- SQL
- JOIN
- Validações
- Relacionamentos entre tabelas
- Integração Python + MySQL

---

# 💡 Diferenciais do Projeto

✔ Sistema totalmente funcional  
✔ Integração real com banco de dados  
✔ Código comentado e explicativo  
✔ Menu estilizado  
✔ Validações completas  
✔ Estrutura organizada  
✔ Estatísticas automáticas  

---

# 📚 Objetivo Acadêmico

Projeto desenvolvido com foco em aprendizado de:
- Banco de dados
- Programação em Python
- Sistemas CRUD
- Estruturas de software
- Boas práticas de validação


