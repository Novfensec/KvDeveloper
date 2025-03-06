from jnius import autoclass  # type: ignore


class PdfViewer:
    def __init__(self, *args, **kwargs):
        pass

    def open_pdf(self, file_path: str, *args) -> None:
        try:
            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")
            File = autoclass("java.io.File")
            file = File(file_path)  # Replace with the path to your PDF file
            uri = Uri.fromFile(file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, "application/pdf")
            intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            current_activity = PythonActivity.mActivity
            current_activity.startActivity(intent)
        except Exception as e:
            print(f"Failed to open PDF: {e}")
