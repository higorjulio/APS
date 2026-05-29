import streamlit as st
from api import perfil, listar_disciplinas, listar_matriculas, listar_notas

st.set_page_config(
    page_title="Portal do Aluno",
    page_icon="🎓",
    layout="wide"
)

token = st.session_state.get("token")

if not token:
    st.error("Você precisa fazer login primeiro.")
    st.stop()

resposta_usuario = perfil(token)

if resposta_usuario.status_code != 200:
    st.error("Erro ao carregar dados do aluno.")
    st.stop()

usuario = resposta_usuario.json()

resposta_disciplinas = listar_disciplinas(token)
resposta_matriculas = listar_matriculas(token)
resposta_notas = listar_notas(token)

disciplinas = resposta_disciplinas.json() if resposta_disciplinas.status_code == 200 else []
matriculas = resposta_matriculas.json() if resposta_matriculas.status_code == 200 else []
notas = resposta_notas.json() if resposta_notas.status_code == 200 else []

st.title("🎓 Portal do Aluno")
st.caption("Área acadêmica do estudante")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Disciplinas", len(disciplinas))

with col2:
    st.metric("Matrículas", len(matriculas))

with col3:
    if notas:
        media = sum(float(n.get("valor", 0)) for n in notas) / len(notas)
        st.metric("Média", f"{media:.1f}")
    else:
        st.metric("Média", "-")

st.divider()

with st.container(border=True):
    st.subheader("👤 Dados do aluno")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Nome:**")
        st.write(usuario.get("name", "Não informado"))

    with col2:
        st.write("**E-mail:**")
        st.write(usuario.get("email", "Não informado"))

st.write("")

aba1, aba2, aba3 = st.tabs(["📚 Disciplinas", "📝 Matrículas", "⭐ Notas"])

with aba1:
    st.subheader("Disciplinas cadastradas")

    if resposta_disciplinas.status_code != 200:
        st.error("Erro ao carregar disciplinas.")
    elif disciplinas:
        for disciplina in disciplinas:
            with st.container(border=True):
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.write("**Código**")
                    st.write(disciplina.get("codigo", "-"))

                with col2:
                    st.write("**Disciplina**")
                    st.write(disciplina.get("nome", "-"))
    else:
        st.info("Nenhuma disciplina encontrada.")

with aba2:
    st.subheader("Matrículas do aluno")

    if resposta_matriculas.status_code != 200:
        st.error("Erro ao carregar matrículas.")
    elif matriculas:
        for matricula in matriculas:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**ID**")
                    st.write(matricula.get("id", "-"))

                with col2:
                    st.write("**Aluno ID**")
                    st.write(matricula.get("aluno_id", "-"))

                with col3:
                    st.write("**Disciplina ID**")
                    st.write(matricula.get("disciplina_id", "-"))

                with col4:
                    st.write("**Status**")
                    st.write(matricula.get("status", "-"))
    else:
        st.info("Nenhuma matrícula encontrada.")

with aba3:
    st.subheader("Notas do aluno")

    if resposta_notas.status_code != 200:
        st.error("Erro ao carregar notas.")
    elif notas:
        for nota in notas:
            valor = nota.get("valor", "-")

            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write("**Atividade**")
                    st.write(nota.get("atividade", "-"))

                with col2:
                    st.write("**Nota**")
                    st.write(valor)
    else:
        st.info("Nenhuma nota encontrada.")

st.divider()

if st.button("Sair", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")