-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS eg CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE eg;

-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS `usuario` (
  `cod_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome_usuario` varchar(50) DEFAULT NULL,
  `username_usuario` varchar(50) NOT NULL,
  `email_usuario` varchar(100) NOT NULL UNIQUE,
  `password_usuario` varchar(255) DEFAULT NULL,
  `foto_usuario` varchar(100) DEFAULT NULL,
  `conta_ativa` tinyint(1) NOT NULL DEFAULT 1,
  `criacao_usuario` timestamp NOT NULL DEFAULT current_timestamp(),
  `tipo_usuario` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0 = Usuário Normal, 1 = Administrador',
  PRIMARY KEY (`cod_usuario`),
  UNIQUE KEY `email_usuario` (`email_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dados de teste
INSERT INTO `usuario` (`nome_usuario`, `username_usuario`, `email_usuario`, `password_usuario`, `tipo_usuario`) VALUES
('Fábio Busnardo', 'fabio', 'fabiobusnardo@hotmail.com', 'scrypt:32768:8:1$mKVLdtOEaWxQ8G1h$2d6bea6df53a1bcdcd961b4736cf0d02c8898a8364370fc80e09909acc6bf58ecc203a6db17d1b5efba81ad0ce9ee0df096b55e2a30554e75b200f4062475cb8', 1),
('teste', 'teste', 'teste@teste.com', 'scrypt:32768:8:1$xHdxOaeGgO8m8YC1$c8f5e2644ce14363bc0bb74f35f5339c194c32f27744cf3d22a6c9f61cb32e313d5848970bd426b588e315c9482f52c760c9a659675f4bd420f618212be3cb63', 0);


-- Criar a tabela de países
CREATE TABLE pais (
    cod_pais INT AUTO_INCREMENT PRIMARY KEY,
    nome_pais VARCHAR(100) NOT NULL UNIQUE
);


