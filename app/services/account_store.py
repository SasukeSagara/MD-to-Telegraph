from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class UserAccount:
    user_id: int
    mode: str
    access_token: str | None
    short_name: str | None
    author_name: str | None
    author_url: str | None


class AccountStore:
    def __init__(self, db_path: str) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self._path))

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_telegraph_accounts (
                    user_id INTEGER PRIMARY KEY,
                    mode TEXT NOT NULL DEFAULT 'shared',
                    access_token TEXT,
                    short_name TEXT,
                    author_name TEXT,
                    author_url TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def get(self, user_id: int) -> UserAccount | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT user_id, mode, access_token, short_name, author_name, author_url
                FROM user_telegraph_accounts
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()
        if row is None:
            return None
        return UserAccount(
            user_id=int(row[0]),
            mode=str(row[1]),
            access_token=row[2],
            short_name=row[3],
            author_name=row[4],
            author_url=row[5],
        )

    def upsert_personal_account(
        self,
        *,
        user_id: int,
        access_token: str,
        short_name: str,
        author_name: str,
        author_url: str,
        mode: str = "personal",
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_telegraph_accounts (
                    user_id, mode, access_token, short_name, author_name, author_url
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    mode=excluded.mode,
                    access_token=excluded.access_token,
                    short_name=excluded.short_name,
                    author_name=excluded.author_name,
                    author_url=excluded.author_url,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (user_id, mode, access_token, short_name, author_name, author_url),
            )

    def set_mode(self, user_id: int, mode: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_telegraph_accounts (user_id, mode)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    mode=excluded.mode,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (user_id, mode),
            )

