from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class I18nService:
    def __init__(self, locales_dir: str, default_locale: str = "en") -> None:
        self._default_locale = default_locale.lower()
        self._translations: dict[str, dict[str, str]] = {}
        self._load_locales(locales_dir)

    def _load_locales(self, locales_dir: str) -> None:
        base = Path(locales_dir)
        for path in base.glob("*.json"):
            locale = path.stem.lower()
            data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            self._translations[locale] = {k: str(v) for k, v in data.items()}

    def resolve_locale(self, language_code: str | None) -> str:
        if not language_code:
            return self._default_locale
        normalized = language_code.lower().replace("_", "-")
        candidates = [normalized, normalized.split("-")[0], self._default_locale]
        for candidate in candidates:
            if candidate in self._translations:
                return candidate
        return self._default_locale

    def supported_locales(self) -> list[str]:
        return sorted(self._translations.keys())

    def t(self, locale: str, key: str, **kwargs: Any) -> str:
        text = self._translations.get(locale, {}).get(key)
        if text is None:
            text = self._translations.get(self._default_locale, {}).get(key, key)
        return text.format(**kwargs)

