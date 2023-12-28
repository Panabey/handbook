from pathlib import Path
from datetime import datetime

from httpx import stream


def download_image_url(url: str, filename: str) -> tuple[str, bool]:
    """
    Скачивани изображение из сторонний сервисов по URL
    """
    save_dir = Path("media/avatars")

    full_path = f"media/avatars/{filename}.jpeg"
    if not save_dir.exists():
        save_dir.mkdir(parents=True)

    path = Path(full_path)

    with stream("GET", url, headers={"Cache-Control": "no-cache"}) as response:
        if path.exists():
            last_modif = response.headers["last-modified"]
            dt = datetime.strptime(last_modif, "%a, %d %b %Y %H:%M:%S %Z")
            if dt.timestamp() <= path.stat().st_ctime:
                # Если изображение существует и не было изменено
                return full_path, False

        with open(full_path, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

    return full_path, True
