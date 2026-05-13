-- usar o seu banco de dados da puc
USE BD24022618;

-- apaga as tabelas se elas já existirem
DROP TABLE IF EXISTS solicitacoes;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;

-- criando a tabela 'usuarios'
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

-- criando a tabela 'categorias'
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- criando a tabela 'solicitacoes'
CREATE TABLE chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,                -- NULL quando o usuário for excluído
    categoria_id INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,

	-- so aceita números de 1 a 5 
    urgencia INT NOT NULL CHECK (urgencia BETWEEN 1 AND 5),
    impacto INT NOT NULL CHECK (impacto BETWEEN 1 AND 5),

    -- cálculo de prioridade com pesos (urgência mais importante que impacto)
    -- urgência = 0.6 (60%)
    -- impacto  = 0.4 (40%)
	-- GENERATED ALWAYS: o banco calcula sozinho
    prioridade DECIMAL(5,2) GENERATED ALWAYS AS (
        (urgencia * 0.6) + (impacto * 0.4)
    ) STORED,

    -- classificação automática baseada na prioridade calculada (0 até 5)
    nivel_prioridade VARCHAR(20) GENERATED ALWAYS AS (
        CASE
            WHEN ((urgencia * 0.6) + (impacto * 0.4)) >= 4.2 THEN 'Crítica'
            WHEN ((urgencia * 0.6) + (impacto * 0.4)) >= 3.2 THEN 'Alta'
            WHEN ((urgencia * 0.6) + (impacto * 0.4)) >= 2.2 THEN 'Média'
            ELSE 'Baixa'
        END
    ) STORED,  -- STORED: salva o valor no banco

	-- toda chamada feita sera automaticamente 'Aberta' ate ser resolvida
    status VARCHAR(20) NOT NULL DEFAULT 'Aberta',
    -- data automatica
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

INSERT INTO categorias (nome) VALUES
('Sistema com falha'),
('Acesso bloqueado'),
('Impressora com erro'),
('Internet sem conexão');