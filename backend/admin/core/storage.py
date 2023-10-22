import os
import random
import string

from PIL import Image
from pathlib import Path
from slugify import slugify

from django.core.files import locks
from django.core.files.move import file_move_safe


from django.core.files.storage import FileSystemStorage


class CompressImageStorage(FileSystemStorage):
    def _save(self, name, content):
        # Стандартный модуль Django
        full_path = self.path(name)
        directory = os.path.dirname(full_path)

        try:
            if self.directory_permissions_mode is not None:
                old_umask = os.umask(0o777 & ~self.directory_permissions_mode)
                try:
                    os.makedirs(
                        directory, self.directory_permissions_mode, exist_ok=True
                    )
                finally:
                    os.umask(old_umask)
            else:
                os.makedirs(directory, exist_ok=True)
        except FileExistsError:
            raise FileExistsError(  # noqa: B904
                "%s exists and is not a directory." % directory
            )

        # Расширенный метод сохранения изображений
        full_path, ext = normalize_filename(full_path)
        if ext not in [".svg", ".gif", ".bmp", ".webp"]:
            new_size_ratio = 0.9
            full_path = generate_filename(full_path)

            with Image.open(content) as img:
                img = img.resize(
                    (
                        int(img.size[0] * new_size_ratio),
                        int(img.size[1] * new_size_ratio),
                    ),
                    Image.BILINEAR,
                )

                if img.mode == "LA":
                    img = img.convert("RGBA")
                if img.mode == "RGBA":
                    new_image = Image.new("RGB", img.size, (255, 255, 255))
                    new_image.paste(img, mask=img.split()[3])
                    img = new_image

                img.save(
                    full_path,
                    "JPEG",
                    quality=90,
                    optimize=True,
                    exif=b"",
                    progressive=True,
                )
        else:
            # Стандартный модуль Django
            while True:
                try:
                    # This file has a file path that we can move.
                    if hasattr(content, "temporary_file_path"):
                        file_move_safe(content.temporary_file_path(), full_path)

                    # This is a normal uploadedfile that we can stream.
                    else:
                        # The current umask value is masked out by os.open!
                        fd = os.open(full_path, self.OS_OPEN_FLAGS, 0o666)
                        _file = None
                        try:
                            locks.lock(fd, locks.LOCK_EX)
                            for chunk in content.chunks():
                                if _file is None:
                                    mode = "wb" if isinstance(chunk, bytes) else "wt"
                                    _file = os.fdopen(fd, mode)
                                _file.write(chunk)
                        finally:
                            locks.unlock(fd)
                            if _file is not None:
                                _file.close()
                            else:
                                os.close(fd)
                except FileExistsError:
                    # A new name is needed if the file exists.
                    name = self.get_available_name(name)
                    full_path = self.path(name)
                else:
                    # OK, the file save worked. Break out of the loop.
                    break

        if self.file_permissions_mode is not None:
            os.chmod(full_path, self.file_permissions_mode)

        # Ensure the saved path is always relative to the storage root.
        name = os.path.relpath(full_path, self.location)
        # Ensure the moved file has the same gid as the storage root.
        self._ensure_location_group_id(full_path)
        # Store filenames with forward slashes, even on Windows.
        return str(name).replace("\\", "/")


def normalize_filename(path: str):
    """Удаление символов, которые могут повлять на отображение/сохранение"""
    full_path = Path(path)
    # Исключает специальные символы и заменяет пробелы на подчёркивания
    filename = slugify(full_path.stem, max_length=255)
    filename = filename + full_path.suffix
    return (full_path.parent / filename).as_posix(), full_path.suffix


def generate_filename(path: str):
    """Генерация имени изображения для последующего сохранения"""
    full_path = Path(path)
    full_path = full_path.with_suffix(".jpeg")

    # Если файл с таким именем уже существует добавить случайные данные в путь
    if full_path.exists():
        random_choice = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        filename = f"{full_path.stem}-{random_choice}{full_path.suffix}"
    else:
        filename = full_path.name
    return (full_path.parent / filename).as_posix()
