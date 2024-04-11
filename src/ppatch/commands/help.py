from rich import print

from ppatch.app import app
from ppatch.config import settings


@app.command("settings")
def show_settings():
    print(settings.model_dump_json())
