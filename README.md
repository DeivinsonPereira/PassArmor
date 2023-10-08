# PassArmor

Este é um projeto simples de registro e login em Python que utiliza uma base de dados SQLite para armazenar informações de usuários. O sistema foi desenvolvido para permitir que os usuários se registrem com um endereço de e-mail válido e uma senha forte, e posteriormente façam login em suas contas.

## Funcionalidades

### 1. Registro de Usuário
- Os usuários podem se registrar fornecendo um endereço de e-mail válido e uma senha forte.
- A senha forte deve conter pelo menos 8 caracteres, incluindo pelo menos uma letra maiúscula, uma letra minúscula, um dígito e um caractere especial (!@#$%^&*.).
- O sistema verifica se o endereço de e-mail já está em uso e fornece feedback adequado.
### 2. Login de Usuário
- Os usuários podem fazer login usando seu endereço de e-mail e senha.
- O sistema verifica se o usuário está bloqueado devido a múltiplas tentativas de login fracassadas.
- Após um número máximo de tentativas de login falhadas, a conta do usuário é bloqueada por um período de tempo específico.
- Caso o login seja bem-sucedido, as tentativas de login são redefinidas e a conta não está mais bloqueada.
### 3. Segurança
- As senhas dos usuários são armazenadas de forma segura usando o algoritmo de hash SHA-256 com uma técnica de "salt" para aumentar a segurança.
- As informações de bloqueio da conta (contagem de tentativas de login e tempo de bloqueio) são registradas na base de dados.

## Tecnologias Utilizadas
- Python 3.9.13
- SQLite para armazenamento de dados
- Passlib para hash de senhas
- Email Validator para validar endereços de e-mail
- Secrets para gerar "salt" de forma segura
- Expressões regulares (regex) para validar senhas
