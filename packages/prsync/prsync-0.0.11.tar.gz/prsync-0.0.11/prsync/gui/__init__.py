from prsync.gui import screen, screen_api
import prsync.gui.screen

__all__ = ["screen", "api"]
__version__ = "0.1.0"
__author__ = "Itay Bardugo, itaybardugo91@gmail.com"

api = screen_api.ScreenApi() #init the gui API (screen.py should will call method in that class)