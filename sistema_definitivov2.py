import mysql.connector


# ─── CONEXÃO ───────────────────────────────────────────────

try:
    conexao = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="gabierik2",
        database="BD24022618"
    )
    print("Conexão realizada com sucesso!")
    cursor = conexao.cursor()

except mysql.connector.Error as erro:
    print(f"Erro ao conectar: {erro}")
    exit()


# ─── UTILITÁRIOS ───────────────────────────────────────────

def ler_texto(prompt):
    """Lê um texto obrigatório — não aceita vazio nem número."""
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


# ─── USUÁRIOS ──────────────────────────────────────────────

def cadastrar_usuario():
    try:
        nome = ler_texto("\nNome: ")
        if nome is None:
            return

        email = ler_texto("Email: ")
        if email is None:
            return

        # Telefone é opcional — aceita vazio, mas só dígitos se preenchido
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
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")


# ─── INÍCIO ────────────────────────────────────────────────

menu_principal()

# ─── ENCERRAMENTO ──────────────────────────────────────────

if conexao.is_connected():
    cursor.close()
    conexao.close()
    print("Conexão encerrada.")