from abc import ABC


class ImageStorageService(ABC):
    def upload(
            self,
            path: str,
            image: str,
    ) -> None:
        """
        Persist an image.

        :param path: path
        :param image: image base64 format
        """
        pass
