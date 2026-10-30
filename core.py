"""Quy ước dùng chung; thuật toán từng bài nằm trực tiếp trong pages/*.py."""
from pathlib import Path
import numpy as np
import colour
import matplotlib
matplotlib.use('Agg')

ROOT = Path(__file__).resolve().parent
CMFS = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']

def white(name='D65'):
    return colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][name]

def display_rgb(xyz):
    return np.clip(colour.XYZ_to_sRGB(xyz), 0, 1)
