import pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
import sys
import requests
import json

class TranslatorThread(QThread):
    translated_text_signal = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        translated_text = self.translate_to_english(self.text)
        self.translated_text_signal.emit(translated_text)

    def translate_to_english(self, text):
        try:
            url = "https://YOUR_API_ENDPOINT/translate"
            headers = {"Content-Type": "application/json"}
            data = {
                "q": text,
                "source": "auto",
                "target": "en",
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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # remove window decorations
        self.setGeometry(100, 100, 500, 250)

        self.text_box_non_editable = QTextEdit(self)
        self.text_box_non_editable.setReadOnly(True) 
        self.text_box_non_editable.setStyleSheet("QTextEdit { background-color: #222222; color: white; }")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_box_non_editable)
        self.setLayout(layout)

        # loading anim
        self.loading_index = 0
        self.loading_chars = ['\\', '|', '/', '-']
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loading_animation)
        self.timer.start(300) 

        self.paste_and_translate_clipboard_contents()

    def paste_and_translate_clipboard_contents(self):
        clipboard_text = pyperclip.paste()  # get the clipboard text

        if clipboard_text:  # only proceed if clipboard contains text
            self.translator_thread = TranslatorThread(clipboard_text)
            self.translator_thread.translated_text_signal.connect(self.update_translated_text)
            self.translator_thread.start()

    def update_loading_animation(self):
        self.text_box_non_editable.setPlainText(self.loading_chars[self.loading_index])
        self.loading_index = (self.loading_index + 1) % len(self.loading_chars)

    def update_translated_text(self, translated_text):
        self.timer.stop()  # stop the loading animation
        self.text_box_non_editable.setPlainText(translated_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasteApp()
    window.show()
    sys.exit(app.exec())
