from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from aiogram.utils.markdown import hlink

from app.services.account_manager import AccountManagerError, TelegraphAccountManager
from app.services.audit_service import AuditEvent, AuditService
from app.services.i18n import I18nService
from app.services.inline_cache_service import InlineCacheValue, InMemoryInlineCache
from app.services.md_converter import MarkdownConverter
from app.services.rate_limit_service import InMemoryRateLimiter
from app.services.telegraph_service import TelegraphError, TelegraphService


@dataclass(slots=True)
class HandlerDependencies:
    converter: MarkdownConverter
    telegraph: TelegraphService
    audit: AuditService
    rate_limiter: InMemoryRateLimiter
    inline_cache: InMemoryInlineCache
    account_manager: TelegraphAccountManager
    i18n: I18nService
    bot_username: str
    max_md_size: int


def _build_user_label(message_user: Message | InlineQuery) -> str:
    user = message_user.from_user
    if not user:
        return "Telegram User"
    if user.username:
        return f"@{user.username}"
    full_name = " ".join(part for part in [user.first_name, user.last_name] if part).strip()
    return full_name or f"User {user.id}"


def _build_page_title(user_label: str) -> str:
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # Telegraph title limit: 1..256 chars
    title = f"{user_label} - {dt}"
    return title[:256]


def _extract_markdown_h1_title(markdown_text: str) -> str | None:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"^#\s+(.+?)\s*$", stripped)
        if not match:
            return None
        title = match.group(1).strip()
        return title[:256] if title else None
    return None


def _extract_title_and_body(markdown_text: str) -> tuple[str | None, str]:
    lines = markdown_text.splitlines()
    first_non_empty_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty_idx = idx
            break
    if first_non_empty_idx is None:
        return None, markdown_text

    first_line = lines[first_non_empty_idx].strip()
    match = re.match(r"^#\s+(.+?)\s*$", first_line)
    if not match:
        return None, markdown_text

    title = match.group(1).strip()
    if not title:
        return None, markdown_text

    body_lines = lines[:first_non_empty_idx] + lines[first_non_empty_idx + 1 :]
    # Drop one extra blank line after removed H1 to avoid leading gap.
    if (
        first_non_empty_idx < len(lines) - 1
        and body_lines
        and not body_lines[first_non_empty_idx].strip()
    ):
        del body_lines[first_non_empty_idx]
    return title[:256], "\n".join(body_lines)


def create_router(deps: HandlerDependencies) -> Router:
    router = Router()

    def locale_for(language_code: str | None) -> str:
        return deps.i18n.resolve_locale(language_code)

    def tr(locale: str, key: str, **kwargs: object) -> str:
        return deps.i18n.t(locale, key, **kwargs)

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        locale = locale_for(message.from_user.language_code if message.from_user else None)
        await message.answer(
            tr(locale, "start.message", bot_username=f"@{deps.bot_username}")
        )

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        locale = locale_for(message.from_user.language_code if message.from_user else None)
        await message.answer(
            tr(locale, "start.message", bot_username=f"@{deps.bot_username}")
        )

    @router.message(Command("myaccount"))
    async def myaccount(message: Message) -> None:
        user = message.from_user
        locale = locale_for(user.language_code if user else None)
        if not user:
            await message.answer(tr(locale, "error.user_not_detected"))
            return
        if not deps.account_manager.enabled:
            await message.answer(tr(locale, "error.personal_disabled"))
            return
        parts = (message.text or "").split(maxsplit=1)
        action = parts[1].strip().lower() if len(parts) > 1 else "status"
        if action == "status":
            account = deps.account_manager.get_status(user.id)
            if not account:
                await message.answer(tr(locale, "myaccount.status.none"))
                return
            has_token = "yes" if locale == "en" else "да"
            if not account.access_token:
                has_token = "no" if locale == "en" else "нет"
            await message.answer(
                tr(
                    locale,
                    "myaccount.status.full",
                    mode=account.mode,
                    has_token=has_token,
                    author=account.author_name or "-",
                    author_url=account.author_url or "-",
                )
            )
            return
        if action == "on":
            try:
                account = await deps.account_manager.create_or_enable_personal(user)
            except AccountManagerError as exc:
                await message.answer(tr(locale, "myaccount.on.error", error=str(exc)))
                return
            await message.answer(
                tr(
                    locale,
                    "myaccount.on.ok",
                    author=account.author_name or "-",
                    author_url=account.author_url or "-",
                )
            )
            return
        if action == "off":
            deps.account_manager.set_shared_mode(user.id)
            await message.answer(tr(locale, "myaccount.off.ok"))
            return
        if action == "rotate":
            try:
                account = await deps.account_manager.rotate_personal_token(user.id)
            except AccountManagerError as exc:
                await message.answer(tr(locale, "myaccount.rotate.error", error=str(exc)))
                return
            await message.answer(tr(locale, "myaccount.rotate.ok", mode=account.mode))
            return
        await message.answer(tr(locale, "myaccount.usage"))

    async def validate_request(user_id: int, text: str, request_id: str) -> str | None:
        if not deps.rate_limiter.allow(user_id):
            deps.audit.log(
                AuditEvent(
                    request_id=request_id,
                    user_id=user_id,
                    input_size=len(text),
                    status="rate_limited",
                    error_code="RATE_LIMITED",
                )
            )
            return "RATE_LIMITED"

        if len(text) > deps.max_md_size:
            deps.audit.log(
                AuditEvent(
                    request_id=request_id,
                    user_id=user_id,
                    input_size=len(text),
                    status="validation_error",
                    error_code="MAX_MD_SIZE_EXCEEDED",
                )
            )
            return "MAX_MD_SIZE_EXCEEDED"
        return None

    @router.message()
    async def publish_markdown(message: Message) -> None:
        text = (message.text or "").strip()
        locale = locale_for(message.from_user.language_code if message.from_user else None)
        if not text:
            await message.answer(tr(locale, "error.need_markdown"))
            return

        user_id = int(message.from_user.id) if message.from_user else 0
        request_id = deps.audit.new_request_id()
        validation_error = await validate_request(user_id, text, request_id)
        if validation_error == "RATE_LIMITED":
            await message.answer(tr(locale, "error.rate_limited"))
            return
        if validation_error == "MAX_MD_SIZE_EXCEEDED":
            await message.answer(
                tr(locale, "error.max_md_size", size=len(text), limit=deps.max_md_size)
            )
            return

        try:
            context = deps.account_manager.resolve_publish_context(message.from_user)
            extracted_title, body_text = _extract_title_and_body(text)
            html = deps.converter.to_telegraph_html(body_text)
            title = extracted_title or _build_page_title(_build_user_label(message))
            result = await deps.telegraph.publish_html(
                title=title,
                html=html,
                access_token=context.access_token,
                author_name=context.author_name,
                author_url=context.author_url,
            )
        except TelegraphError as exc:
            deps.audit.log(
                AuditEvent(
                    request_id=request_id,
                    user_id=user_id,
                    input_size=len(text),
                    status="publish_error",
                    error_code=str(exc),
                )
            )
            await message.answer(tr(locale, "error.publish_failed"))
            return

        deps.audit.log(
            AuditEvent(
                request_id=request_id,
                user_id=user_id,
                input_size=len(text),
                status="ok",
                result_url=result.urls[0],
            )
        )
        links = "\n".join(result.urls)
        context = deps.account_manager.resolve_publish_context(message.from_user)
        await message.answer(
            tr(
                locale,
                "publish.ok",
                mode=context.mode,
                page_count=result.page_count,
                links=links,
            )
        )

    @router.inline_query()
    async def inline_publish(inline_query: InlineQuery) -> None:
        text = inline_query.query.strip()
        locale = locale_for(
            inline_query.from_user.language_code if inline_query.from_user else None
        )
        user_id = int(inline_query.from_user.id) if inline_query.from_user else 0
        request_id = deps.audit.new_request_id()

        if not text:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="empty-query",
                        title=tr(locale, "inline.empty.title"),
                        description=tr(
                            locale,
                            "inline.empty.desc",
                            bot_username=f"@{deps.bot_username}",
                        ),
                        input_message_content=InputTextMessageContent(
                            message_text=tr(locale, "inline.empty.text")
                        ),
                    )
                ],
                cache_time=1,
                is_personal=True,
            )
            return

        validation_error = await validate_request(user_id, text, request_id)
        if validation_error == "RATE_LIMITED":
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="rate-limited",
                        title=tr(locale, "inline.rate.title"),
                        description=tr(locale, "inline.rate.desc"),
                        input_message_content=InputTextMessageContent(
                            message_text=tr(locale, "inline.rate.text")
                        ),
                    )
                ],
                cache_time=1,
                is_personal=True,
            )
            return
        if validation_error == "MAX_MD_SIZE_EXCEEDED":
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="md-too-large",
                        title=tr(locale, "inline.max.title"),
                        description=tr(locale, "inline.max.desc", limit=deps.max_md_size),
                        input_message_content=InputTextMessageContent(
                            message_text=tr(
                                locale,
                                "inline.max.text",
                                size=len(text),
                                limit=deps.max_md_size,
                            )
                        ),
                    )
                ],
                cache_time=1,
                is_personal=True,
            )
            return

        cache_key = sha256(text.encode("utf-8")).hexdigest()
        cached = deps.inline_cache.get(cache_key)
        if cached:
            urls_text = "\n".join(cached.urls)
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id=f"cached-{cache_key[:20]}",
                        title=tr(locale, "inline.cached.title"),
                        description=tr(locale, "inline.cached.desc", page_count=cached.page_count),
                        input_message_content=InputTextMessageContent(message_text=urls_text),
                    )
                ],
                cache_time=60,
                is_personal=True,
            )
            return

        try:
            context = deps.account_manager.resolve_publish_context(inline_query.from_user)
            extracted_title, body_text = _extract_title_and_body(text)
            html = deps.converter.to_telegraph_html(body_text)
            title = extracted_title or _build_page_title(_build_user_label(inline_query))
            result = await deps.telegraph.publish_html(
                title=title,
                html=html,
                access_token=context.access_token,
                author_name=context.author_name,
                author_url=context.author_url,
            )
        except TelegraphError as exc:
            deps.audit.log(
                AuditEvent(
                    request_id=request_id,
                    user_id=user_id,
                    input_size=len(text),
                    status="inline_publish_error",
                    error_code=str(exc),
                )
            )
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="publish-error",
                        title=tr(locale, "inline.publish_error.title"),
                        description=tr(locale, "inline.publish_error.desc"),
                        input_message_content=InputTextMessageContent(
                            message_text=tr(locale, "inline.publish_error.text")
                        ),
                    )
                ],
                cache_time=1,
                is_personal=True,
            )
            return

        deps.inline_cache.set(
            cache_key,
            InlineCacheValue(text=text, urls=result.urls, page_count=result.page_count),
        )
        deps.audit.log(
            AuditEvent(
                request_id=request_id,
                user_id=user_id,
                input_size=len(text),
                status="inline_ok",
                result_url=result.urls[0],
            )
        )
        urls_text = "\n".join(result.urls)
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id=f"ok-{cache_key[:20]}",
                    title=tr(locale, "inline.ok.title"),
                    description=tr(locale, "inline.ok.desc", page_count=result.page_count),
                    input_message_content=InputTextMessageContent(
                        message_text=f"{hlink('Telegraph', result.urls[0])}\n\n{urls_text}",
                        parse_mode="HTML",
                    ),
                )
            ],
            cache_time=30,
            is_personal=True,
        )

    return router


def get_localized_commands(i18n: I18nService, locale: str) -> list[BotCommand]:
    return [
        BotCommand(command="start", description=i18n.t(locale, "cmd.start")),
        BotCommand(command="myaccount", description=i18n.t(locale, "cmd.myaccount")),
        BotCommand(command="help", description=i18n.t(locale, "cmd.help")),
    ]

