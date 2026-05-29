import streamlit as st
from api import (
    perfil,
    listar_alunos,
    listar_disciplinas,
    listar_matriculas,
    listar_notas,
    cadastrar_disciplina,
    cadastrar_matricula,
    cadastrar_nota
)

st.set_page_config(
    page_title="Painel Admin",
    page_icon="🛡️",
    layout="wide"
)

token = st.session_state.get("token")

if not token:
    st.error("Você precisa fazer login primeiro.")
    st.stop()

resposta_usuario = perfil(token)

if resposta_usuario.status_code != 200:
    st.error("Erro ao carregar usuário.")
    st.stop()

usuario = resposta_usuario.json()

if usuario.get("role") != "admin":
    st.error("Acesso permitido apenas para administradores.")
    st.stop()

resposta_alunos = listar_alunos(token)
resposta_disciplinas = listar_disciplinas(token)
resposta_matriculas = listar_matriculas(token)
resposta_notas = listar_notas(token)

alunos = resposta_alunos.json() if resposta_alunos.status_code == 200 else []
disciplinas = resposta_disciplinas.json() if resposta_disciplinas.status_code == 200 else []
matriculas = resposta_matriculas.json() if resposta_matriculas.status_code == 200 else []
notas = resposta_notas.json() if resposta_notas.status_code == 200 else []

st.title("🛡️ Painel Administrativo")
st.caption(f"Administrador: {usuario.get('name', 'Admin')}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Alunos", len(alunos))

with col2:
    st.metric("Disciplinas", len(disciplinas))

with col3:
    st.metric("Matrículas", len(matriculas))

with col4:
    st.metric("Notas", len(notas))

st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "👥 Alunos",
    "📚 Disciplinas",
    "📝 Matrículas",
    "⭐ Notas"
])

with aba1:
    st.subheader("Alunos cadastrados")

    if resposta_alunos.status_code != 200:
        st.error("Erro ao carregar alunos.")
    elif alunos:
        for aluno in alunos:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**ID**")
                    st.write(str(aluno.get("id", "-")))

                with col2:
                    st.write("**Nome**")
                    st.write(str(aluno.get("name", "-")))

                with col3:
                    st.write("**E-mail**")
                    st.write(str(aluno.get("email", "-")))

                with col4:
                    st.write("**Role**")
                    st.write(str(aluno.get("role", "-")))
    else:
        st.info("Nenhum aluno encontrado.")

with aba2:
    st.subheader("Disciplinas")

    with st.expander("Cadastrar nova disciplina"):
        codigo = st.text_input("Código da disciplina")
        nome = st.text_input("Nome da disciplina")
        professor_id = st.number_input("ID do professor", min_value=0, step=1)

        if st.button("Cadastrar disciplina", use_container_width=True):
            if not codigo or not nome:
                st.error("Preencha código e nome.")
            else:
                resposta = cadastrar_disciplina(codigo, nome, professor_id, token)

                if resposta.status_code in [200, 201]:
                    st.success("Disciplina cadastrada com sucesso!")
                    st.rerun()
                else:
                    try:
                        st.error(resposta.json().get("detail", "Erro ao cadastrar disciplina."))
                    except:
                        st.error("Erro ao cadastrar disciplina.")

    st.divider()

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

with aba3:
    st.subheader("Matrículas")

    with st.expander("Cadastrar nova matrícula"):
        aluno_id = st.number_input("ID do aluno", min_value=1, step=1)
        disciplina_id = st.number_input("ID da disciplina", min_value=1, step=1)
        semestre = st.number_input("Semestre", min_value=1, step=1)
        ano = st.number_input("Ano", min_value=2024, step=1)

        if st.button("Cadastrar matrícula", use_container_width=True):
            resposta = cadastrar_matricula(
                aluno_id,
                disciplina_id,
                semestre,
                ano,
                token
            )

            if resposta.status_code in [200, 201]:
                st.success("Matrícula cadastrada com sucesso!")
                st.rerun()
            else:
                try:
                    st.error(resposta.json().get("detail", "Erro ao cadastrar matrícula."))
                except:
                    st.error("Erro ao cadastrar matrícula.")

    st.divider()

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

with aba4:
    st.subheader("Notas")

    with st.expander("Cadastrar nova nota"):
        enrollment_id = st.number_input("ID da matrícula", min_value=1, step=1)
        atividade = st.text_input("Atividade", value="Nota Final")
        valor = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Cadastrar nota", use_container_width=True):
            if not atividade:
                st.error("Preencha a atividade.")
            else:
                resposta = cadastrar_nota(
                    enrollment_id,
                    atividade,
                    valor,
                    token
                )

                if resposta.status_code in [200, 201]:
                    st.success("Nota cadastrada com sucesso!")
                    st.rerun()
                else:
                    try:
                        st.error(resposta.json().get("detail", "Erro ao cadastrar nota."))
                    except:
                        st.error("Erro ao cadastrar nota.")

    st.divider()

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
                    st.write("**Valor**")
                    st.write(nota.get("valor", "-"))
    else:
        st.info("Nenhuma nota encontrada.")

st.divider()

if st.button("Sair", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")