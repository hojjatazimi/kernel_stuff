from pathlib import Path
import numpy as np
from PIL import Image
from psychopy import core, event, visual

win = visual.Window(
    (900, 900),
    screen=1,
    units='pix',
    allowGUI=True,
    fullscr=False
)

path_to_image_file = '/home/kernel/Downloads/1_1_1.png'

image_stim = visual.ImageStim(win, image=path_to_image_file)
text_stim = visual.TextStim(
    win,
    text="Showing image from file",
    pos=(0.0, 0.8),
    units="norm",
    height=0.05,
    wrapWidth=0.8,
)

image_stim.draw()
text_stim.draw()
win.flip()
event.waitKeys()
