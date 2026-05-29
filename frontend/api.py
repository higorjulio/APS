import requests

BASE_URL = "http://127.0.0.1:8000"


def registrar(name, email, password, role):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }
    )


def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )


def perfil(token):
    return requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )


def listar_alunos(token):
    return requests.get(
        f"{BASE_URL}/alunos",
        headers={"Authorization": f"Bearer {token}"}
    )


def listar_disciplinas(token):
    return requests.get(
        f"{BASE_URL}/disciplinas",
        headers={"Authorization": f"Bearer {token}"}
    )


def listar_matriculas(token):
    return requests.get(
        f"{BASE_URL}/matriculas",
        headers={"Authorization": f"Bearer {token}"}
    )


def listar_notas(token):
    return requests.get(
        f"{BASE_URL}/notas",
        headers={"Authorization": f"Bearer {token}"}
    )


def cadastrar_disciplina(codigo, nome, professor_id, token):
    return requests.post(
        f"{BASE_URL}/disciplinas",
        json={
            "codigo": codigo,
            "nome": nome,
            "professor_id": professor_id if professor_id != 0 else None
        },
        headers={"Authorization": f"Bearer {token}"}
    )


def cadastrar_matricula(aluno_id, disciplina_id, semestre, ano, token):
    return requests.post(
        f"{BASE_URL}/matriculas",
        json={
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "semestre": semestre,
            "ano": ano
        },
        headers={"Authorization": f"Bearer {token}"}
    )


def cadastrar_nota(enrollment_id, atividade, valor, token):
    return requests.post(
        f"{BASE_URL}/notas",
        json={
            "enrollment_id": enrollment_id,
            "atividade": atividade,
            "valor": valor
        },
        headers={"Authorization": f"Bearer {token}"}
    )