import pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
import sys
import requests
import json

class TranslatorThread(QThread):
    """Thread for running the translation API call in the background."""
    translated_text_signal = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        """Run the translation in the background."""
        translated_text = self.translate_to_english(self.text)
        self.translated_text_signal.emit(translated_text)

    def translate_to_english(self, text):
        """Uses LibreTranslate API to translate text to English (self-hosted)."""
        try:
            url = "https://YOUR_API_ENDPOINT/translate"
            headers = {"Content-Type": "application/json"}
            data = {
                "q": text,
                "source": "auto",  # Automatically detect source language
                "target": "en",    # Target language is English
                "format": "text",
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                return "Translation failed. API error."
            result = response.json()
            return result.get("translatedText", "Translation failed.")
        except Exception:
            return "Translation failed."

class PasteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Remove window decorations
        self.setGeometry(100, 100, 500, 250)

        # Create the lower (non-editable) text box
        self.text_box_non_editable = QTextEdit(self)
        self.text_box_non_editable.setReadOnly(True)  # Make it non-editable
        self.text_box_non_editable.setStyleSheet("QTextEdit { background-color: #222222; color: white; }")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.text_box_non_editable)  # Lower non-editable text box
        self.setLayout(layout)

        # Start the loading animation
        self.loading_index = 0
        self.loading_chars = ['\\', '|', '/', '-', '\\', '|']
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loading_animation)
        self.timer.start(300)  # Update every 300 ms

        # Translate clipboard contents when the window is initialized
        self.paste_and_translate_clipboard_contents()

    def paste_and_translate_clipboard_contents(self):
        """Pastes clipboard contents and translates to English."""
        clipboard_text = pyperclip.paste()  # Get the clipboard text

        if clipboard_text:  # Only proceed if clipboard contains text
            self.translator_thread = TranslatorThread(clipboard_text)
            self.translator_thread.translated_text_signal.connect(self.update_translated_text)
            self.translator_thread.start()

    def update_loading_animation(self):
        """Update the loading animation in the non-editable text box."""
        self.text_box_non_editable.setPlainText(self.loading_chars[self.loading_index])
        self.loading_index = (self.loading_index + 1) % len(self.loading_chars)

    def update_translated_text(self, translated_text):
        """Updates the lower text box with the translated text."""
        self.timer.stop()  # Stop the loading animation
        self.text_box_non_editable.setPlainText(translated_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasteApp()
    window.show()
    sys.exit(app.exec())
