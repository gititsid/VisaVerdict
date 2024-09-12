from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

CONFIG_FILE_PATH = PROJECT_ROOT / "config" / "config.yaml"

APP_HOST = "0.0.0.0"
APP_PORT = 8000
