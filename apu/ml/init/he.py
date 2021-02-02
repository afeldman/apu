"""
implementation of he initializer for pytorch

author: anton feldmann <anton.feldmann@gmail.com>
"""
import math

from torch.nn.init import (kaiming_normal_, kaiming_uniform_)

he_normal = kaiming_normal_
he_uniform = kaiming_uniform_
