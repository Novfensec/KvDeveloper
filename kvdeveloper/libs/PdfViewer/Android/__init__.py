from android.runnable import run_on_ui_thread  # type: ignore
from jnius import autoclass  # type: ignore


@run_on_ui_thread
def open_pdf_on_android(filepath: str, *args) -> None:
    try:
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        File = autoclass("java.io.File")
        file = File(filepath)
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
