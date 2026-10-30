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


def get_watched_accounts(conn, platform: str) -> list[dict]:
    """Accounts on the platform that are on the scrape list, as {name, url} dicts."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COALESCE(display_name, username), account_url
            FROM accounts
            WHERE platform = %s AND is_watched AND account_url IS NOT NULL
            ORDER BY id
            """,
            (platform,),
        )
        return [{"name": name, "url": url} for name, url in cur.fetchall()]


def watch_account(conn, account: Account) -> int:
    """Upsert the account and put it on the scrape list."""
    account_id = upsert_account(conn, account)
    with conn.cursor() as cur:
        cur.execute("UPDATE accounts SET is_watched = TRUE WHERE id = %s", (account_id,))
        conn.commit()
    return account_id


def is_account_approved(conn, account: Account) -> bool:
    """True if the account is already in the database and approved. Unknown accounts are not approved."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT is_approved FROM accounts WHERE platform = %s AND username = %s",
            (account.platform, account.username),
        )
        row = cur.fetchone()
        return bool(row and row[0])
