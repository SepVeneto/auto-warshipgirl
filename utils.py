import win32gui
import toml

config = toml.load('./config.toml')
def getWindowSize():
  hwnd = win32gui.FindWindow(None, config.get('basic')['title'])
  return win32gui.GetWindowRect(hwnd)

