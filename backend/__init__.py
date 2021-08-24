import os, sys

BACKEND = os.path.dirname(os.path.realpath(__file__))
PROJ_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")
)
# sys.path hack to make mynode work without setting PYTHONPATH
sys.path.insert(1, BACKEND)
from scripts import index
