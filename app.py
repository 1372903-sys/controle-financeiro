import streamlit as st
from datetime import datetime
import database as db
import utils
import styles
import pandas as pd
import re

# Configuração da Página
st.set_page_config(
    page_title="Controle Financeiro Seguro",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Banco de Dados e Estilos
db.init_db()
styles.apply_styles()

# Função para exibir o cabeçalho sofisticado
def show_sophisticated_header():
    st.markdown('<h1 class="sophisticated-title">Controle Financeiro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sophisticated-subtitle">A Estratégia Inteligente para sua Prosperidade</p>', unsafe_allow_html=True)

# --- Gerenciamento de Sessão ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_id' not in st.session_state: st.session_state['user_id'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'auth_page' not in st.session_state: st.session_state['auth_page'] = 'login'

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# --- TELA DE AUTENTICAÇÃO ---
if not st.session_state['logged_in']:
    show_sophisticated_header()
    
    if st.session_state['auth_page'] == 'login':
        st.subheader("Acesse sua conta")
        with st.form("login_form"):
            email_or_user = st.text_input("E-mail ou Usuário")
            pw = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                user_data = db.login_user(email_or_user, pw)
                if user_data:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'], st.session_state['username'] = user_data
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else: st.error("Dados de acesso incorretos.")
        
        col_l1, col_l2 = st.columns(2)
        if col_l1.button("Criar nova conta"): st.session_state['auth_page'] = 'register'; st.rerun()
        if col_l2.button("Esqueci minha senha"): st.session_state['auth_page'] = 'reset'; st.rerun()

    elif st.session_state['auth_page'] == 'register':
        st.subheader("Cadastre-se")
        with st.form("register_form"):
            new_user = st.text_input("Nome de Usuário")
            new_email = st.text_input("E-mail válido")
            new_pw = st.text_input("Senha", type="password")
            confirm_pw = st.text_input("Confirme a senha", type="password")
            if st.form_submit_button("Cadastrar"):
                if not is_valid_email(new_email): st.error("E-mail inválido.")
                elif new_pw != confirm_pw: st.error("Senhas não coincidem.")
                elif db.create_user(new_user, new_email, new_pw):
                    st.success("Conta criada! Realize o login."); st.session_state['auth_page'] = 'login'; st.rerun()
                else: st.error("Usuário ou e-mail já cadastrado.")
        if st.button("Voltar para Login"): st.session_state['auth_page'] = 'login'; st.rerun()

    elif st.session_state['auth_page'] == 'reset':
        st.subheader("Recuperar Senha")
        if 'reset_step' not in st.session_state: st.session_state['reset_step'] = 1
        
        if st.session_state['reset_step'] == 1:
            email_reset = st.text_input("E-mail cadastrado")
            if st.button("Enviar Código"):
                code = db.generate_reset_code(email_reset)
                if code:
                    st.session_state['reset_email'] = email_reset
                    st.session_state['reset_step'] = 2
                    st.info(f"CÓDIGO DE VERIFICAÇÃO: {code}")
                    st.rerun()
                else: st.error("E-mail não encontrado.")
        
        elif st.session_state['reset_step'] == 2:
            st.write(f"Código enviado para: {st.session_state['reset_email']}")
            input_code = st.text_input("Código de 6 dígitos")
            new_pw_reset = st.text_input("Nova Senha", type="password")
            if st.button("Redefinir Senha"):
                if db.verify_reset_code(st.session_state['reset_email'], input_code):
                    db.reset_password(st.session_state['reset_email'], new_pw_reset)
                    st.success("Senha alterada!"); st.session_state['auth_page'] = 'login'; st.session_state['reset_step'] = 1; st.rerun()
                else: st.error("Código inválido.")
        if st.button("Voltar"): st.session_state['auth_page'] = 'login'; st.session_state['reset_step'] = 1; st.rerun()
    st.stop()

# --- ÁREA LOGADA ---
user_id = st.session_state['user_id']
username = st.session_state['username']

st.sidebar.title(f"👤 {username}")
if st.sidebar.button("Sair"): logout()
st.sidebar.divider()
menu = st.sidebar.radio("Ir para:", ["Mensal", "🎯 Metas Financeiras", "Resumo Anual", "🔮 Projeção 12 Meses"])

# Seleção de Mês e Ano
current_date = datetime.now()
months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
selected_month_name = st.sidebar.selectbox("Mês", months, index=current_date.month - 1)
selected_month = months.index(selected_month_name) + 1
selected_year = st.sidebar.number_input("Ano", min_value=2020, max_value=2030, value=current_date.year)

show_sophisticated_header()

if menu == "Mensal":
    st.subheader(f"📊 {selected_month_name} / {selected_year}")
    in_df = db.get_incomes(user_id, selected_month, selected_year)
    ex_df = db.get_expenses(user_id, selected_month, selected_year)
    inv_df = db.get_investments(user_id, selected_month, selected_year)
    
    t_in = in_df['value'].sum() if not in_df.empty else 0.0
    t_ex = ex_df['value'].sum() if not ex_df.empty else 0.0
    t_inv = inv_df['amount'].sum() if not inv_df.empty else 0.0
    
    c1, col_bal, c3 = st.columns([1, 1.5, 1])
    with col_bal:
        balance = t_in - t_ex
        st.metric("Saldo Líquido Atual", utils.format_currency(balance))
    
    st.divider()
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Receitas", utils.format_currency(t_in))
    col_m2.metric("Despesas", utils.format_currency(t_ex), delta_color="inverse")
    col_m3.metric("Investido", utils.format_currency(t_inv))

    t1, t2, t3 = st.tabs(["📥 Receitas", "📤 Despesas", "📈 Investimentos"])
    with t1:
        with st.form("in_f", clear_on_submit=True):
            s, c = st.columns(2); src = s.text_input("Fonte"); cat = c.selectbox("Categoria", ["Salário", "Freelance", "Dividendos", "Outros"])
            v = st.number_input("Valor", min_value=0.0, step=0.01); r = st.checkbox("Replicar 12 meses")
            if st.form_submit_button("Adicionar Receita"):
                if src and v > 0:
                    db.add_income(user_id, src, v, cat, selected_month, selected_year, 1 if r else 0)
                    st.success("Receita adicionada!"); st.rerun()
        if not in_df.empty:
            df_in_disp = in_df.copy()
            df_in_disp['Valor'] = df_in_disp['value'].apply(utils.format_currency)
            st.dataframe(df_in_disp[['source_name', 'category', 'Valor']].rename(columns={'source_name':'Fonte','category':'Cat'}), use_container_width=True)
            for _, r in in_df.iterrows():
                if st.button(f"🗑️ Excluir {r['source_name']}", key=f"i_{r['id']}"): db.delete_income(r['id'], user_id); st.rerun()

    with t2:
        with st.form("ex_f", clear_on_submit=True):
            d = st.text_input("Descrição"); v_e = st.number_input("Valor", min_value=0.0); ct = st.selectbox("Tipo", ["Fixa", "Ocasional"]); r_e = st.checkbox("Replicar 12 meses", value=(ct=="Fixa"))
            if st.form_submit_button("Adicionar Despesa"):
                if d and v_e > 0:
                    db.add_expense(user_id, d, v_e, ct, selected_month, selected_year, 1 if r_e else 0)
                    st.success("Despesa adicionada!"); st.rerun()
        if not ex_df.empty:
            df_ex_disp = ex_df.copy()
            df_ex_disp['Valor'] = df_ex_disp['value'].apply(utils.format_currency)
            st.dataframe(df_ex_disp[['description', 'category', 'Valor']].rename(columns={'description':'Desc','category':'Tipo'}), use_container_width=True)
            for _, r in ex_df.iterrows():
                if st.button(f"🗑️ Excluir {r['description']}", key=f"e_{r['id']}"): db.delete_expense(r['id'], user_id); st.rerun()

    with t3:
        with st.form("inv_f", clear_on_submit=True):
            v_i = st.number_input("Valor", min_value=0.0); c_i = st.selectbox("Cat", ["Ações", "FIIs", "Renda Fixa", "Reserva", "Outros"]); r_i = st.checkbox("Replicar 12 meses")
            # Adicionar meta vinculada (opcional)
            goals_df = db.get_goals(user_id)
            goal_options = ["Nenhuma"] + goals_df['name'].tolist() if not goals_df.empty else ["Nenhuma"]
            selected_goal_name = st.selectbox("Vincular a uma Meta?", goal_options)
            
            if st.form_submit_button("Adicionar Investimento"):
                if v_i > 0:
                    db.add_investment(user_id, v_i, c_i, selected_month, selected_year, 1 if r_i else 0)
                    if selected_goal_name != "Nenhuma":
                        goal_id = goals_df[goals_df['name'] == selected_goal_name]['id'].iloc[0]
                        db.update_goal_progress(goal_id, user_id, v_i)
                        st.balloons()
                        st.toast(f"🎯 Meta '{selected_goal_name}' atualizada!")
                    st.success("Investimento registrado!"); st.rerun()
        if not inv_df.empty:
            df_inv_disp = inv_df.copy()
            df_inv_disp['Valor'] = df_inv_disp['amount'].apply(utils.format_currency)
            st.dataframe(df_inv_disp[['category', 'Valor']].rename(columns={'category':'Cat'}), use_container_width=True)
            for _, r in inv_df.iterrows():
                if st.button(f"🗑️ Excluir {r['category']}", key=f"v_{r['id']}"): db.delete_investment(r['id'], user_id); st.rerun()

elif menu == "🎯 Metas Financeiras":
    st.subheader("🎯 Suas Metas de Prosperidade")
    
    # Criar nova meta
    with st.expander("➕ Criar Nova Meta"):
        with st.form("goal_f", clear_on_submit=True):
            gn = st.text_input("Nome da Meta (ex: Reserva de Emergência)")
            gt = st.number_input("Valor Alvo (R$)", min_value=0.0, step=100.0)
            gd = st.date_input("Prazo (Opcional)", value=None)
            if st.form_submit_button("Salvar Meta"):
                if gn and gt > 0:
                    db.add_goal(user_id, gn, gt, gd)
                    st.success("Meta criada com sucesso!"); st.rerun()

    # Listar metas existentes
    goals_df = db.get_goals(user_id)
    if not goals_df.empty:
        for _, g in goals_df.iterrows():
            progress = min(g['current_value'] / g['target_value'], 1.0)
            col_g1, col_g2 = st.columns([3, 1])
            with col_g1:
                st.write(f"### {g['name']}")
                st.progress(progress)
                st.write(f"Progresso: **{progress*100:.1f}%** ({utils.format_currency(g['current_value'])} de {utils.format_currency(g['target_value'])})")
                if progress >= 1.0:
                    st.success("🏆 Meta Atingida! Parabéns pela sua disciplina!")
            with col_g2:
                if st.button("🗑️ Excluir", key=f"dg_{g['id']}"):
                    db.delete_goal(g['id'], user_id)
                    st.rerun()
            st.divider()
    else:
        st.info("Você ainda não definiu nenhuma meta. Comece agora a planejar seu futuro!")

elif menu == "Resumo Anual":
    st.subheader(f"📅 Resumo Anual - {selected_year}")
    in_a, ex_a, inv_a = db.get_annual_summary(user_id, selected_year)
    t_in_y = in_a['value'].sum(); t_ex_y = ex_a['value'].sum(); t_inv_y = inv_a['amount'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita Total", utils.format_currency(t_in_y))
    c2.metric("Despesa Total", utils.format_currency(t_ex_y))
    c3.metric("Saldo Líquido", utils.format_currency(t_in_y - t_ex_y))
    c4.metric("Total Investido", utils.format_currency(t_inv_y))
    
    st.divider()
    m_d = []
    for i in range(1, 13):
        m_d.append({
            "Mês": months[i-1], 
            "Receita": in_a[in_a['month']==i]['value'].sum(), 
            "Despesa": ex_a[ex_a['month']==i]['value'].sum(), 
            "Investimento": inv_a[inv_a['month']==i]['amount'].sum()
        })
    df_c = pd.DataFrame(m_d)
    df_c['Mês'] = pd.Categorical(df_c['Mês'], categories=months, ordered=True)
    st.bar_chart(df_c.sort_values('Mês'), x="Mês", y=["Receita", "Despesa", "Investimento"])

elif menu == "🔮 Projeção 12 Meses":
    st.subheader("🔮 Projeção Financeira - 12 Meses")
    df_p = db.get_future_projection(user_id, selected_month, selected_year)
    if not df_p.empty:
        df_p['Mês Nome'] = df_p.apply(lambda x: f"{months[int(x['Mês'])-1]} / {int(x['Ano'])}", axis=1)
        st.line_chart(df_p.set_index("Mês Nome")[["Receita", "Despesa", "Saldo"]])
        st.table(df_p[["Mês Nome", "Receita", "Despesa", "Investimento", "Saldo"]])
