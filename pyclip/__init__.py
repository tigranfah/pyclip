import sys
import os
import logging

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import pygame_gui

sys.path.append(os.path.join(os.getcwd(), "pyclip"))

pygame.init()

logging_format = "%(message)s - %(levelname)s - %(asctime)s - %(name)s"

logging.basicConfig(level=logging.INFO, format=logging_format)

from clip import *
from movie import *
from viewer import *
from writer import *

# import clip
# import movie
# import viewer
# import writer
