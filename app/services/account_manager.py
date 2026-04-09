from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from aiogram.types import User

from app.services.account_store import AccountStore, UserAccount


class AccountManagerError(Exception):
    """Raised when personal account action fails."""


@dataclass(slots=True)
class PublishContext:
    access_token: str
    author_name: str
    author_url: str | None
    mode: str


def _build_author_name(user: User) -> str:
    if user.username:
        return f"@{user.username}"
    full_name = " ".join(part for part in [user.first_name, user.last_name] if part).strip()
    return full_name or f"Telegram User {user.id}"


def _build_author_url(user: User) -> str:
    if user.username:
        return f"https://t.me/{user.username}"
    return f"tg://user?id={user.id}"


class TelegraphAccountManager:
    def __init__(
        self,
        *,
        enabled: bool,
        store: AccountStore,
        default_access_token: str,
        default_author_name: str,
        default_author_url: str | None,
    ) -> None:
        self._enabled = enabled
        self._store = store
        self._default_access_token = default_access_token
        self._default_author_name = default_author_name
        self._default_author_url = default_author_url

    @property
    def enabled(self) -> bool:
        return self._enabled

    async def create_or_enable_personal(self, user: User) -> UserAccount:
        if not self._enabled:
            raise AccountManagerError("PERSONAL_ACCOUNTS_DISABLED")
        existing = self._store.get(user.id)
        if existing and existing.access_token:
            self._store.set_mode(user.id, "personal")
            return self._store.get(user.id) or existing

        author_name = _build_author_name(user)
        author_url = _build_author_url(user)
        short_name = f"tg_{user.id}"[:32]
        payload = {
            "short_name": short_name,
            "author_name": author_name[:128],
            "author_url": author_url[:512],
        }

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post("https://api.telegra.ph/createAccount", data=payload)
            response.raise_for_status()
            data = response.json()
        if not data.get("ok"):
            raise AccountManagerError(str(data.get("error", "CREATE_ACCOUNT_FAILED")))

        result: dict[str, Any] = data["result"]
        token = result.get("access_token")
        if not token:
            raise AccountManagerError("NO_ACCESS_TOKEN")
        self._store.upsert_personal_account(
            user_id=user.id,
            access_token=str(token),
            short_name=str(result.get("short_name", short_name)),
            author_name=str(result.get("author_name", author_name)),
            author_url=str(result.get("author_url", author_url)),
            mode="personal",
        )
        return self._store.get(user.id)  # type: ignore[return-value]

    async def rotate_personal_token(self, user_id: int) -> UserAccount:
        account = self._store.get(user_id)
        if not account or not account.access_token:
            raise AccountManagerError("NO_PERSONAL_ACCOUNT")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://api.telegra.ph/revokeAccessToken",
                data={"access_token": account.access_token},
            )
            response.raise_for_status()
            data = response.json()
        if not data.get("ok"):
            raise AccountManagerError(str(data.get("error", "ROTATE_FAILED")))
        result: dict[str, Any] = data["result"]
        token = result.get("access_token")
        if not token:
            raise AccountManagerError("NO_ACCESS_TOKEN")
        self._store.upsert_personal_account(
            user_id=user_id,
            access_token=str(token),
            short_name=account.short_name or f"tg_{user_id}",
            author_name=account.author_name or f"Telegram User {user_id}",
            author_url=account.author_url or f"tg://user?id={user_id}",
            mode=account.mode,
        )
        return self._store.get(user_id)  # type: ignore[return-value]

    def set_shared_mode(self, user_id: int) -> None:
        self._store.set_mode(user_id, "shared")

    def get_status(self, user_id: int) -> UserAccount | None:
        return self._store.get(user_id)

    def resolve_publish_context(self, user: User | None) -> PublishContext:
        if not user:
            return PublishContext(
                access_token=self._default_access_token,
                author_name=self._default_author_name,
                author_url=self._default_author_url,
                mode="shared",
            )
        account = self._store.get(user.id)
        if account and account.mode == "personal" and account.access_token:
            return PublishContext(
                access_token=account.access_token,
                author_name=account.author_name or _build_author_name(user),
                author_url=account.author_url or _build_author_url(user),
                mode="personal",
            )
        return PublishContext(
            access_token=self._default_access_token,
            author_name=self._default_author_name,
            author_url=self._default_author_url,
            mode="shared",
        )

