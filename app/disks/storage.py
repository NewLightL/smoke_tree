import logging
import os
from typing import BinaryIO
from pathlib import Path

import yadisk
import shutil
from fastapi_storages.base import BaseStorage

from app.core import load_config
from app.disks.secure import secure_filename


log = logging.getLogger(f"my_logger.{os.path.dirname(os.path.abspath(__file__))}")

class YandexStorage(BaseStorage):
    def __init__(
        self,
        token: str,
        secret: str,
        client_id: str,
        disk_path: str = "/",
        static_path: str = "/",
        ) -> None:
        self.client = yadisk.Client(
            id=client_id,
            secret=secret,
            token=token
        )
        self.disk_path = Path(disk_path) # Папка на диске
        self.static_path = Path(static_path) # Папка static
        self.static_path.mkdir(exist_ok=True, parents=True)

        with self.client:
            if not self.client.check_token(token):
                raise ValueError("not connect to the disk")


    def write(self, file: BinaryIO, name: str) -> str: # type: ignore
        try:
            local_path = str(self.static_path / Path(name))

            if not os.path.exists(local_path):
                with open(local_path, "wb") as local_file:
                    file.seek(0)
                    shutil.copyfileobj(file, local_file)
            else:
                with open(local_path, "wb") as local_file:
                    file.seek(0)
                    local_file.truncate(0)
                    shutil.copyfileobj(file, local_file)

            with self.client:
                remote_path = str(self.disk_path / Path(name))
                if not self.client.exists(remote_path):
                    with open(local_path, "rb") as local_file:
                        local_file.seek(0)
                        self.client.upload(local_file, remote_path)
                self.check_file_in_static_path(name)

            return name
        except Exception as ex:
            log.fatal(ex)


    def get_name(self, name: str) -> str:
        return secure_filename(Path(name).name)


    def get_path(self, name: str) -> str:
        return str(self.static_path / Path(name))


    def get_size(self, name: str) -> int:
        with self.client:
            try:
                meta = self.client.get_meta(f"{self.disk_path}/{name}")
                return meta.size if meta.size is not None else 0
            except:
                return 0


    def open(self, name: str) -> BinaryIO: # type: ignore
        try:
            self.check_file_in_static_path(name)
            path = self.static_path / Path(name).name

            return open(path, "rb")
        except Exception as ex:
            log.fatal(ex)

    def generate_new_filename(self, filename: str) -> str:
        try:
            with self.client:
                self.check_file_in_static_path(filename)

                counter = 0
                path = self.static_path / filename
                stem, extension = Path(filename).stem, Path(filename).suffix

                while path.exists():
                    counter += 1
                    path = self.static_path / f"{stem}_{counter}{extension}"

                return path.name
        except Exception as ex:
            log.fatal(ex)


    def _download_file_to_static(self, disk_path: str, file_path: str) -> None:
        try:
            with self.client:
                with open(os.path.join(file_path), "wb") as file:
                    file.seek(0)
                    self.client.download(
                        disk_path,
                        file
                    )
        except Exception as ex:
            log.fatal(ex)


    def check_file_in_static_path(self, name: str) -> None:
        try:
            with self.client:
                local_path = os.path.join(self.static_path, name)

                if not os.path.exists(local_path):
                    remote_path = os.path.join(self.disk_path, name)
                    self._download_file_to_static(remote_path, local_path)
        except Exception as ex:
            log.fatal(ex)


settings = load_config()

yandex_storage = YandexStorage(
    settings.api.yandex_token,
    settings.api.yandex_secret,
    settings.api.yandex_client_id,
    static_path=os.path.join(settings.core.static_path, "photo")
)
