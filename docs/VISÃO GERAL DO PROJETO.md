# CriptoManager

## 1. Escopo do Projeto

O **CriptoManager** é um módulo Python para criptografia simétrica que permite:

- **Gerenciar chaves de criptografia**
  - Geração de chaves únicas com Fernet do `cryptography`
  - Armazenamento seguro em arquivo (`key.key`) na raiz do projeto
  - Validação de integridade da chave antes do uso

- **Enviar mensagens criptografadas**
  - Recebe texto plano (string) e retorna a versão criptografada em bytes
  - Pode ser usado para transmitir dados sensíveis entre aplicações Python

- **Receber mensagens criptografadas**
  - Descriptografa os dados recebidos usando a chave previamente gerada
  - Trata erros de chave inválida ou mensagens corrompidas

- **Testes e exemplos**
  - `test_unittest.py` e `test.py` para validar todas as funcionalidades
  - `examples/main.py` como referência de uso do sistema

- **Estrutura modular e reutilizável**
  - Código principal isolado em `/src`
  - Scripts de teste em `/tests`
  - Exemplos em `/examples`
  - Documentação em `/docs`

## 2. Tecnologias de Software

- **Linguagem:** Python 3.x
- **Biblioteca de Criptografia:** `cryptography` (módulo Fernet)
- **Criptografia simétrica com AES 128 em modo CBC**
- **Mensagens autenticadas** (garante integridade e confidencialidade)
- **Ambiente de Desenvolvimento:** PyCharm
- **Controle de Versão:** Git (GitHub)
- Estrutura de projeto organizada para testes, exemplos e documentação

## 3. Lógica de Programação e Fluxo

### Criação e Validação de Chave

- **Função `generate_key(path)`**
  - Gera uma chave Fernet aleatória (`Fernet.generate_key()`)
  - Salva em arquivo binário (`key.key`) na raiz do projeto

- **Função `load_key(path)`**
  - Lê a chave do arquivo
  - Tenta criar um objeto Fernet para validar integridade
  - Lança `InvalidKeyError` se a chave for inválida

### Criptografia de Mensagens

- **Função `encrypt_message(message, key_path)`**
  - Carrega a chave com `load_key()`
  - Criptografa o texto plano usando `Fernet.encrypt()`
  - Retorna a mensagem em bytes

### Descriptografia de Mensagens

- **Função `decrypt_message(encrypted_message, key_path)`**
  - Carrega a chave com `load_key()`
  - Tenta descriptografar usando `Fernet.decrypt()`
  - Captura exceções:
    - `InvalidKeyError` → chave inválida
    - `InvalidToken` → mensagem corrompida ou não corresponde à chave

### Testes Automatizados

- `unittest` garante que:
  - Mensagem criptografada → descriptografada corretamente
  - Mensagem corrompida → detectada como inválida
  - Chave corrompida → detectada e restaurada
  - Mensagem antiga não pode ser descriptografada com nova chave

## 4. Características Técnicas

- **Segurança**
  - Confidencialidade via criptografia simétrica
  - Validação de integridade via Fernet

- **Portabilidade**
  - Estrutura modular (`/src`) permite fácil importação em outros projetos Python

- **Manutenibilidade**
  - Pastas `/tests`, `/examples`, `/docs` para organizar desenvolvimento, testes e documentação

- **Erros tratados**
  - Chave inválida, arquivo ausente, mensagem corrompida