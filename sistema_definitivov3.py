import mysql.connector


# ─── CONEXÃO ───────────────────────────────────────────────

try:
    conexao = mysql.connector.connect(
        host="127.0.0.1",       # ou IP do servidor
        user="root",            # seu usuário
        password="gabierik2",   # sua senha
        database="BD24022618"   # nome do banco de dados
    )
    print("Conexão realizada com sucesso!")
    cursor = conexao.cursor()

except mysql.connector.Error as erro:
    print(f"Erro ao conectar: {erro}")
    exit()


# ─── UTILITÁRIOS ───────────────────────────────────────────

def ler_texto(prompt):
    valor = input(prompt).strip() 
    if not valor:
        print("Campo obrigatório! Não pode ficar em branco.")
        return None
    
    try:
        float(valor)
        print("Este campo não aceita valores numéricos.")
        return None
    
    except ValueError:
        return valor
    
"""
*input(prompt) --> pede um texto ao usuário. pede um texto ao usuário.
*strip() --> remove espaços em branco no começo e no final.
*tryexcept() --> tenta converter o valor para número. 
Se conseguir, mostra mensagem de erro, pois não pode ser número. 
Se não conseguir, retorna o texto normalmente.

"""

def ler_inteiro(prompt, minimo=None, maximo=None):
    """Lê um número inteiro com intervalo opcional."""
    try:
        valor = int(input(prompt).strip())
        if minimo is not None and valor < minimo:
            print(f"Valor mínimo: {minimo}")
            return None
        
        if maximo is not None and valor > maximo:
            print(f"Valor máximo: {maximo}")
            return None
        return valor
    
    except ValueError:
        print("Digite apenas números inteiros.")
        return None
    
"""
*(prompt, minimo=None, maximo=None)--> essa função lê um número inteiro e
pode limitar valores mínimos e máximos, de acordo com o que for passado na função.
*Faz o inverso do ler_texto: tenta converter o valor para inteiro. 
Se conseguir, verifica se está dentro dos limites.

"""


# ─── USUÁRIOS ──────────────────────────────────────────────

def cadastrar_usuario():
    try:
        nome = ler_texto("\nNome: ")
        if nome is None:
            return

        email = ler_texto("Email: ")
        if email is None:
            return

        telefone = input("Telefone: ").strip()
        if telefone:
            if not telefone.isdigit():
                print("Telefone deve conter apenas números!")
                return

        cursor.execute("""
            INSERT INTO usuarios (nome, email, telefone)
            VALUES (%s, %s, %s)
        """, (nome, email, telefone))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")

"""
*Telefone é opcional. Aceita vazio, mas só dígitos se preenchido.
*isdigit()--> função do python que garante que só tenha números de 0 a 9. 
Se tiver qualquer outro caractere, retorna False.

"""


def listar_usuarios():
    try:
        cursor.execute("SELECT id, nome, email, telefone FROM usuarios")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return

        print("\n" + "-" * 40)
        for u in usuarios:
            print(f"  ID       : {u[0]}")
            print(f"  Nome     : {u[1]}")
            print(f"  Email    : {u[2]}")
            print(f"  Telefone : {u[3] or '-'}")
            print("-" * 40)

    except Exception as e:
        print(f"Erro ao listar usuários: {e}")

"""
*fetchall()--> pega todos os registros retornados pela última consulta feita.
*u[3] or '-' --> se o telefone for vazio, mostra um traço no lugar.
*Esta forma de imprimir os usuários é mais organizada, 
com separação por linhas e colunas onde U representa o usuário e os numeros
os indices.

"""


# ─── CHAMADOS ──────────────────────────────────────────────

def abrir_chamado():
    try:
        cursor.execute("SELECT id, nome FROM usuarios")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNenhum usuário cadastrado. Cadastre um usuário primeiro.")
            return

        print("\nUsuários disponíveis:")
        for u in usuarios:
            print(f"  {u[0]} - {u[1]}")

        usuario_id = ler_inteiro("Informe o ID do usuário: ", minimo=1)
        if usuario_id is None:
            return

        cursor.execute("SELECT id, nome FROM categorias")
        categorias = cursor.fetchall()

        print("\nCategorias:")
        for c in categorias:
            print(f"  {c[0]} - {c[1]}")

        categoria_id = ler_inteiro("Informe o ID da categoria: ", minimo=1)
        if categoria_id is None:
            return

        descricao = ler_texto("Descrição do problema: ")
        if descricao is None:
            return

        print("\nUrgência (1 = baixa  →  5 = crítica)")
        urgencia = ler_inteiro("Urgência [1-5]: ", minimo=1, maximo=5)
        if urgencia is None:
            return

        print("Impacto  (1 = baixo  →  5 = alto)")
        impacto = ler_inteiro("Impacto  [1-5]: ", minimo=1, maximo=5)
        if impacto is None:
            return

        cursor.execute("""
            INSERT INTO chamados (usuario_id, categoria_id, descricao, urgencia, impacto)
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario_id, categoria_id, descricao, urgencia, impacto))
        conexao.commit()

        cursor.execute("""
            SELECT id, prioridade, nivel_prioridade, status
            FROM chamados
            WHERE id = LAST_INSERT_ID()
        """)
        sol = cursor.fetchone()

        print("\nChamado registrado!")
        print(f"   ID           : {sol[0]}")
        print(f"   Prioridade   : {sol[1]}")
        print(f"   Nível        : {sol[2]}")
        print(f"   Status       : {sol[3]}")

    except Exception as e:
        print(f"Erro ao abrir chamado: {e}")

"""
*print(f"  {u[0]} - {u[1]}") --> esta em formatado de tupla,
onde u[0] é o id do usuário e u[1] é o nome do usuário (funciona assim para todas).
*o valor minino é colocado para evitar que o usuário informe um id negativo ou zero,
que não existe. Ele é aplicado na função ler_inteiro, que já foi criada.
*LAST_INSERT_ID()--> função do MySQL que retorna o ID do último registro inserido na tabela.

"""


def listar_chamados():
    try:
        cursor.execute("""
            SELECT s.id, u.nome, c.nome, s.descricao,
                   s.urgencia, s.impacto, s.prioridade,
                   s.nivel_prioridade, s.status, s.data_abertura
            FROM chamados s
            JOIN usuarios   u ON s.usuario_id   = u.id
            JOIN categorias c ON s.categoria_id = c.id
            ORDER BY s.prioridade DESC
        """)
        chamados = cursor.fetchall()

        if not chamados:
            print("\nNenhum chamado cadastrado.")
            return

        print("\n" + "-" * 40)
        for s in chamados:
            print(f"  ID         : {s[0]}")
            print(f"  Usuário    : {s[1]}")
            print(f"  Categoria  : {s[2]}")
            print(f"  Descrição  : {s[3]}")
            print(f"  Urgência   : {s[4]}")
            print(f"  Impacto    : {s[5]}")
            print(f"  Prioridade : {s[6]}")
            print(f"  Nível      : {s[7]}")
            print(f"  Status     : {s[8]}")
            print(f"  Aberto em  : {s[9]}")
            print("-" * 40)

    except Exception as e:
        print(f"Erro ao listar chamados: {e}")

"""
*Join junta as tabelas chamados, usuarios e categorias para exibir informações completas.
*ORDER BY s.prioridade DESC --> ordena os chamados pela prioridade, do mais alto para o mais baixo.
"""


def buscar_por_prioridade():
    try:
        niveis = {"1": "Baixa", "2": "Média", "3": "Alta", "4": "Crítica"}

        print("\nFiltrar por nível de prioridade:")
        print("  1 - Baixa")
        print("  2 - Média")
        print("  3 - Alta")
        print("  4 - Crítica")

        opcao = input("Escolha: ").strip()

        if opcao not in niveis:
            print("Opção inválida!")
            return

        nivel_escolhido = niveis[opcao]

        cursor.execute("""
            SELECT s.id, u.nome, c.nome, s.descricao,
                   s.urgencia, s.impacto, s.prioridade,
                   s.nivel_prioridade, s.status, s.data_abertura
            FROM chamados s
            JOIN usuarios   u ON s.usuario_id   = u.id
            JOIN categorias c ON s.categoria_id = c.id
            WHERE s.nivel_prioridade = %s
            ORDER BY s.prioridade DESC
        """, (nivel_escolhido,))

        chamados = cursor.fetchall()

        if not chamados:
            print(f"\nNenhum chamado encontrado com prioridade '{nivel_escolhido}'.")
            return

        print(f"\n  Chamados com prioridade: {nivel_escolhido}  ({len(chamados)} encontrado(s))")
        print("-" * 40)
        for s in chamados:
            print(f"  ID         : {s[0]}")
            print(f"  Usuário    : {s[1]}")
            print(f"  Categoria  : {s[2]}")
            print(f"  Descrição  : {s[3]}")
            print(f"  Urgência   : {s[4]}")
            print(f"  Impacto    : {s[5]}")
            print(f"  Prioridade : {s[6]}")
            print(f"  Nível      : {s[7]}")
            print(f"  Status     : {s[8]}")
            print(f"  Aberto em  : {s[9]}")
            print("-" * 40)

    except Exception as e:
        print(f"Erro ao buscar por prioridade: {e}")


# ─── STATUS ────────────────────────────────────────────────

def atualizar_status():
    try:
        cursor.execute("SELECT id, status FROM chamados")
        chamados = cursor.fetchall()

        if not chamados:
            print("\nNenhum chamado encontrado.")
            return

        print("\nChamados disponíveis:")
        for c in chamados:
            print(f"  ID: {c[0]}  |  Status atual: {c[1]}")

        chamado_id = ler_inteiro("\nDigite o ID do chamado: ", minimo=1)
        if chamado_id is None:
            return

        print("\nNovo status:")
        print("  1 - Aberto")
        print("  2 - Em andamento")
        print("  3 - Resolvido")

        opcao = input("Escolha: ").strip()

        status_map = {
            "1": "Aberto",
            "2": "Em andamento",
            "3": "Resolvido",
        }

        if opcao not in status_map:
            print("Opção inválida!")
            return

        novo_status = status_map[opcao]

        cursor.execute("""
            UPDATE chamados
            SET status = %s
            WHERE id = %s
        """, (novo_status, chamado_id))
        conexao.commit()

        if cursor.rowcount == 0:
            print("ID não encontrado.")
        else:
            print(f"Status atualizado para '{novo_status}' com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar status: {e}")

"""
*rowcount--> retorna o número de linhas afetadas por uma operação SQL
Se for 0, significa que o ID do chamado não foi encontrado.
Se for 1, a atualização foi bem-sucedida.

"""


# ─── ESTATÍSTICAS ───────────────────────────────────────────

def estatisticas():
    try:
        # Total de usuários
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]

        # Total de chamados
        cursor.execute("SELECT COUNT(*) FROM chamados")
        total_chamados = cursor.fetchone()[0]

        # Chamados por status
        cursor.execute("SELECT status, COUNT(*) FROM chamados GROUP BY status")
        por_status = cursor.fetchall()

        # Chamados por nível de prioridade
        cursor.execute("SELECT nivel_prioridade, COUNT(*) FROM chamados GROUP BY nivel_prioridade")
        por_prioridade = cursor.fetchall()

        # Categoria com mais chamados
        cursor.execute("""
            SELECT c.nome, COUNT(*) AS total
            FROM chamados s
            JOIN categorias c ON s.categoria_id = c.id
            GROUP BY c.nome
            ORDER BY total DESC
            LIMIT 1
        """)
        top_categoria = cursor.fetchone()


        print("\n" + "=" * 40)
        print("         ESTATÍSTICAS DO SISTEMA")
        print("=" * 40)
        print(f"  Usuários cadastrados : {total_usuarios}")
        print(f"  Total de chamados    : {total_chamados}")

        print("\n  Chamados por status:")
        for s in por_status:
            print(f"    {s[0]:<15}: {s[1]}")

        print("\n  Chamados por prioridade:")
        for p in por_prioridade:
            print(f"    {p[0]:<15}: {p[1]}")

        if top_categoria:
            print(f"\n  Categoria mais acionada: {top_categoria[0]} ({top_categoria[1]} chamado(s))")

        print("=" * 40)

    except Exception as e:
        print(f"Erro ao carregar estatísticas: {e}")

"""
*{s[0]:<15}: {s[1]} --> formata a string para alinhar à esquerda em um campo de 15 caracteres,
seguido do número de chamados. Isso cria uma exibição mais organizada.

"""


# ─── MENU ──────────────────────────────────────────────────

def menu_principal():
    while True:
        print("\n╔═══════════════════════════════╗")
        print("║      SISTEMA T.I. — MENU      ║")
        print("╠═══════════════════════════════╣")
        print("║  1 - Cadastrar usuário        ║")
        print("║  2 - Listar usuários          ║")
        print("║  3 - Abrir chamado            ║")
        print("║  4 - Listar chamados          ║")
        print("║  5 - Buscar por prioridade    ║")
        print("║  6 - Atualizar status         ║")
        print("║  7 - Estatísticas             ║")
        print("║  0 - Sair                     ║")
        print("╚═══════════════════════════════╝")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            abrir_chamado()
        elif opcao == "4":
            listar_chamados()
        elif opcao == "5":
            buscar_por_prioridade()
        elif opcao == "6":
            atualizar_status()
        elif opcao == "7":
            estatisticas()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")


menu_principal()

if conexao.is_connected():
    cursor.close()
    conexao.close()
    print("Conexão encerrada.")