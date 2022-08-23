import torch
import os, sys
root = os.path.dirname(os.path.dirname(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
from tool.darknet2pytorch import Darknet
from cfg import Cfg
from train import get_args

cfg = get_args(**Cfg)
model = Darknet(cfg.cfgfile, inference=False)

model.load_state_dict(torch.load(os.path.join(root, "checkpoints/Yolov4_epoch20.pth"), 
    map_location=torch.device('cuda'))) # for loading model on cpu

model.save_weights(os.path.join(root, 'test.weights'), cutoff=0)
print("successfully converted .pth to .weights")