import win32gui
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

def getWindowSize():
  hwnd = win32gui.FindWindow(None, config.get('basic', 'title'))
  return win32gui.GetWindowRect(hwnd)

