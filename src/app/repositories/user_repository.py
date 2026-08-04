from app.database import get_connection


def create_user(user):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (
            nome,
            email,
            senha_hash,
            data_nascimento,
            telefone,
            nivel,
            ativo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        user.nome,
        user.email,
        user.senha_hash,
        user.data_nascimento,
        user.telefone,
        user.nivel,
        1
    ))

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return user_id


def get_user_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user