
import time

import board
import digitalio
import asyncio
import countio
import displayio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

global SHOTS_LEFT
global BULLETS_LEFT
global TOTAL_SHOTS
global TOTAL_BULLETS
global COUNTER_FONT
global BULLET_FONT

TOTAL_SHOTS = 120  # Number of shots
SHOTS_LEFT = TOTAL_SHOTS

TOTAL_BULLETS = 34 # number of bullet icons that can fit on the screen
BULLETS_LEFT = TOTAL_BULLETS

counter_font_file = "fonts/whiterabbit.bdf"
COUNTER_FONT = bitmap_font.load_font(counter_font_file)

bullet_font_file = "fonts/military.bdf"
BULLET_FONT = bitmap_font.load_font(bullet_font_file)

# TFT chipset: ST7789

async def catch_interrupt(pin):
    """Print a message when pin goes Down, We break the beam."""
    with countio.Counter(pin, edge=countio.Edge.FALL, pull=digitalio.Pull.UP) as interrupt:
        while True:
            if interrupt.count > 0:
                global SHOTS_LEFT
                global BULLETS_LEFT

                # Decrement shot as beam is broken
                SHOTS_LEFT -= 1

                # Shots should not go below 0
                if SHOTS_LEFT <= 0:
                    SHOTS_LEFT = 0

                BULLETS_LEFT = int((SHOTS_LEFT / TOTAL_SHOTS) * TOTAL_BULLETS)

                print("Shots left: {}".format(SHOTS_LEFT))
                print("Bullets: {}".format(BULLETS_LEFT))

                # reset interrupt counter.
                interrupt.count = 0
            # Let another task run.
            await asyncio.sleep(0)

async def update_shots_display():
    while True:
        green = 0x00FF00
        yellow = 0xFFFF00
        red = 0xFF0000

        # Default color
        font_color = green

        # Use yellow/red as we get close to out.
        if 50 > SHOTS_LEFT >= 20:
            font_color = yellow
        elif SHOTS_LEFT < 20:
            font_color = red

        text_area = []

        # counter area
        text_area.append(
            label.Label(
                font=COUNTER_FONT,
                color=font_color,
                scale=1,
                padding_bottom=4
            )
        )
        text_area[0].anchor_point = (0.5, 0.8)
        text_area[0].anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
        text_area[0].text = str(SHOTS_LEFT)

        # bullet area
        text_area.append(
            label.Label(
                font=BULLET_FONT,
                color=font_color,
                scale=1
            )
        )
        text_area[1].anchor_point = (0, 0)
        text_area[1].anchored_position = (0, board.DISPLAY.height - 20)
        text_area[1].text = "'" * BULLETS_LEFT

        group = displayio.Group()
        group.append(text_area[0])
        group.append(text_area[1])

        board.DISPLAY.show(group)

        await asyncio.sleep(0)

async def main():
    interrupt_task = asyncio.create_task(catch_interrupt(board.D5))
    update_shots_display_task = asyncio.create_task(update_shots_display())

    await asyncio.gather(interrupt_task, update_shots_display_task)

asyncio.run(main())


