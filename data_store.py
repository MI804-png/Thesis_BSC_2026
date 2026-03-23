from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from werkzeug.security import check_password_hash, generate_password_hash


DB_PATH = Path(__file__).with_name("hr_analysis.db")

DEFAULT_USERS = [
    {"username": "admin", "password": "admin123", "role": "admin", "full_name": "System Administrator"},
    {"username": "ceo", "password": "ceo123", "role": "ceo", "full_name": "Chief Executive Officer"},
    {"username": "hr", "password": "hr123", "role": "hr", "full_name": "HR Director"},
    {"username": "finance", "password": "finance123", "role": "finance", "full_name": "Finance Manager"},
    {"username": "operations", "password": "operations123", "role": "operations", "full_name": "Operations Lead"},
]


def _dict_from_row(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                source TEXT NOT NULL,
                provider TEXT,
                batch_name TEXT,
                created_by INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                result_json TEXT NOT NULL,
                FOREIGN KEY(created_by) REFERENCES users(id)
            );
            """
        )

        user_count = connection.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
        if user_count == 0:
            now = datetime.now(timezone.utc).isoformat()
            connection.executemany(
                """
                INSERT INTO users (username, password_hash, role, full_name, created_at)
                VALUES (:username, :password_hash, :role, :full_name, :created_at)
                """,
                [
                    {
                        "username": user["username"],
                        "password_hash": generate_password_hash(user["password"]),
                        "role": user["role"],
                        "full_name": user["full_name"],
                        "created_at": now,
                    }
                    for user in DEFAULT_USERS
                ],
            )


def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username.strip().lower(),),
        ).fetchone()
    user = _dict_from_row(row)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_user_by_id(user_id: int | None) -> dict[str, Any] | None:
    if user_id is None:
        return None
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return _dict_from_row(row)


def save_analysis(
    *,
    created_by: int,
    company_name: str,
    payload: Mapping[str, Any],
    result: Mapping[str, Any],
    source: str = "manual",
    provider: str | None = None,
    batch_name: str | None = None,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analyses (company_name, source, provider, batch_name, created_by, created_at, payload_json, result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_name,
                source,
                provider,
                batch_name,
                created_by,
                now,
                json.dumps(dict(payload)),
                json.dumps(dict(result)),
            ),
        )
        return int(cursor.lastrowid)


def _hydrate_analysis(row: sqlite3.Row | None) -> dict[str, Any] | None:
    record = _dict_from_row(row)
    if record is None:
        return None
    record["payload"] = json.loads(record.pop("payload_json"))
    record["result"] = json.loads(record.pop("result_json"))
    return record


def get_analysis_by_id(analysis_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT analyses.*, users.username, users.full_name, users.role
            FROM analyses
            JOIN users ON users.id = analyses.created_by
            WHERE analyses.id = ?
            """,
            (analysis_id,),
        ).fetchone()
    return _hydrate_analysis(row)


def list_recent_analyses(user_id: int, role: str, limit: int = 15) -> list[dict[str, Any]]:
    query = (
        """
        SELECT analyses.*, users.username, users.full_name, users.role
        FROM analyses
        JOIN users ON users.id = analyses.created_by
        """
    )
    params: Iterable[Any]
    if role == "admin":
        query += " ORDER BY analyses.created_at DESC LIMIT ?"
        params = (limit,)
    else:
        query += " WHERE analyses.created_by = ? ORDER BY analyses.created_at DESC LIMIT ?"
        params = (user_id, limit)

    with get_connection() as connection:
        rows = connection.execute(query, tuple(params)).fetchall()
    return [_hydrate_analysis(row) for row in rows if row is not None]


def list_company_history(company_name: str, user_id: int, role: str) -> list[dict[str, Any]]:
    query = "SELECT * FROM analyses WHERE company_name = ?"
    params: list[Any] = [company_name]
    if role != "admin":
        query += " AND created_by = ?"
        params.append(user_id)
    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        rows = connection.execute(query, tuple(params)).fetchall()
    return [_hydrate_analysis(row) for row in rows if row is not None]
