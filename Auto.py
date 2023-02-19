from random import random
from PIL import Image
import utils
import time
import cv2
import os
import numpy as np
import pyautogui

class Auto:
  def __init__(self, stage) -> None:
    self.NORMALIZE_LEFT = (utils.config.get('basic')['left'])
    self.NORMALIZE_TOP = (utils.config.get('basic')['top'])
    self.NORMALIZE_WIDTH = (utils.config.get('basic')['width'])
    self.NORMALIZE_HEIGHT = (utils.config.get('basic')['height'])
    self.stage = stage[0]
    self.steps = utils.config.get('stage')[self.stage]

    self.resize()
    # TODO 自动创建
    self.mockTemp('__temp__')
    self.travseDir('./screenshots')

  def resize(self):
    left, top, right, bottom = utils.getWindowSize()
    width = right - left
    height = bottom - top
    self.widthScale = width / self.NORMALIZE_WIDTH
    self.heightScale = height / self.NORMALIZE_HEIGHT
    self.offsetX = self.NORMALIZE_LEFT - left
    self.offsetY = self.NORMALIZE_TOP - top

    self.area = tuple(utils.config.get('basic')['random'])

  def mockTemp(self, path):
    if not os.path.exists(path):
      os.makedirs(path)
  
  def travseDir(self, dir):
    list = os.listdir(dir)
    for item in list:
      path = os.path.join(dir, item)
      if os.path.isdir(path):
        self.travseDir(path)
      else:
        self.resizeImg(path, item)
    
  def resizeImg(self, path: str, name: str):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    oHeight, oWidth = img.shape[0], img.shape[1]
    out = cv2.resize(img, (int(self.widthScale * oWidth), int(self.heightScale * oHeight)))

    # savePath = path.replace('screenshots', '__temp__')
    cv2.imencode('.png', out)[1].tofile(os.path.join('__temp__', name))

  def run(self):
    for step in self.steps:
      if step == '-':
        self.random()
      else:
        self.action(step)

  def action(self, path):
    print(path)
    rect = self.getPos(path)
    print(path, rect)
    if rect == None:
      return None
    center = pyautogui.center(rect)
    pyautogui.click(center)
    time.sleep(1)
  
  def getPos(self, path: str):
    operate = []
    if '?' in path:
      operate.append('?')
      path = path.replace('?', '')
    if '!' in path:
      operate.append('!')
      path = path.replace('!', '')
    while True:
      imgPath = os.path.join('./__temp__', path + '.png')
      # img = cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8), -1)
      res = pyautogui.locateOnScreen(Image.open(imgPath))
      # res = pyautogui.locateOnScreen(r'D:\repo\auto-suml\__temp__\common\开始出征.png')
      print(path, res, operate)
      if res != None:
        if '!' in operate:
          print('enter')
          self.action('放弃')
          return None
        return res
      elif '?' in operate or '!' in operate:
        return None
      else:
        time.sleep(0.5)
  
  def random(self):
    x1, y1, x2, y2 = self.area
    offsetWidth = (x2 - x1) * self.widthScale
    offsetHeight = (y2 - y1) * self.heightScale
    seed = random()

    clickX = x1 + seed * offsetWidth + self.offsetX
    clickY = y1 + seed * offsetHeight + self.offsetY
    pyautogui.click((clickX, clickY))