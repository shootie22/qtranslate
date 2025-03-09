# qtranslate
a quick and simple tool to translate text for Linux

![preview](https://raw.githubusercontent.com/shootie22/qtranslate/refs/heads/main/readme-media/preview.gif)

### example usage:
1. have an instance of [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate)
2. add your instance's URL to the script on line 24
3. set up a shortcut to launch the script
4. ...
5. profit

### python requirements:
- pyperclip (for clipboard handling)
- PyQt6 (for the UI)
- requests (for making the API req)

so:
`pip install pyperclip pyqt6 requests`

---

I prefer not having window decorations, but you can turn them on by commenting line 47.

I've only tested it on Wayland. it may also work on x11.

feel free to contribute / fork / complain
