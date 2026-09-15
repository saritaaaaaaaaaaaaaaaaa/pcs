from app.database import get_connection


RECIPE_FIELDS = """
    receitas.id,
    receitas.titulo,
    receitas.descricao,
    receitas.imagem,
    receitas.tempo_preparo,
    receitas.dificuldade,
    receitas.criado_em,
    categorias.nome AS categoria_nome
"""


def _fetch_all(query: str, params: tuple = ()):
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def get_categories():
    return _fetch_all("SELECT id, nome FROM categorias ORDER BY nome COLLATE NOCASE")


def get_difficulties():
    return _fetch_all(
        """
        SELECT DISTINCT dificuldade
        FROM receitas
        WHERE dificuldade IS NOT NULL AND TRIM(dificuldade) <> ''
        ORDER BY dificuldade COLLATE NOCASE
        """
    )


def get_recipes_by_filters(titulo: str, categoria_id: int | None, dificuldade: str):
    clauses = []
    params = []

    if titulo.strip():
        clauses.append("receitas.titulo LIKE ?")
        params.append(f"%{titulo.strip()}%")
    if categoria_id is not None:
        clauses.append("receitas.categoria_id = ?")
        params.append(categoria_id)
    if dificuldade.strip():
        clauses.append("LOWER(receitas.dificuldade) = LOWER(?)")
        params.append(dificuldade.strip())

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return _fetch_all(
        f"""
        SELECT {RECIPE_FIELDS}
        FROM receitas
        LEFT JOIN categorias ON receitas.categoria_id = categorias.id
        {where}
        ORDER BY receitas.criado_em DESC
        """,
        tuple(params),
    )


def get_latest_recipes():
    return _fetch_all(
        f"""
        SELECT {RECIPE_FIELDS}
        FROM receitas
        LEFT JOIN categorias ON receitas.categoria_id = categorias.id
        ORDER BY receitas.criado_em DESC
        """
    )


def get_top_rated_recipes():
    return _fetch_all(
        f"""
        SELECT {RECIPE_FIELDS}, AVG(avaliacoes.nota) AS media_avaliacoes,
               COUNT(avaliacoes.id) AS total_avaliacoes
        FROM receitas
        LEFT JOIN categorias ON receitas.categoria_id = categorias.id
        INNER JOIN avaliacoes ON avaliacoes.receita_id = receitas.id
        GROUP BY receitas.id, receitas.titulo, receitas.descricao, receitas.imagem,
                 receitas.tempo_preparo, receitas.dificuldade, receitas.criado_em,
                 categorias.nome
        ORDER BY media_avaliacoes DESC, total_avaliacoes DESC, receitas.criado_em DESC
        """
    )
