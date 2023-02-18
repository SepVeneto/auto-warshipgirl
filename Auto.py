import utils
import cv2
import os

class Auto:
  def __init__(self, stage) -> None:
    self.NORMALIZE_LEFT = utils.config.get('basic', 'left')
    self.NORMALIZE_TOP = utils.config.get('basic', 'top')
    self.NORMALIZE_WIDTH = utils.config.get('basic', 'width')
    self.NORMALIZE_HEIGHT = utils.config.get('basic', 'height')
    self.stage = stage
    self.steps = utils.config.get('stage', stage)

  def resize(self):
    left, top, right, bottom = utils.getWindowSize()
    width = right - left
    height = bottom - top
    self.widthScale = width / self.NORMALIZE_WIDTH
    self.heightScale = height / self.NORMALIZE_HEIGHT

  def mockTemp(self):
    if not os.path.exists('__temp__'):
      os.makedirs('__temp__')
    images = os.listdir('screenshots/common')
    conditions = os.listdir(f'screeshots/{self.stage}')
    
  def resizeImg(self, path):
    img = cv2.imread(path)
    oHeight, oWidth = img.shape[0], img.shape[1]
    print(int(self.widthScale * oWidth), int(oHeight * self.heightScale))
    out = cv2.resize(img, (int(self.widthScale * oWidth), int(self.heightScale * oHeight)))
    cv2.imwrite('./temp.png', out)
