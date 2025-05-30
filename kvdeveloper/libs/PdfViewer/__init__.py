from kivy.utils import platform


class PdfViewer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open_new_file(self, filepath: str, *args) -> None:

        if platform == "android":
            from .Android import open_pdf_on_android

            open_pdf_on_android(filepath=filepath)

        elif platform == "ios":
            from .iOS import open_pdf_on_ios

            open_pdf_on_ios(filepath=filepath)

        else:
            raise NotImplementedError
