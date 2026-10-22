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


def sync_watched_accounts(conn, platform: str, user_urls: list[str]) -> None:
    """Mark accounts on the platform as watched exactly when their profile URL is in user_urls."""
    normalized_urls = [url.rstrip('/').lower() for url in user_urls]
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE accounts
            SET is_watched = (lower(rtrim(account_url, '/')) = ANY(%s))
            WHERE platform = %s
            """,
            (normalized_urls, platform),
        )
        conn.commit()


def is_account_approved(conn, account: Account) -> bool:
    """True if the account is already in the database and approved. Unknown accounts are not approved."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT is_approved FROM accounts WHERE platform = %s AND username = %s",
            (account.platform, account.username),
        )
        row = cur.fetchone()
        return bool(row and row[0])
