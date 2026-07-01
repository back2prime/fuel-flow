import resend
from pathlib import Path

from core.config import settings


class ResendHelper:
    """Wrapper around the Resend SDK for sending transactional emails.

    Loads the HTML reset-password template once at init time.
    All send methods are async and use resend.Emails.send_async internally.
    """

    def __init__(self, email: str, key: str):
        self._email = email
        resend.api_key = key
        self._reset_template = (
            Path(__file__).parent.parent / "templates" / "reset_password.html"
        ).read_text(encoding="utf-8")

    async def send_email(
        self, to: str, subject: str, html: str
    ) -> resend.Emails.SendResponse:
        params: resend.Emails.SendParams = {
            "from": self._email,
            "to": to,
            "subject": subject,
            "html": html,
        }
        return await resend.Emails.send_async(params)

    async def send_reset_password(
        self, to: str, token: str
    ) -> resend.Emails.SendResponse:
        url = f"{settings.resend.FRONTEND_URL}/reset-password?token={token}"
        html = self._reset_template.replace("{url}", url)
        return await self.send_email(to=to, subject="Reset your password", html=html)


resend_helper = ResendHelper(
    email=settings.resend.FROM_EMAIL, key=settings.resend.RESEND_API_KEY
)
