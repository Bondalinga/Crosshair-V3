import tkinter as tk
import threading
import keyboard
import time
import config

visible = True  # Initialize the 'visible' variable
toggle_lock = threading.Lock()  # Lock for synchronization
outline_width = config.outline_width  # Outline width

class CrosshairOverlay(tk.Tk):
    def __init__(self, size, width, distance, color_r, color_g, color_b, is_outline=True, is_crosshair=True, offset_x=0, offset_y=0, crosshair_visible=True):
        super().__init__()
        self.l = size
        self.w = width
        self.tn = distance
        self.nk = self._nk(self.w, self.tn)
        self.L = self._L(self.l, self.nk)
        self.LL = self._LL(self.L, self.w)
        self.ox = offset_x
        self.oy = offset_y
        self.c = "#" + "".join(map(lambda x: format(int(x), "02x"), [color_r, color_g, color_b])).upper()
        self.iol = is_outline
        self.ich = is_crosshair
        self.update_enabled = True  # Added flag to enable/disable updates
        self.visible = True  # Hiding flag

        self.geometry(self._gm(self.L + 4, self.L + 4, self.ox, self.oy))
        self.canvas = tk.Canvas(self, bg="snow", width=self.L + self.w, height=self.L + self.w,
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._init_transparent()
        self._calculate_offsets()

        # Start a separate thread for keyboard events
        self.keyboard_thread = threading.Thread(target=self._start_keyboard_thread)
        self.keyboard_thread.start()

    def _start_keyboard_thread(self):
        keyboard.add_hotkey('home', self.toggle_visibility)
        keyboard.wait('esc')  # Wait for the 'esc' key to exit the thread

    def _calculate_offsets(self):
        self.ox = (self.winfo_screenwidth() - self.L) // 2
        self.oy = (self.winfo_screenheight() - self.L) // 2
        self.geometry(self._gm(self.L + 4, self.L + 4, self.ox, self.oy))

    def _init_transparent(self):
        self.overrideredirect(True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "snow")
        self.bind("<Button-1>", self.on_click)

    def _update_crosshair(self):
        import os
        import sys
        sys.stdout = open(os.devnull, 'w')
        if not self.update_enabled:
            return

        # Clear existing items on the canvas
        self.canvas.delete("all")

        # Implement the logic to draw the crosshair based on the user's preferences
        if self.ich:
            self._create_crosshair()

    def _create_crosshair(self):
        self._create_crosshair_up()
        self._create_crosshair_down()
        self._create_crosshair_left()
        self._create_crosshair_right()

    def _create_crosshair_up(self):
        if config.draw_top:
            if self.iol:
                self.canvas.create_rectangle(self.LL, 0, self.LL + self.w + 1, self.l + 1, fill=self.c, width=outline_width)
            else:
                self.canvas.create_rectangle(self.LL, 0, self.LL + self.w + 1, self.l + 1, fill=self.c, outline="snow", width=outline_width)
        else:
            pass

    def _create_crosshair_down(self):
        if config.draw_bottom:
            if self.iol:
                self.canvas.create_rectangle(self.LL, self.l + self.nk, self.LL + self.w + 1, self.L + 1, fill=self.c, width=outline_width)
            else:
                self.canvas.create_rectangle(self.LL, self.l + self.nk, self.LL + self.w + 1, self.L + 1, fill=self.c, outline="snow", width=outline_width)
        else:
            pass

    def _create_crosshair_left(self):
        if config.draw_left:
            if self.iol:
                self.canvas.create_rectangle(0, self.LL, self.l + 1, self.LL + self.w + 1, fill=self.c, width=outline_width)
            else:
                self.canvas.create_rectangle(0, self.LL, self.l + 1, self.LL + self.w + 1, fill=self.c, outline="snow", width=outline_width)
        else:
            pass

    def _create_crosshair_right(self):
        if config.draw_right:
            if self.iol:
                self.canvas.create_rectangle(self.l + self.nk, self.LL, self.L + 1, self.LL + self.w + 1, fill=self.c, width=outline_width)
            else:
                self.canvas.create_rectangle(self.l + self.nk, self.LL, self.L + 1, self.LL + self.w + 1, fill=self.c, outline="snow", width=outline_width)
        else:
            pass

    def _gm(self, ww, wh, offset_x, offset_y):
        return str(int(ww)) + "x" + str(int(wh)) + "+" + str(int(offset_x)) + "+" + str(int(offset_y))

    def _nk(self, w, tn):
        return w + tn * 2

    def _L(self, l, nk):
        return nk + l * 2

    def _LL(self, L, w):
        return (L - w) / 2

    def on_click(self, event):
        # Handle the click event, or do nothing to make it transparent to mouse clicks
        pass

    def toggle_visibility(self):
        with toggle_lock:
            if self.visible:
                self.after(1, self.withdraw)
            else:
                self.after(1, self.deiconify)
            self.visible = not self.visible

if __name__ == "__main__":
    app = CrosshairOverlay(config.size, config.width, config.distance,config.color_r, config.color_g, config.color_b, config.crosshair_visible, config.draw_top, config.draw_bottom, config.draw_right, config.draw_left)
    app.mainloop()