from random import random
from string import Template
from PIL import Image
import pyautogui
import time

START = (1367,824,1624,894)
BATTLE = (1418,816,1656,897)
CHOOSE = (908,787,1638,890)
CONTINUE = (1483,828,1653,858)
BACK = (1100,611,1273,654)
AREA = (657,229,1561,821)

COUNT = 34

# pyautogui.mouseInfo()

# im = pyautogui.screenshot()
# om = im.crop(BATTLE)
# om.save(r'D:\repo\auto-suml\screenshots\battle.png')

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
    if self.context.getPos('battle'):
      self.context.current = Battle(self.context)
      return True
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
    return pyautogui.locateOnScreen(path.safe_substitute(type=type))
  
  def randomClick(self):
    x1, y1, x2, y2 = AREA
    offsetWidth = x2 - x1
    offsetHeight = y2 - y1
    seed = random()
    pyautogui.click(x1 + seed * offsetWidth, y1 + seed * offsetHeight)

jounery = Jounery()

while True:
  time.sleep(1)
  jounery.run()
