# 💰 Controle Financeiro - Streamlit & SQLite

Esta é uma aplicação de controle financeiro multiplataforma projetada para ser simples, moderna e eficiente.

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.8 ou superior instalado.

### Passo a Passo
1. **Clone ou baixe** os arquivos do projeto.
2. **Instale as dependências**:
   ```bash
   pip install streamlit pandas
   ```
3. **Execute a aplicação**:
   ```bash
   streamlit run app.py
   ```
4. A aplicação abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 📱 Acesso no Android/Mobile
Para usar no Android como um app:
1. **Rede Local**: Se o seu PC e celular estiverem no mesmo Wi-Fi, acesse o endereço IP do seu PC seguido da porta 8501 (ex: `192.168.1.5:8501`).
2. **PWA**: No Chrome do Android, clique nos três pontos e selecione "Adicionar à tela de inicialização". Ele se comportará como um aplicativo nativo.

## ☁️ Como Hospedar Gratuitamente

### 1. Streamlit Community Cloud (Recomendado)
1. Suba o código para um repositório no **GitHub**.
2. Acesse [share.streamlit.io](https://share.streamlit.io).
3. Conecte sua conta do GitHub e selecione o repositório.
4. O Streamlit fará o deploy automático e fornecerá um link público.

*Nota: Como usamos SQLite, os dados são salvos em um arquivo local. No Streamlit Cloud, se o servidor reiniciar, o arquivo SQLite pode ser resetado. Para persistência permanente na nuvem, recomenda-se conectar a um banco externo (como PostgreSQL) ou usar o `Streamlit Secrets` para gerenciar conexões.*

## ✨ Funcionalidades
- **Registro de Receitas**: Nome da fonte e valor.
- **Registro de Despesas**: Categorização entre Fixas e Ocasionais.
- **Investimentos**: Acompanhamento mensal de aportes.
- **Navegação Histórica**: Visualize qualquer mês/ano anterior.
- **Dashboard Anual**: Resumo agregado dos 12 meses do ano selecionado.
- **Design Moderno**: Suporte nativo a Light/Dark mode e interface responsiva.
