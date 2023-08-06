from .widget import Widget


class NumberBox(Widget):
    def __init__(self, text: str, parent=None, address=''):
        super().__init__(parent, address)
        self._number = 0
        self._focusable = True

    def _show(self, canvas):
        x, y, w, h = self._box
        if self._focused:
            canvas.draw_frame(self._box, thick=True)
        else:
            canvas.draw_frame(self._box, thick=False, dashed=True)
        text = str(self._number)
        textw, texth = strsize(text)
        textx = w - textw - 1
        texty = int((h - texth) / 2)
        canvas.draw_text(text, (x + textx, y + texty))

    def _handle_key(self, key):
        if ord('0') <= key <= ord('9'):
            n = int(key)
            self._number
            return
        return key
