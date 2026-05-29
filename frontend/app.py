import streamlit as st
from api import login, registrar, perfil

st.set_page_config(
    page_title="Portal Acadêmico",
    page_icon="🎓",
    layout="wide"
)

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef8f7, #f7fafc);
}

.topo {
    background: white;
    padding: 22px 35px;
    border-radius: 0 0 22px 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

.logo {
    font-size: 30px;
    font-weight: 800;
    color: #006d77;
}

.hero {
    background: linear-gradient(135deg, #009688, #006d77);
    color: white;
    padding: 50px;
    border-radius: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.hero h1 {
    font-size: 46px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    min-height: 145px;
    border-top: 5px solid #009688;
}

.login-box {
    background: white;
    padding: 38px;
    border-radius: 25px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.12);
}

.badge {
    background: #e0f7f5;
    color: #006d77;
    padding: 8px 14px;
    border-radius: 20px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 15px;
}

.footer-text {
    text-align: center;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topo">
    <div class="logo">🎓 SynCampus</div>
    <p>Portal acadêmico para alunos, professores e administração</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("""
    <div class="hero">
        <div class="badge">Sistema Acadêmico Online</div>
        <h1>Organize sua vida acadêmica em um só lugar</h1>
        <p>
            Acesse notas, disciplinas, matrícula, frequência e informações importantes
            de forma rápida, simples e segura.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h2>📚</h2>
            <h3>Disciplinas</h3>
            <p>Veja suas matérias cadastradas.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h2>📝</h2>
            <h3>Notas</h3>
            <p>Acompanhe seu desempenho.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <h2>👨‍🏫</h2>
            <h3>Professores</h3>
            <p>Consulte turmas e orientações.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:

    st.markdown("""
<style>
.marquee {
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    background: white;
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

.marquee span {
    display: inline-block;
    animation: mover 12s linear infinite;
    font-weight: bold;
    color: #006d77;
    font-size: 18px;
}

@keyframes mover {
    from {
        transform: translateX(100%);
    }
    to {
        transform: translateX(-100%);
    }
}
</style>

<div class="marquee">
    <span>✨ Venha fazer parte da melhor instituição do planeta!!🚀 Matriculas abertas✨ 2026.2</span>
</div>
""", unsafe_allow_html=True)

    if st.session_state.pagina == "login":
        st.markdown("### Entrar no Portal")
        st.caption("Use seu e-mail e senha cadastrados")

        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Acessar Portal", use_container_width=True):
            resposta = login(email, senha)

            if resposta.status_code == 200:
                dados = resposta.json()
                token = dados["access_token"]

                resposta_perfil = perfil(token)

                if resposta_perfil.status_code == 200:
                    usuario = resposta_perfil.json()

                    st.session_state["token"] = token
                    st.session_state["usuario"] = usuario

                    if usuario["role"] == "aluno":
                        st.switch_page("pages/aluno.py")
                    elif usuario["role"] == "professor":
                        st.switch_page("pages/professor.py")
                    elif usuario["role"] == "admin":
                        st.switch_page("pages/admin.py")
                    else:
                        st.error("Tipo de usuário inválido.")
                else:
                    st.error("Erro ao carregar perfil.")
            else:
                st.error("E-mail ou senha inválidos.")

        st.divider()

        st.write("Ainda não tem conta?")

        if st.button("Criar Conta", use_container_width=True):
            st.session_state.pagina = "registro"
            st.rerun()

    else:
        st.markdown("### Criar Conta")
        st.caption("Preencha os dados para se cadastrar")

        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        role = st.selectbox(
            "Tipo de usuário",
            ["aluno", "professor", "admin"]
        )

        if st.button("Registrar", use_container_width=True):
            resposta = registrar(nome, email, senha, role)

            if resposta.status_code == 201:
                st.success("Conta criada com sucesso!")
                st.session_state.pagina = "login"
                st.rerun()
            else:
                try:
                    st.error(resposta.json()["detail"])
                except:
                    st.error("Erro ao registrar usuário.")

        st.divider()

        if st.button("Voltar para Login", use_container_width=True):
            st.session_state.pagina = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown("""
<p class="footer-text">
    Desenvolvido para gestão acadêmica de alunos, professores e administradores.
</p>
""", unsafe_allow_html=True)