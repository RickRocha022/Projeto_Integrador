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

    if not valor.replace(" ", "").isalpha():
        print("Este campo aceita apenas letras.")
        return None

    return valor

"""
*strip() --> remove espaços em branco no começo e no final.
*replace(" ", "") --> remove os espaços antes de validar, para que
nomes com espaço (ex: "João Silva") não sejam rejeitados.
*isalpha() --> retorna True apenas se todos os caracteres forem letras.
Se houver número, símbolo ou caractere especial, retorna False.
"""

def ler_email(prompt):
    valor = input(prompt).strip()
    if not valor:
        print("Campo obrigatório! Não pode ficar em branco.")
        return None

    if "@" not in valor:
        print("E-mail inválido!.")
        return None

    return valor

"""
*"@" not in valor --> verifica se o caractere @ está presente na string.
Se não estiver, o e-mail é considerado inválido.
*Separada de ler_texto pois e-mail possui caracteres especiais
(@, ., -) que seriam barrados pela validação isalpha().
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
*(prompt, minimo=None, maximo=None) --> lê um número inteiro e
pode limitar valores mínimos e máximos.
*Faz o inverso do ler_texto: tenta converter para inteiro.
Se conseguir, verifica se está dentro dos limites.
"""

# ─── USUÁRIOS ──────────────────────────────────────────────

def cadastrar_usuario():
    try:
        nome = ler_texto("\nNome: ")
        if nome is None:
            return

        email = ler_email("Email: ")
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
*isdigit() --> garante que só tenha números de 0 a 9.
"""

def listar_usuarios():
    try:
        cursor.execute("SELECT id, nome, email, telefone FROM usuarios")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return

        print("\n" + "─" * 40)
        for u in usuarios:
            print(f"  ID       : {u[0]}")
            print(f"  Nome     : {u[1]}")
            print(f"  Email    : {u[2]}")
            print(f"  Telefone : {u[3] or '-'}")
            print("─" * 40)

    except Exception as e:
        print(f"Erro ao listar usuários: {e}")

"""
*fetchall() --> pega todos os registros retornados pela última consulta.
*u[3] or '-' --> se o telefone for vazio, mostra um traço no lugar.
"""

def buscar_por_usuario():
    try:
        termo = input("\nDigite o ID, nome ou e-mail do usuário: ").strip()
        if not termo:
            print("Campo obrigatório! Não pode ficar em branco.")
            return

        if termo.isdigit():
            cursor.execute(
                "SELECT id, nome, email, telefone FROM usuarios WHERE id = %s",
                (int(termo),)
            )
        else:
            like = f"%{termo}%"
            cursor.execute(
                "SELECT id, nome, email, telefone FROM usuarios WHERE nome LIKE %s OR email LIKE %s",
                (like, like)
            )

        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNenhum usuário encontrado.")
            return

        print(f"\n  {len(usuarios)} usuário(s) encontrado(s):")
        print("─" * 40)
        for u in usuarios:
            print(f"  ID       : {u[0]}")
            print(f"  Nome     : {u[1]}")
            print(f"  Email    : {u[2]}")
            print(f"  Telefone : {u[3] or '-'}")
            print("─" * 40)

    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")

"""
*isdigit() --> verifica se o termo digitado é um número inteiro.
Se sim, busca pelo ID exato. Se não, busca por nome ou email.
*LIKE %termo% --> encontra registros que contenham o termo
em qualquer posição do campo nome ou email.
*u[3] or '-' --> se o telefone for vazio ou None, exibe um traço.
*fetchall() --> retorna todos os registros encontrados pela consulta.
"""

def excluir_usuario():
    try:
        cursor.execute("SELECT id, nome, email FROM usuarios")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return

        print("\nUsuários cadastrados:")
        print("─" * 40)
        for u in usuarios:
            print(f"  ID    : {u[0]}")
            print(f"  Nome  : {u[1]}")
            print(f"  Email : {u[2]}")
            print("─" * 40)

        usuario_id = ler_inteiro("\nDigite o ID do usuário a excluir: ", minimo=1)
        if usuario_id is None:
            return

        cursor.execute("SELECT nome FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            print("Usuário não encontrado.")
            return

        # Verifica se o usuário possui chamados vinculados
        cursor.execute("SELECT COUNT(*) FROM chamados WHERE usuario_id = %s", (usuario_id,))
        total_chamados = cursor.fetchone()[0]

        print(f"\nUsuário selecionado: {usuario[0]}")

        if total_chamados > 0:
            print(f"\nAtenção: este usuário possui {total_chamados} chamado(s) vinculado(s).")
            print("Os chamados serão mantidos, mas ficarão sem usuário associado.")

        confirmacao = input("\nTem certeza que deseja excluir? (s/n): ").strip().lower()
        if confirmacao != "s":
            print("Exclusão cancelada. Digite apenas valores válidos!")
            return

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conexao.commit()
        print(f"Usuário '{usuario[0]}' excluído com sucesso!")

        if total_chamados > 0:
            print(f"{total_chamados} chamado(s) mantido(s) sem usuário associado.")

    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")

"""
*COUNT(*) FROM chamados WHERE usuario_id --> verifica quantos chamados
estão vinculados ao usuário antes de excluí-lo.
*ON DELETE SET NULL (configurado no SQL) --> ao excluir o usuário, o banco
automaticamente define usuario_id como NULL nos chamados vinculados,
mantendo o histórico dos chamados sem apagá-los.
*Os chamados ficam preservados e podem ser consultados normalmente,
aparecendo sem usuário associado nas listagens.
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

        print("\nChamado registrado com sucesso!")
        print(f"   ID           : {sol[0]}")
        print(f"   Prioridade   : {sol[1]}")
        print(f"   Nível        : {sol[2]}")
        print(f"   Status       : {sol[3]}")

    except Exception as e:
        print(f"Erro ao abrir chamado: {e}")

"""
*print(f"  {u[0]} - {u[1]}") --> tupla onde u[0] é o id e u[1] é o nome.
*minimo=1 evita que o usuário informe id negativo ou zero.
*LAST_INSERT_ID() --> retorna o ID do último registro inserido na tabela.
"""

def listar_chamados():
    try:
        cursor.execute("""
            SELECT s.id, COALESCE(u.nome, 'Usuário excluído'), c.nome, s.descricao,
                   s.urgencia, s.impacto, s.prioridade,
                   s.nivel_prioridade, s.status, s.data_abertura
            FROM chamados s
            LEFT JOIN usuarios   u ON s.usuario_id   = u.id
            JOIN      categorias c ON s.categoria_id = c.id
            ORDER BY s.prioridade DESC
        """)
        chamados = cursor.fetchall()

        if not chamados:
            print("\nNenhum chamado cadastrado.")
            return

        print("\n" + "─" * 40)
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
            print("─" * 40)

    except Exception as e:
        print(f"Erro ao listar chamados: {e}")

"""
*JOIN junta as tabelas chamados, usuarios e categorias para exibir informações completas.
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
            SELECT s.id, COALESCE(u.nome, 'Usuário excluído'), c.nome, s.descricao,
                   s.urgencia, s.impacto, s.prioridade,
                   s.nivel_prioridade, s.status, s.data_abertura
            FROM chamados s
            LEFT JOIN usuarios   u ON s.usuario_id   = u.id
            JOIN      categorias c ON s.categoria_id = c.id
            WHERE s.nivel_prioridade = %s
            ORDER BY s.prioridade DESC
        """, (nivel_escolhido,))

        chamados = cursor.fetchall()

        if not chamados:
            print(f"\nNenhum chamado encontrado com prioridade '{nivel_escolhido}'.")
            return

        print(f"\n  Chamados com prioridade: {nivel_escolhido}  ({len(chamados)} encontrado(s))")
        print("─" * 40)
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
            print("─" * 40)

    except Exception as e:
        print(f"Erro ao buscar por prioridade: {e}")


def buscar_por_status():
    try:
        status_map = {"1": "Aberto", "2": "Em andamento", "3": "Resolvido"}

        print("\nFiltrar por status:")
        print("  1 - Aberto")
        print("  2 - Em andamento")
        print("  3 - Resolvido")

        opcao = input("Escolha: ").strip()

        if opcao not in status_map:
            print("Opção inválida!")
            return

        status_escolhido = status_map[opcao]

        cursor.execute("""
            SELECT s.id, COALESCE(u.nome, 'Usuário excluído'), c.nome, s.descricao,
                   s.urgencia, s.impacto, s.prioridade,
                   s.nivel_prioridade, s.status, s.data_abertura
            FROM chamados s
            LEFT JOIN usuarios   u ON s.usuario_id   = u.id
            JOIN      categorias c ON s.categoria_id = c.id
            WHERE s.status = %s
            ORDER BY s.prioridade DESC
        """, (status_escolhido,))

        chamados = cursor.fetchall()

        if not chamados:
            print(f"\nNenhum chamado encontrado com status '{status_escolhido}'.")
            return

        print(f"\n  Chamados com status: {status_escolhido}  ({len(chamados)} encontrado(s))")
        print("─" * 40)
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
            print("─" * 40)

    except Exception as e:
        print(f"Erro ao buscar por status: {e}")

"""
*Segue o mesmo padrão de buscar_por_prioridade(), trocando o filtro
de nivel_prioridade por status e adaptando o menu de opções.
*WHERE s.status = %s --> filtra apenas os chamados com o status escolhido.
*ORDER BY s.prioridade DESC --> mesmo critério de ordenação das outras buscas.
*status_map usa as mesmas opções de texto já definidas em atualizar_status(),
garantindo consistência nos valores armazenados no banco.
"""

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
*rowcount --> retorna o número de linhas afetadas por uma operação SQL.
Se for 0, o ID do chamado não foi encontrado.
Se for 1, a atualização foi bem-sucedida.
"""

def excluir_chamado():
    try:
        cursor.execute("""
            SELECT s.id, COALESCE(u.nome, 'Usuário excluído'), s.descricao, s.status
            FROM chamados s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            ORDER BY s.id
        """)
        chamados = cursor.fetchall()

        if not chamados:
            print("\nNenhum chamado cadastrado.")
            return

        print("\nChamados cadastrados:")
        print("─" * 40)
        for c in chamados:
            print(f"  ID        : {c[0]}")
            print(f"  Usuário   : {c[1]}")
            print(f"  Descrição : {c[2]}")
            print(f"  Status    : {c[3]}")
            print("─" * 40)

        chamado_id = ler_inteiro("\nDigite o ID do chamado a excluir: ", minimo=1)
        if chamado_id is None:
            return

        cursor.execute("SELECT descricao FROM chamados WHERE id = %s", (chamado_id,))
        chamado = cursor.fetchone()

        if not chamado:
            print("Chamado não encontrado.")
            return

        print(f"\nChamado selecionado: {chamado[0]}")
        confirmacao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
        if confirmacao != "s":
            print("Exclusão cancelada.")
            return

        cursor.execute("DELETE FROM chamados WHERE id = %s", (chamado_id,))
        conexao.commit()
        print("Chamado excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir chamado: {e}")

"""
*JOIN com usuarios --> exibe o nome do usuário dono do chamado na listagem,
facilitando a identificação antes da exclusão.
*fetchone() --> confirma se o ID informado realmente existe antes de deletar.
*confirmacao != "s" --> exige confirmação explícita antes de deletar,
evitando exclusões acidentais.
*DELETE FROM ... WHERE id = %s --> exclui apenas o chamado com o ID informado.
"""

# ─── ESTATÍSTICAS ───────────────────────────────────────────

def estatisticas():
    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM chamados")
        total_chamados = cursor.fetchone()[0]

        cursor.execute("SELECT status, COUNT(*) FROM chamados GROUP BY status")
        por_status = cursor.fetchall()

        cursor.execute("SELECT nivel_prioridade, COUNT(*) FROM chamados GROUP BY nivel_prioridade")
        por_prioridade = cursor.fetchall()

        cursor.execute("""
            SELECT c.nome, COUNT(*) AS total
            FROM chamados s
            JOIN categorias c ON s.categoria_id = c.id
            GROUP BY c.nome
            ORDER BY total DESC
            LIMIT 1
        """)
        top_categoria = cursor.fetchone()

        print("\n" + "═" * 40)
        print("         ESTATÍSTICAS DO SISTEMA")
        print("═" * 40)
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

        print("═" * 40)

    except Exception as e:
        print(f"Erro ao carregar estatísticas: {e}")

"""
*{s[0]:<15}: {s[1]} --> formata a string alinhada à esquerda em 15 caracteres,
seguido do número de chamados, criando uma exibição organizada.
"""

# ─── MENU ──────────────────────────────────────────────────

def menu_principal():
    largura = 38  # largura interna do menu (entre as bordas)

    def linha(texto=""):
        return f"  ║{texto.ljust(largura)}║"

    def titulo(texto):
        return f"  ║{texto.center(largura)}║"

    while True:
        print("\n  ╔" + "═" * largura + "╗")
        print(titulo("SISTEMA DE T.I. — MENU"))
        print("  ╠" + "═" * largura + "╣")

        print(titulo("USUÁRIOS"))
        print(linha("  1  ›  Cadastrar usuário"))
        print(linha("  2  ›  Listar usuários"))
        print(linha("  3  ›  Buscar usuário"))
        print(linha("  4  ›  Excluir usuário"))

        print("  ╠" + "═" * largura + "╣")

        print(titulo("CHAMADOS"))
        print(linha("  5  ›  Abrir chamado"))
        print(linha("  6  ›  Listar chamados"))
        print(linha("  7  ›  Buscar por prioridade"))
        print(linha("  8  ›  Buscar por status"))
        print(linha("  9  ›  Atualizar status"))
        print(linha(" 10  ›  Excluir chamado"))

        print("  ╠" + "═" * largura + "╣")

        print(titulo("SISTEMA"))
        print(linha(" 11  ›  Estatísticas"))
        print(linha("  0  ›  Sair"))

        print("  ╚" + "═" * largura + "╝")
        


        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            buscar_por_usuario()
        elif opcao == "4":
            excluir_usuario()
        elif opcao == "5":
            abrir_chamado()
        elif opcao == "6":
            listar_chamados()
        elif opcao == "7":
            buscar_por_prioridade()
        elif opcao == "8":
            buscar_por_status()
        elif opcao == "9":
            atualizar_status()
        elif opcao == "10":
            excluir_chamado()
        elif opcao == "11":
            estatisticas()
        elif opcao == "0":
            print("\nEncerrando sistema...")
            break
        else:
            print("Opção inválida!")
            continue

        input("\n  Pressione ENTER para voltar ao menu...")

menu_principal()

if conexao.is_connected():
    cursor.close()
    conexao.close()
    print("Conexão encerrada.")