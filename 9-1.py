from random import random
from string import Template
import cv2
import pyautogui
import collections
import time

import win32gui

START = (1367,824,1624,894)
BATTLE = (1418,816,1656,897)
CHOOSE = (908,787,1638,890)
CONTINUE = (1483,828,1653,858)
BACK = (1100,611,1273,654)
AREA = (657,229,1561,821)
DD = (266,587,1094,693)
REBACK = (1214,823,1384,888)

COUNT = 34

# path = Template(r'D:\repo\auto-suml\screenshots\start.png')
# res = pyautogui.locateOnScreen('D:/repo/auto-suml/screenshots/start.png')
# print(res, path.safe_substitute(type=type))
pyautogui.mouseInfo()

# im = pyautogui.screenshot()
# om = im.crop(REBACK)
# om.save(r'D:\repo\auto-suml\screenshots\reback_9-1.png')

class Back:
  def __init__(self, context) -> None:
    self.context = context
  def show(self):
    print('回港')
  def run(self):
    global COUNT
    self.context.action('back')
    COUNT -= 1
    # COUNT -= 1
    self.context.current = Continue(self.context)

class Reback:
  def __init__(self, context) -> None:
    self.context = context
  def show(self):
    print('撤退')
  def run(self):
    self.context.action('reback_9-1')
    self.context.current = Continue(self.context)

class Continue:
  def __init__(self, context) -> None:
    self.context = context
  def show(self):
    print('继续')
  def run(self):
    if self.checkBack():
      return
    if self.checkStart():
      return
    if self.checkBattle():
      return
    self.context.randomClick()
  def checkBack(self):
    if self.context.getPos('back'):
      self.context.current = Back(self.context)
      return True
    return False

  def checkBattle(self):
    if self.context.getPos('battle') and not self.context.getPos('DD'):
      self.context.current = Battle(self.context)
      return True
    if self.context.getPos('battle') and self.context.getPos('DD'):
      self.context.current = Reback(self.context)
      return False
    return False

  def checkStart(self):
    if self.context.getPos('start'):
      self.context.current = Start(self.context)
      return True
    return False
    

class Choose:
  def __init__(self, context) -> None:
    self.context = context
  def show(self):
    print('选择阵型')
  def run(self):
    try:
      self.context.action('choose')
      self.context.current = Continue(self.context)
    except TypeError:
      print('pass')

class Battle:
  context = None
  def __init__(self, context) -> None:
    self.context = context
  def show(self):
    print('开始战斗')
  def run(self):
    try:
      self.context.action('battle')
      self.context.current = Choose(self.context)
    except TypeError:
      print('pass')


class Start:
  context = None
  def __init__(self, context) -> None:
    self.context = context
  
  def show(self):
    print('开始出征')
  
  def run(self):
    print('剩余%d', COUNT)
    if COUNT == 0:
      return
    self.context.action('start')
    self.context.current = Continue(self.context) # except TypeError:

class Jounery:
  def __init__(self) -> None:
    self.start_context = Start(self)
    self.battle_context = Battle(self)
    self.choose_context = Choose(self)
    self.continue_context = Continue(self)
    self.back_context = Back(self)

    self.current = self.start_context

  def run(self):
    self.current.show()
    self.current.run()

  def action(self, type):
    left, top, width, height = self.getPos(type)
    center = pyautogui.center((left, top, width, height))
    pyautogui.click(center)
  
  def getPos(self, type):
    path = Template(r'D:\repo\auto-suml\screenshots\${type}.png')
    res = pyautogui.locateOnScreen(path.safe_substitute(type=type))
    print(res, path.safe_substitute(type=type))
    return res
  
  def randomClick(self):
    x1, y1, x2, y2 = AREA
    offsetWidth = x2 - x1
    offsetHeight = y2 - y1
    seed = random()
    pyautogui.click(x1 + seed * offsetWidth, y1 + seed * offsetHeight)

# jounery = Jounery()

# while True:
#   time.sleep(2)
#   jounery.run()

def getWindowSize(name = '战舰少女R - 标准引擎'):
  hwnd = win32gui.FindWindow(None, name)

  return win32gui.GetWindowRect(hwnd)

  # width = right - left
  # height = bottom - top
  # return (width, height)

NORMALIZE_LEFT = 280
NORMALIZE_TOP = 90
NORMALIZE_WIDTH = 2000
NORMALIZE_HEIGHT = 1214


rect = getWindowSize()

def getScale(path):
  left, top, right, bottom = rect
  width = right - left
  height = bottom - top
  # leftOffset = NORMALIZE_LEFT - left
  # topOffset = NORMALIZE_TOP - top
  widthScale = width / NORMALIZE_WIDTH
  heightScale = height / NORMALIZE_HEIGHT

  img = cv2.imread(path)
  oHeight, oWidth = img.shape[0], img.shape[1]
  print(int(widthScale * oWidth), int(oHeight * heightScale))
  out = cv2.resize(img, (int(widthScale * oWidth), int(heightScale * oHeight)))
  
  cv2.imwrite('./temp.png', out)

  print(rect)
  # scaleWidth = width / NORMALIZE_WIDTH
  # scaleHeight = height / NORMALIZE_HEIGHT


# res = pyautogui.locateOnScreen('D:/repo/auto-suml/screenshots/start.png')
# getScale('./screenshots/start.png')
# res = pyautogui.locateOnScreen('./temp.png', confidence=0.9)
# center = pyautogui.center(res)
# pyautogui.moveTo(center)
# print(res)

battle = Auto('9-1')
battle.apply(['开始出征', '开始战斗', '单横阵', '追击?', '回港'])