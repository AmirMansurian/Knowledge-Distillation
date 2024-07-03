"""Base Model for Semantic Segmentation"""
import torch.nn as nn
from .base_models.resnet import *

__all__ = ['SegBaseModel']


class SegBaseModel(nn.Module):
    r"""Base Model for Semantic Segmentation

    Parameters
    ----------
    backbone : string
        Pre-trained dilated backbone network type (default:'resnet50'; 'resnet50',
        'resnet101' or 'resnet152').
    """

    def __init__(self, nclass, aux, backbone='resnet50', local_rank=None, pretrained_base=True, **kwargs):
        super(SegBaseModel, self).__init__()
        self.aux = aux
        self.nclass = nclass
        if backbone == 'resnet18':
            self.pretrained = resnet18(pretrained=pretrained_base, dilated=True, local_rank=local_rank, **kwargs)
        elif backbone == 'resnet50':
            self.pretrained = resnet50(pretrained=pretrained_base, local_rank=local_rank, dilated=True, **kwargs)
        elif backbone == 'resnet101':
            self.pretrained = resnet101(pretrained=pretrained_base, local_rank=local_rank, dilated=True, **kwargs)
        else:
            raise RuntimeError('unknown backbone: {}'.format(backbone))

    def base_forward(self, x):
        """forwarding pre-trained network"""
        '''
        x = self.pretrained.conv1(x)
        x = self.pretrained.bn1(x)
        x = self.pretrained.relu(x)
        x = self.pretrained.maxpool(x)
        '''
        
        x = self.pretrained.conv1(x)
        x = self.pretrained.bn1(x)
        x = self.pretrained.relu1(x)

        x = self.pretrained.conv2(x)
        x = self.pretrained.bn2(x)
        x = self.pretrained.relu2(x)

        x = self.pretrained.conv3(x)
        x = self.pretrained.bn3(x)
        x = self.pretrained.relu3(x)
        x = self.pretrained.maxpool(x)
        
        c1 = self.pretrained.layer1(x)
        c2 = self.pretrained.layer2(c1)
        c3 = self.pretrained.layer3(c2)
        c4 = self.pretrained.layer4(c3)

        return c1, c2, c3, c4

    def evaluate(self, x):
        """evaluating network with inputs and targets"""
        return self.forward(x)[0]

    def demo(self, x):
        pred = self.forward(x)
        if self.aux:
            pred = pred[0]
        return pred
