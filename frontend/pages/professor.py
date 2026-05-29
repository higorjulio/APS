import streamlit as st
from api import (
    perfil,
    listar_disciplinas,
    listar_matriculas,
    listar_notas,
    listar_alunos,
    cadastrar_nota
)

st.set_page_config(
    page_title="Portal do Professor",
    page_icon="👨‍🏫",
    layout="wide"
)

token = st.session_state.get("token")

if not token:
    st.error("Você precisa fazer login primeiro.")
    st.stop()

resposta_usuario = perfil(token)

if resposta_usuario.status_code != 200:
    st.error("Erro ao carregar dados do professor.")
    st.stop()

usuario = resposta_usuario.json()

if usuario.get("role") != "professor":
    st.error("Acesso permitido apenas para professores.")
    st.stop()

resposta_disciplinas = listar_disciplinas(token)
resposta_matriculas = listar_matriculas(token)
resposta_notas = listar_notas(token)
resposta_alunos = listar_alunos(token)

disciplinas = resposta_disciplinas.json() if resposta_disciplinas.status_code == 200 else []
matriculas = resposta_matriculas.json() if resposta_matriculas.status_code == 200 else []
notas = resposta_notas.json() if resposta_notas.status_code == 200 else []
alunos = resposta_alunos.json() if resposta_alunos.status_code == 200 else []

st.title("👨‍🏫 Portal do Professor")
st.caption(f"Professor: {usuario.get('name', 'Não informado')}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Disciplinas", len(disciplinas))

with col2:
    st.metric("Matrículas", len(matriculas))

with col3:
    st.metric("Alunos", len(alunos))

with col4:
    st.metric("Notas lançadas", len(notas))

st.divider()

with st.container(border=True):
    st.subheader("👤 Dados do professor")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Nome:**")
        st.write(usuario.get("name", "Não informado"))

    with col2:
        st.write("**E-mail:**")
        st.write(usuario.get("email", "Não informado"))

st.write("")

aba1, aba2, aba3, aba4 = st.tabs([
    "📚 Disciplinas",
    "👥 Alunos",
    "📝 Matrículas",
    "⭐ Notas"
])

with aba1:
    st.subheader("Disciplinas")

    if resposta_disciplinas.status_code != 200:
        st.error("Erro ao carregar disciplinas.")
    elif disciplinas:
        for disciplina in disciplinas:
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write("**ID**")
                    st.write(disciplina.get("id", "-"))

                with col2:
                    st.write("**Código**")
                    st.write(disciplina.get("codigo", "-"))

                with col3:
                    st.write("**Nome**")
                    st.write(disciplina.get("nome", "-"))
    else:
        st.info("Nenhuma disciplina encontrada.")

with aba2:
    st.subheader("Alunos cadastrados")

    if resposta_alunos.status_code != 200:
        st.error("Erro ao carregar alunos.")
    elif alunos:
        for aluno in alunos:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**ID**")
                    st.write(aluno.get("id", "-"))

                with col2:
                    st.write("**Nome**")
                    st.write(aluno.get("name", aluno.get("nome", "-")))

                with col3:
                    st.write("**E-mail**")
                    st.write(aluno.get("email", "-"))

                with col4:
                    st.write("**Perfil**")
                    st.write(aluno.get("role", "-"))
    else:
        st.info("Nenhum aluno encontrado.")

with aba3:
    st.subheader("Matrículas")

    if resposta_matriculas.status_code != 200:
        st.error("Erro ao carregar matrículas.")
    elif matriculas:
        for matricula in matriculas:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**ID da matrícula**")
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

with aba4:
    st.subheader("Lançar nota")

    with st.form("form_lancar_nota"):
        enrollment_id = st.number_input(
            "ID da matrícula",
            min_value=1,
            step=1
        )

        atividade = st.text_input(
            "Atividade",
            value="Nota Final"
        )

        valor = st.number_input(
            "Nota",
            min_value=0.0,
            max_value=10.0,
            step=0.1
        )

        enviar = st.form_submit_button(
            "Lançar nota",
            use_container_width=True
        )

        if enviar:
            resposta = cadastrar_nota(
                enrollment_id,
                atividade,
                valor,
                token
            )

            if resposta.status_code in [200, 201]:
                st.success("Nota lançada com sucesso!")
                st.rerun()
            else:
                try:
                    st.error(resposta.json().get("detail", "Erro ao lançar nota."))
                except:
                    st.error("Erro ao lançar nota.")

    st.divider()

    st.subheader("Notas lançadas")

    if resposta_notas.status_code != 200:
        st.error("Erro ao carregar notas.")
    elif notas:
        for nota in notas:
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write("**ID**")
                    st.write(nota.get("id", "-"))

                with col2:
                    st.write("**Atividade**")
                    st.write(nota.get("atividade", "-"))

                with col3:
                    st.write("**Nota**")
                    st.write(nota.get("valor", "-"))
    else:
        st.info("Nenhuma nota encontrada.")

st.divider()

if st.button("Sair", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")