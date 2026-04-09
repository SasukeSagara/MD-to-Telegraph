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

1. Incoming message from the user.
2. Rate limit and size validation.
3. Markdown → safe HTML.
4. Publish to Telegraph (1..N pages).
5. Reply with link(s).
6. Audit request metadata.

Optional:

7. User enables personal mode with `/myaccount on`.
8. The bot calls `createAccount` and stores the token in the local database.
9. Further publishes use the user’s personal author name.
