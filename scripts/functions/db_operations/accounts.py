import json
from classes import Account


def upsert_account(conn, account: Account) -> int:
    """Insert an account or return existing id on (platform, username) conflict."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO accounts (platform, username, account_url, display_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (platform, username)
            DO UPDATE SET
                account_url = COALESCE(EXCLUDED.account_url, accounts.account_url),
                display_name = COALESCE(EXCLUDED.display_name, accounts.display_name)
            RETURNING id
            """,
            (account.platform, account.username, account.account_url, account.display_name),
        )
        conn.commit()
        return cur.fetchone()[0]
