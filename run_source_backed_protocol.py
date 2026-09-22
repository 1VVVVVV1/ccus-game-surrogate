"""Select the source-backed profile before importing the research pipeline."""
import os
from pathlib import Path

os.environ['CCUS_CONFIG_PATH'] = str(Path(__file__).resolve().parent / 'config/model_config.source_backed.json')

if __name__ == '__main__':
    from src.source_backed_protocol import main
    raise SystemExit(main())
