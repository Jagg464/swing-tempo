"""Gmail API client (stub). Live: OAuth via credentials.json/token.json, list unread,
mark read, send notification + monthly check-in emails. See EM.1.1 / G.2 / G.3."""
from config import settings


def list_unread() -> list[dict]:
    raise NotImplementedError("Implement Gmail list_unread (google-api-python-client).")


def mark_read(message_id: str) -> None:
    raise NotImplementedError("Implement Gmail mark_read.")


def send_email(to: str, subject: str, body: str) -> None:
    if settings.DRY_RUN:
        print(f"[dry-run email] to={to} subject={subject!r}")
        return
    raise NotImplementedError("Implement Gmail send_email.")