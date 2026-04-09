import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.handlers import HandlerDependencies, create_router, get_localized_commands
from app.config import get_settings
from app.services.account_manager import TelegraphAccountManager
from app.services.account_store import AccountStore
from app.services.audit_service import AuditService
from app.services.i18n import I18nService
from app.services.inline_cache_service import InMemoryInlineCache
from app.services.md_converter import MarkdownConverter
from app.services.rate_limit_service import InMemoryRateLimiter
from app.services.telegraph_service import TelegraphService


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


async def run() -> None:
    settings = get_settings()
    setup_logging(settings.log_level.upper())

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    me = await bot.get_me()
    account_store = AccountStore(settings.accounts_db_path)
    account_manager = TelegraphAccountManager(
        enabled=settings.enable_personal_accounts,
        store=account_store,
        default_access_token=settings.telegraph_access_token,
        default_author_name=settings.default_author_name,
        default_author_url=(
            str(settings.default_author_url) if settings.default_author_url else None
        ),
    )

    deps = HandlerDependencies(
        converter=MarkdownConverter(),
        telegraph=TelegraphService(
            access_token=settings.telegraph_access_token,
            author_name=settings.default_author_name,
            author_url=str(settings.default_author_url) if settings.default_author_url else None,
            max_pages_per_request=settings.max_pages_per_request,
        ),
        audit=AuditService(),
        rate_limiter=InMemoryRateLimiter(settings.user_rate_limit_per_minute),
        inline_cache=InMemoryInlineCache(ttl_seconds=120),
        account_manager=account_manager,
        i18n=I18nService(
            locales_dir=settings.locales_dir,
            default_locale=settings.default_locale,
        ),
        bot_username=me.username or "bot",
        max_md_size=settings.max_md_size,
    )
    # Register localized command menus for all supported locales.
    for locale in deps.i18n.supported_locales():
        await bot.set_my_commands(
            commands=get_localized_commands(deps.i18n, locale),
            language_code=locale,
        )
    await bot.set_my_commands(
        commands=get_localized_commands(deps.i18n, settings.default_locale),
    )

    dp.include_router(create_router(deps))
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()

