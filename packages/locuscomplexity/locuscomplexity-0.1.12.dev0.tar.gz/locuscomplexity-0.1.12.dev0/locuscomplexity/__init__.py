import locuscomplexity.fitness, locuscomplexity.complexity, locuscomplexity.color_code
import os

__all__ = ["color_code", "fitness", "complexity"]


_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, path)

print (get_data('data/dict_colors.pkl'))