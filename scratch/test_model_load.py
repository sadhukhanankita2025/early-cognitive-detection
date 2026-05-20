import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Attention, InputLayer

class FixedAttention(Attention):
    @classmethod
    def from_config(cls, config):
        if "score_mode" in config:
            if not isinstance(config["score_mode"], str):
                config["score_mode"] = "dot"
        return cls(**config)

class FixedInputLayer(InputLayer):
    @classmethod
    def from_config(cls, config):
        if "batch_shape" in config:
            config["batch_input_shape"] = config.pop("batch_shape")
        if "optional" in config:
            config.pop("optional")
        return cls(**config)

print("Attempting to load model...")
try:
    model = load_model(
        "advanced_neuroai_model.h5",
        custom_objects={
            "Attention": FixedAttention,
            "InputLayer": FixedInputLayer
        },
        compile=False
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    import traceback
    traceback.print_exc()
