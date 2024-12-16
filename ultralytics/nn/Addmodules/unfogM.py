import cv2
import torch
import torch.nn as nn
import math

import torchvision
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms
#import sys
#sys.path.append('ultralytics/nn/Addmodules/unfogM.py')
import Unfog

import numpy as np
from torchvision import transforms
from PIL import Image
import glob

class unfog_M(nn.Module):



    def __init__(self):
        super(Unfog.unfog_net, self).__init__()



    def forward(self, x):


        dehaze_net = Unfog.unfog_net.cuda()
        dehaze_net.load_state_dict(torch.load('snapshots/dehazer.pthEpoch9.pth'))
        clean_image= dehaze_net(x)
        torchvision.utils.save_image(torch.cat((x, clean_image), 0), 'E:/yyj_file/ultralytics-main/runscode/2.png')





        return clean_image



