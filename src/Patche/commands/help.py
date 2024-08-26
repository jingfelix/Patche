from rich import print

from Patche.app import app
from Patche.config import settings


@app.command("settings")
def show_settings():
    """
    Show current settings
    """
    print(settings.model_dump_json())
