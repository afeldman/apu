import math

from torch.nn.init import _calculate_fan_in_and_fan_out,
                          _no_grad_normal_,
                          _no_grad_uniform_,
                          xavier_uniform,
                          xavier_normal


def he_uniform_(tensor, gain=1., mode="fan_in"):
    # type: (Tensor, float, str) -> Tensor
    r"""
    """
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)

    if mode == "fan_out":
        std = gain * math.sqrt(2.0 / float(fan_out))
    else:
        std = gain * math.sqrt(2.0 / float(fan_in))

    a = math.sqrt(3.0) * std

    return _no_grad_uniform_(tensor, -a, a)


def he_normal_(tensor, gain=1., mode="fan_in"):
    # type: (Tensor, float, str) -> Tensor
    r"""
    """
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)

    if mode == "fan_out":
        std = gain * math.sqrt(2.0 / float(fan_out))
    else:
        std = gain * math.sqrt(2.0 / float(fan_in))

    return _no_grad_normal_(tensor, 0., std)

he_nromal = he_normal_
he_uniform = he_uniform_
glorot_normal = xavier_uniform
glorot_unified = xavier_normal