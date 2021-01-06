import torch

def to_polar(x, y):
  return (x**2 + y**2).sqrt(), torch.atan(y/x)

def to_cart(radius, theta, comp=False):

  x_rot = radius * torch.cos(theta)
  y_rot = radius * torch.sin(theta)

  if comp:
    return torch.complex(x_rot, y_rot), _
  else:
    return x_rot, y_rot
