import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from markdown2 import markdown
from typing import Optional
from .config import def_dir, IMAGE_LIBRARY, app


class MarkdownDisplayer(QMainWindow):
    def __init__(self) -> None:
        """
        Initialize the MarkdownDisplayer window.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """
        Set up the UI components for the main window.
        """
        self.setWindowTitle("KvDeveloper")
        self.setWindowIcon(QIcon(f"{IMAGE_LIBRARY}/kvdeveloper/kvdeveloper_logo64.png"))
        self.setGeometry(100, 100, 1100, 600)

        # Create a QWebEngineView to render HTML content
        self.browser = QWebEngineView()

        # Enable JavaScript clipboard access in the browser
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

        # Set up the central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

    def display_markdown(self, directory: str) -> None:
        """
        Load and display the markdown content from a specified directory.

        :param directory: The directory containing the README.md file.
        """
        # Read the markdown file
        with open(
            os.path.join(directory, "readme.md"), "r", encoding="utf-8"
        ) as md_file:
            markdown_content = md_file.read()

        # Convert markdown content to HTML
        html_content = markdown(
            markdown_content,
            extras=[
                "fenced-code-blocks",
                "tables",
                "code-friendly",
                "strike",
                "markdown-in-html",
            ],
        )

        # Load CSS and JavaScript for styling and syntax highlighting
        with open(
            os.path.join(def_dir, "assets/css/github-markdown.css"),
            "r",
            encoding="utf-8",
        ) as css_file:
            css_content = css_file.read()

        with open(
            os.path.join(def_dir, "assets/js/prism.js"), "r", encoding="utf-8"
        ) as js_file:
            js_content = js_file.read()

        with open(
            os.path.join(def_dir, "assets/css/prism.css"), "r", encoding="utf-8"
        ) as highlight_file:
            highlight_content = highlight_file.read()

        # Create the complete HTML content with embedded CSS and JavaScript
        base_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                {css_content}
                {highlight_content}
            </style>
        </head>
        <body class="markdown-body">
            {html_content}
            <script>
                {js_content}
            </script>
        </body>
        </html>
        """

        # Display the HTML content in the QWebEngineView
        self.browser.setHtml(base_html)


def info_reader(directory: str) -> None:
    """
    Start a window displaying the markdown file.

    :param directory: The directory containing the README.md file.
    """
    # Create the application and the main window
    app = QApplication(sys.argv)
    window = MarkdownDisplayer()

    # Show the window and display the markdown content
    window.display_markdown(directory)
    window.show()

    # Start the application event loop
    sys.exit(app.exec_())
