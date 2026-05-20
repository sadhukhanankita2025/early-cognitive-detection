import streamlit as st
import numpy as np
import librosa
import tempfile
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Attention

print("All imports from app.py successful!")
print(f"NumPy version: {np.__version__}")
print(f"TensorFlow version: {tf.__version__}")
