from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.articles import translate_pending_articles

BATCH_SIZE = 50


def main():
    conn = Database().conn
    translate_pending_articles(conn, BATCH_SIZE)
    conn.close()


if __name__ == '__main__':
    main()
