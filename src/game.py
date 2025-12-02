# src/game.py
import arcade
import os

from src.setting import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
HOME_IMG = os.path.join(ASSET_DIR, "sprites", "home_screen1.png")


class upsideDownGame(arcade.Window):
    

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Background sprite (full-screen)
        self.bg_list = arcade.SpriteList()
        if os.path.exists(HOME_IMG):
            try:
                bg = arcade.Sprite(HOME_IMG)
                bg.center_x = SCREEN_WIDTH // 2
                bg.center_y = SCREEN_HEIGHT // 2
                bg.width = SCREEN_WIDTH
                bg.height = SCREEN_HEIGHT
                self.bg_list.append(bg)
            except Exception:
                print("Failed to load background sprite:", HOME_IMG)
        else:
            print("Background image not found:", HOME_IMG)

        # Button (LBWH coordinates)
        self.btn_left = SCREEN_WIDTH // 2 - 150
        self.btn_bottom = int(SCREEN_HEIGHT * 0.30)
        self.btn_width = 300
        self.btn_height = 80
        self.btn_right = self.btn_left + self.btn_width
        self.btn_top = self.btn_bottom + self.btn_height

        # Colors (use RGB tuples to avoid missing named colors)
        self.color_default = (200, 150, 0)   # dark yellow (default)
        self.color_hover = (255, 200, 0)     # brighter yellow on hover
        self.color_pressed = (150, 0, 0)     # dark red when clicked
        self.text_color = (255, 255, 255)    # white text

        # Interaction state
        self.is_hover = False
        self.is_pressed = False    # becomes True when button is clicked (until popup closed)
        self.show_popup = False

        # Prebuild text object for START (we draw it each frame)
        self.start_text = arcade.Text(
            "START",
            self.btn_left + self.btn_width // 2,
            self.btn_bottom + self.btn_height // 2 - 15,
            self.text_color,
            30,
            anchor_x="center",
            anchor_y="center",
        )

        # Popup properties (centered)
        self.popup_width = 420
        self.popup_height = 180
        self.popup_left = (SCREEN_WIDTH - self.popup_width) // 2
        self.popup_bottom = (SCREEN_HEIGHT - self.popup_height) // 2

        # Popup text
        self.popup_text = arcade.Text(
            "COMING SOON",
            SCREEN_WIDTH // 2,
            self.popup_bottom + self.popup_height // 2 + 10,
            (0, 0, 0),
            28,
            anchor_x="center",
            anchor_y="center",
        )

        # hint text
        self.hint_text = arcade.Text(
            ".....",
            SCREEN_WIDTH // 2,
            int(SCREEN_HEIGHT * 0.18),
            (220, 220, 220),
            12,
            anchor_x="center",
        )

    # ---------------- Drawing ----------------
    def on_draw(self):
        self.clear()

        # Draw background
        if len(self.bg_list) > 0:
            self.bg_list.draw()
        else:
            # fallback background fill
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.DARK_SLATE_GRAY
            )

        # Choose button color based on state
        if self.is_pressed:
            btn_color = self.color_pressed
        elif self.is_hover:
            btn_color = self.color_hover
        else:
            btn_color = self.color_default

        # Draw button filled rectangle (LBWH)
        try:
            # some builds expose lbwh functions
            arcade.draw_lbwh_rectangle_filled(self.btn_left, self.btn_bottom, self.btn_width, self.btn_height, btn_color)
            arcade.draw_lbwh_rectangle_outline(self.btn_left, self.btn_bottom, self.btn_width, self.btn_height, (0, 0, 0), border_width=3)
        except Exception:
            # fallback: draw via center-based function if needed
            cx = self.btn_left + self.btn_width // 2
            cy = self.btn_bottom + self.btn_height // 2
            arcade.draw_rectangle_filled(cx, cy, self.btn_width, self.btn_height, btn_color)
            arcade.draw_rectangle_outline(cx, cy, self.btn_width, self.btn_height, (0, 0, 0), border_width=3)

        # Draw START text
        self.start_text.draw()

        # Draw hint
        self.hint_text.draw()

        # Draw popup if requested
        if self.show_popup:
            # semi-transparent overlay darken
            try:
                arcade.draw_lbwh_rectangle_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 120))
            except Exception:
                # fallback: full opaque (some builds ignore alpha)
                arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0))

            # popup box (white)
            try:
                arcade.draw_lbwh_rectangle_filled(self.popup_left, self.popup_bottom, self.popup_width, self.popup_height, (255, 255, 255))
                arcade.draw_lbwh_rectangle_outline(self.popup_left, self.popup_bottom, self.popup_width, self.popup_height, (0, 0, 0), border_width=2)
            except Exception:
                arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.popup_width, self.popup_height, (255, 255, 255))
                arcade.draw_rectangle_outline(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.popup_width, self.popup_height, (0, 0, 0), border_width=2)

            # draw popup text (black)
            self.popup_text.draw()

    # ---------------- Input ----------------
    def on_mouse_motion(self, x, y, dx, dy):
        # update hover flag if mouse inside button rectangle
        self.is_hover = (self.btn_left <= x <= self.btn_right and self.btn_bottom <= y <= self.btn_top)
        # change cursor visibility/appearance: show mouse cursor always; (Arcade doesn't provide custom cursor reliably)
        # we won't change OS cursor; visual hover feedback is the button color change.

    def on_mouse_press(self, x, y, button, modifiers):
        # If popup open and user clicked outside popup -> close popup and reset pressed state
        if self.show_popup:
            if not (self.popup_left <= x <= self.popup_left + self.popup_width and self.popup_bottom <= y <= self.popup_bottom + self.popup_height):
                self.show_popup = False
                self.is_pressed = False
            return

        # If click inside button -> mark pressed and show popup
        if self.btn_left <= x <= self.btn_right and self.btn_bottom <= y <= self.btn_top:
            self.is_pressed = True
            self.show_popup = True

    def on_key_press(self, symbol, modifiers):
        # Escape closes popup if open
        if symbol == arcade.key.ESCAPE and self.show_popup:
            self.show_popup = False
            self.is_pressed = False

    def run(self):
        arcade.run()
   