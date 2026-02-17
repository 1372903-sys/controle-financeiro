# 🚀 Guia de Publicação Permanente: Controle Financeiro

Para transformar sua aplicação em um site permanente e acessível de qualquer lugar, siga estes passos simples usando o **Streamlit Community Cloud** (Gratuito).

## 1. Preparação do Código
Certifique-se de que você tem os seguintes arquivos na pasta do seu projeto:
- `app.py` (Arquivo principal)
- `database.py` (Lógica do banco de dados)
- `styles.py` (Design e cores de prosperidade)
- `utils.py` (Utilitários de formatação)
- `requirements.txt` (Lista de dependências)

## 2. Subir para o GitHub
1. Crie uma conta no [GitHub](https://github.com/) (se não tiver).
2. Crie um novo repositório chamado `controle-financeiro`.
3. Faça o upload de todos os arquivos mencionados acima para este repositório.

## 3. Publicar no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io/).
2. Faça login com sua conta do GitHub.
3. Clique em **"New app"**.
4. Selecione o repositório `controle-financeiro`.
5. No campo **"Main file path"**, digite `app.py`.
6. Clique em **"Deploy!"**.

## 4. Benefícios do Site Permanente
- **Acesso Global**: Acesse pelo celular (Android/iOS) ou PC via navegador.
- **Segurança HTTPS**: Conexão criptografada automática.
- **Atualização Automática**: Sempre que você mudar o código no GitHub, o site se atualiza sozinho.
- **Banco de Dados**: O arquivo `finance_control.db` será criado no servidor e manterá seus dados salvos.

---
**Nota sobre Persistência:** No Streamlit Cloud gratuito, o banco de dados SQLite é salvo no disco local do servidor. Se o servidor for reiniciado, os dados podem ser resetados. Para um uso profissional de longo prazo, recomenda-se conectar a um banco de dados externo (como Supabase ou MongoDB), mas para controle pessoal, este método inicial funciona perfeitamente.
