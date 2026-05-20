import os
import tempfile
import traceback
from datetime import datetime

import librosa
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import keras

from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    make_response
)

from flask_cors import CORS

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Attention, InputLayer, Dense

from fpdf import FPDF

# =========================================================
# FIX KERAS / TENSORFLOW VERSION COMPATIBILITY
# =========================================================

original_dense_init = Dense.__init__

def fixed_dense_init(self, *args, quantization_config=None, **kwargs):
    return original_dense_init(self, *args, **kwargs)

Dense.__init__ = fixed_dense_init

try:
    keras.layers.Dense.__init__ = fixed_dense_init
except:
    pass


original_dense_from_config = Dense.from_config

def fixed_dense_from_config(cls, config):

    config = dict(config)

    config.pop("quantization_config", None)

    if hasattr(original_dense_from_config, "__func__"):
        return original_dense_from_config.__func__(cls, config)

    return original_dense_from_config(config)

Dense.from_config = classmethod(fixed_dense_from_config)

try:
    keras.layers.Dense.from_config = classmethod(
        fixed_dense_from_config
    )
except:
    pass

# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    static_folder='frontend/dist',
    static_url_path='/'
)

CORS(app)

# =========================================================
# FRONTEND SERVING
# =========================================================

@app.route('/')
def index():

    index_path = os.path.join(
        app.static_folder,
        'index.html'
    )

    if os.path.exists(index_path):
        return send_file(index_path)

    return "Frontend build not found", 404


@app.errorhandler(404)
def not_found(e):

    index_path = os.path.join(
        app.static_folder,
        'index.html'
    )

    if request.path.startswith('/api'):
        return jsonify({
            "error": "API route not found"
        }), 404

    if os.path.exists(index_path):
        return send_file(index_path)

    return "Not Found", 404

# =========================================================
# HEALTH CHECK
# =========================================================

@app.route('/health', methods=['GET'])
def health():

    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

# =========================================================
# CUSTOM KERAS CLASSES
# =========================================================

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
            config["batch_input_shape"] = config.pop(
                "batch_shape"
            )

        config.pop("optional", None)

        return cls(**config)


class FixedDense(Dense):

    @classmethod
    def from_config(cls, config):

        config.pop("quantization_config", None)

        return cls(**config)

# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = "advanced_neuroai_model.h5"

model = None

def get_model():

    global model

    if model is None:

        print("\n--- Loading Model ---")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        model = load_model(
            MODEL_PATH,
            custom_objects={
                "Attention": FixedAttention,
                "InputLayer": FixedInputLayer,
                "Dense": FixedDense
            },
            compile=False
        )

        print("--- Model Loaded Successfully ---")

    return model

# =========================================================
# FEATURE EXTRACTION
# =========================================================

def extract_features(audio_path):

    print("Loading Audio...")

    y, sr = librosa.load(
        audio_path,
        sr=22050,
        mono=True
    )

    print(f"Audio Samples: {len(y)}")

    mfccs = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=40
    )

    mfccs = mfccs.T

    max_time = 200

    if len(mfccs) > max_time:

        mfccs = mfccs[:max_time, :]

    else:

        padding = max_time - len(mfccs)

        mfccs = np.pad(
            mfccs,
            ((0, padding), (0, 0)),
            mode='constant'
        )

    return mfccs

# =========================================================
# PREDICT ROUTE
# =========================================================

@app.route('/predict', methods=['POST'])
def predict():

    print("\n--- Prediction Request ---")

    temp_audio_path = None

    try:

        # =====================================================
        # CHECK FILE
        # =====================================================

        if 'file' not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files['file']

        if file.filename == '':

            return jsonify({
                "error": "No selected file"
            }), 400

        print(f"Received File: {file.filename}")

        # =====================================================
        # VALIDATE EXTENSION
        # =====================================================

        allowed_extensions = [
            'wav',
            'mp3',
            'ogg',
            'm4a'
        ]

        ext = file.filename.split('.')[-1].lower()

        if ext not in allowed_extensions:

            return jsonify({
                "error": f"Unsupported file type: {ext}"
            }), 400

        # =====================================================
        # SAVE TEMP FILE
        # =====================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{ext}"
        ) as tmp_file:

            file.save(tmp_file.name)

            temp_audio_path = tmp_file.name

        print(f"Temp Audio: {temp_audio_path}")

        # =====================================================
        # EXTRACT FEATURES
        # =====================================================

        features = extract_features(temp_audio_path)

        features = np.expand_dims(
            features,
            axis=0
        )

        print(f"Feature Shape: {features.shape}")

        # =====================================================
        # LOAD MODEL
        # =====================================================

        m = get_model()

        # =====================================================
        # PREDICTION
        # =====================================================

        prediction = m.predict(
            features,
            verbose=0
        )

        score = float(prediction[0][0])

        result = {
            "score": score,
            "prediction": (
                "Risk Detected"
                if score >= 0.5
                else "Healthy Profile"
            ),
            "timestamp": datetime.now().isoformat()
        }

        print("Prediction Result:", result)

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        try:

            if temp_audio_path and os.path.exists(
                temp_audio_path
            ):

                os.remove(temp_audio_path)

                print("Temporary File Removed")

        except:
            pass

# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@app.route('/download-report', methods=['POST'])
def download_report():

    temp_graph_path = None

    try:

        data = request.get_json(force=True) or {}

        score = float(data.get('score', 0))
        filename = data.get(
            'filename',
            'Patient_Audio'
        )

        # =====================================================
        # CREATE PDF
        # =====================================================

        pdf = FPDF()

        pdf.set_auto_page_break(
            auto=True,
            margin=15
        )

        pdf.add_page()

        line_width = (
            pdf.w -
            pdf.l_margin -
            pdf.r_margin
        )

        # =====================================================
        # HEADER
        # =====================================================

        pdf.set_font(
            "Helvetica",
            "B",
            24
        )

        pdf.set_text_color(
            139,
            92,
            246
        )

        pdf.cell(
            line_width,
            20,
            txt="NeuroAI Clinical Report",
            ln=True,
            align='C'
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.set_text_color(
            100,
            100,
            100
        )

        pdf.cell(
            line_width,
            8,
            txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ln=True,
            align='C'
        )

        pdf.ln(10)

        # =====================================================
        # AUDIO DETAILS
        # =====================================================

        pdf.set_font(
            "Helvetica",
            "B",
            14
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.cell(
            line_width,
            10,
            txt="Audio Analysis Details",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            12
        )

        pdf.multi_cell(
            line_width,
            8,
            txt=f"Filename: {filename}"
        )

        pdf.ln(5)

        # =====================================================
        # RESULT SECTION
        # =====================================================

        pdf.set_font(
            "Helvetica",
            "B",
            14
        )

        pdf.cell(
            line_width,
            10,
            txt="AI Diagnostic Result",
            ln=True
        )

        if score >= 0.5:

            status = "RISK DETECTED"

            pdf.set_text_color(
                231,
                76,
                60
            )

        else:

            status = "HEALTHY PROFILE"

            pdf.set_text_color(
                46,
                204,
                113
            )

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            line_width,
            12,
            txt=status,
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            12
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.cell(
            line_width,
            8,
            txt=f"Confidence Score: {score * 100:.2f}%",
            ln=True
        )

        pdf.ln(10)

        # =====================================================
        # CREATE GRAPH
        # =====================================================

        categories = ['Healthy', 'Risk']

        values = [
            (1 - score) * 100,
            score * 100
        ]

        colors = ['green', 'red']

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.png'
        ) as tmp_graph:

            temp_graph_path = tmp_graph.name

        plt.figure(figsize=(6, 4))

        plt.barh(
            categories,
            values,
            color=colors
        )

        plt.xlim(0, 100)

        plt.xlabel("Probability (%)")

        plt.title(
            "AI Prediction Distribution"
        )

        plt.tight_layout()

        plt.savefig(
            temp_graph_path,
            dpi=150,
            bbox_inches='tight'
        )

        plt.close()

        if (
            temp_graph_path and
            os.path.exists(temp_graph_path)
        ):

            pdf.image(
                temp_graph_path,
                x=25,
                w=160
            )

        pdf.ln(10)

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        pdf.set_font(
            "Helvetica",
            "B",
            14
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.cell(
            line_width,
            10,
            txt="Recommendations",
            ln=True
        )

        pdf.set_font(
            "Helvetica",
            "",
            12
        )

        if score >= 0.5:

            recommendations = [
                "Immediate medical consultation recommended.",
                "Clinical cognitive assessment advised.",
                "Lifestyle and neurological evaluation needed.",
                "Maintain regular monitoring."
            ]

        else:

            recommendations = [
                "Maintain a healthy lifestyle.",
                "Continue regular exercise.",
                "Routine health monitoring recommended."
            ]

        for rec in recommendations:

            pdf.multi_cell(
                line_width,
                8,
                txt=f"- {rec}"
            )

        pdf.ln(5)

        # =====================================================
        # DISCLAIMER
        # =====================================================

        pdf.set_font(
            "Helvetica",
            "I",
            9
        )

        pdf.set_text_color(
            150,
            150,
            150
        )

        pdf.multi_cell(
            line_width,
            5,
            txt=(
                "Medical Disclaimer: "
                "This report is AI-generated and "
                "is NOT a medical diagnosis. "
                "Please consult a qualified "
                "healthcare professional."
            )
        )

        # =====================================================
        # GENERATE PDF
        # =====================================================

        pdf_bytes = bytes(
            pdf.output(dest='S')
        )

        print("PDF Generated Successfully")

        response = make_response(
            pdf_bytes
        )

        response.headers.set(
            "Content-Type",
            "application/pdf"
        )

        response.headers.set(
            "Content-Disposition",
            'attachment; filename="NeuroAI_Report.pdf"'
        )

        return response

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        try:

            if (
                temp_graph_path and
                os.path.exists(temp_graph_path)
            ):

                os.remove(temp_graph_path)

                print("Temporary Graph Removed")

        except:
            pass

# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':

    print("\n--- Starting NeuroAI Flask Server ---")

    try:

        get_model()

    except Exception as e:

        print(
            f"WARNING: Model preload failed: {e}"
        )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )