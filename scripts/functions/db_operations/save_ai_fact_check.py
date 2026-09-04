def save_ai_fact_check(conn, post_id: int, provider: str, result: dict) -> int:
    """Upsert an AI fact-check suggestion for a post and replace its sources. Returns the fact-check id."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ai_fact_checks (post_id, provider, likely_disinformation, reasoning)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (post_id, provider) DO UPDATE SET
                likely_disinformation = EXCLUDED.likely_disinformation,
                reasoning = EXCLUDED.reasoning,
                checked_at = NOW()
            RETURNING id
            """,
            (post_id, provider, result["likely_disinformation"], result["reasoning"]),
        )
        fact_check_id = cur.fetchone()[0]

        cur.execute(
            "DELETE FROM ai_fact_check_sources WHERE ai_fact_check_id = %s",
            (fact_check_id,),
        )
        for source in result.get("sources", []):
            cur.execute(
                """
                INSERT INTO ai_fact_check_sources (ai_fact_check_id, title, link)
                VALUES (%s, %s, %s)
                """,
                (fact_check_id, source["title"], source["link"]),
            )

        conn.commit()
        return fact_check_id
