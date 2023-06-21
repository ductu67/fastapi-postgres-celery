from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, select_autoescape, PackageLoader
from starlette.background import BackgroundTasks

from ..core.config import settings

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailTemplate:
    """Class to manage all Email operations."""

    def __init__(self):
        """Initialize the EmailManager.
                Define the configuration instance.
                """
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False
        )
        pass
        # self.html = """
        # <h2>Thanks for using Fastapi-mail</h2>
        # """

    async def send_mail_to_user(self, subject, template_name, user_name, email, url: str = None):
        template = env.get_template(f'{template_name}.html')
        html = template.render(
            url=url,
            first_name=user_name,
            subject=subject
        )
        if not html:
            html = self.html
        message = MessageSchema(
            subject=subject,
            recipients=email,
            body=html,
            subtype="html"
        )
        fm = FastMail(self.conf)
        await fm.send_message(message)
        return

    async def send_mail_background_to_user(self, backgroundtasks: BackgroundTasks, subject, template_name, user_name,
                                           url, email):
        template = env.get_template(f'{template_name}.html')
        html = template.render(
            url=url,
            first_name=user_name,
            subject=subject
        )
        message = MessageSchema(
            subject=subject,
            recipients=email,
            body=html,
            subtype="html"
        )
        fm = FastMail(self.conf)
        backgroundtasks.add_task(
            fm.send_message, message, template_name=template_name
        )
        return
