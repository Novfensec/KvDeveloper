from jnius import autoclass, cast  # type: ignore
from kivy.utils import platform

if platform == "android":
    # Java classes
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    WebView = autoclass("android.webkit.WebView")
    WebViewClient = autoclass("android.webkit.WebViewClient")


class WebViewAPI:
    def __init__(self):
        if platform == "android":
            # Access the current Android activity
            self.activity = PythonActivity.mActivity
        else:
            raise NotImplementedError("WebView is only supported on Android")

    def create_webview(self):
        if platform != "android":
            raise EnvironmentError("This method is supported only on Android")

        # Create a WebView instance
        self.webview = WebView(self.activity)
        self.webview_client = WebViewClient()

        # Configure the WebView
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.setWebViewClient(self.webview_client)

    def load_url(self, url):
        if not hasattr(self, "webview"):
            raise AttributeError(
                "WebView has not been created. Call create_webview() first."
            )

        # Load a URL in the WebView
        self.webview.loadUrl(url)

    def attach_to_layout(self):
        if not hasattr(self, "webview"):
            raise AttributeError(
                "WebView has not been created. Call create_webview() first."
            )

        # Attach the WebView to the current Android layout
        layout_params = autoclass("android.view.ViewGroup$LayoutParams")
        params = layout_params(
            layout_params.MATCH_PARENT,
            layout_params.MATCH_PARENT,
        )
        self.activity.addContentView(self.webview, params)
