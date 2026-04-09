# User Flow

```mermaid
flowchart TD
    user[User] --> sendMd[SendMarkdown]
    sendMd --> validate[ValidateSizeAndRate]
    validate -->|invalid| reject[ReturnValidationError]
    validate -->|valid| resolveMode[ResolvePublishMode]
    resolveMode -->|shared| sharedCtx[UseSharedToken]
    resolveMode -->|personal| personalCtx[UsePersonalToken]
    sharedCtx --> convert[ConvertMarkdownToSafeHtml]
    personalCtx --> convert
    convert --> publish[PublishToTelegraph]
    publish -->|error| publishError[ReturnPublishError]
    publish -->|ok| reply[ReturnLinksToUser]
    reply --> audit[WriteAuditMetadata]

    user --> personalCmd["/myaccount on|off|status|rotate"]
    personalCmd --> accountActions[CreateOrManagePersonalAccount]
    accountActions --> accountStore[(AccountStore)]
    accountActions --> telegraphApi[telegraPhApi]
```

1. Входящее сообщение от пользователя.
2. Rate-limit и валидация размера.
3. Конвертация Markdown -> безопасный HTML.
4. Публикация в Telegraph (1..N страниц).
5. Ответ пользователю ссылкой(ами).
6. Аудит метаданных запроса.

Опционально:
7. Пользователь включает personal-режим через `/myaccount on`.
8. Бот создает Telegraph-account через `createAccount` и сохраняет токен в локальную БД.
9. Дальнейшие публикации идут от персонального имени пользователя.
