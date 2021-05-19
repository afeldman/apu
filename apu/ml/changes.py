""" change the default setting of a layer in runtime """
from apu.ast.keyword_mapping import get_pos_to_keyword_map


def change_default_args(**kwargs):
    # https://github.com/traveller59/torchplus/blob/master/tools.py
    def layer_wrapper(layer):
        class DefaultArgumentLayer(layer):
            def __init__(self, *args, **kwa) -> None:
                # get the position of the constructor of layerclass
                pos2keyword = get_pos_to_keyword_map(layer.__init__)
                keyword2pos = {
                    keyword: pos
                    for pos, keyword in pos2keyword.items()
                }
                for key, value in kwargs.items():
                    if key not in kwa and keyword2pos[key] > len(args):
                        # set new value for the parameter
                        kwa.update({key: value})
                super().__init__()

        return DefaultArgumentLayer

    return layer_wrapper
