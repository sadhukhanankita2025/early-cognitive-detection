import os
import numpy as np
import librosa
import tempfile
import tensorflow as tf
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Attention, InputLayer
from fpdf import FPDF
from datetime import datetime
import traceback
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
import io

app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')

# Robust CORS for development and production
CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------------------
# Serve Frontend
# -----------------------------------
@app.route('/')
def index():
    dist_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(dist_path):
        return send_file(dist_path)
    return "Frontend build not found. Please run 'npm run build' in the frontend folder.", 404

@app.errorhandler(404)
def not_found(e):
    dist_path = os.path.join(app.static_folder, 'index.html')
    if request.path.startswith('/api'):
        return jsonify({"error": "API route not found"}), 404
    if os.path.exists(dist_path):
        return send_file(dist_path)
    return "Not Found", 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

# -----------------------------------
# Monkey Patch Layers for Keras Compatibility
# -----------------------------------
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

# -----------------------------------
# Load Model
# -----------------------------------
MODEL_PATH = "advanced_neuroai_model.h5"
model = None

def get_model():
    global model
    if model is None:
        print(f"--- Loading Model from {MODEL_PATH} ---")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        model = load_model(
            MODEL_PATH,
            custom_objects={
                "Attention": FixedAttention,
                "InputLayer": FixedInputLayer
            },
            compile=False
        )
        print("--- Model Loaded Successfully ---")
    return model

# -----------------------------------
# Feature Extraction
# -----------------------------------
def extract_features(audio_path):
    # Use sr=None to keep native sampling rate
    y, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs = mfccs.T
    
    # Standardize to 200 time steps
    max_time = 200
    if len(mfccs) > max_time:
        mfccs = mfccs[:max_time, :]
    else:
        padding = max_time - len(mfccs)
        mfccs = np.pad(mfccs, ((0, padding), (0, 0)), mode='constant')
    return mfccs

# -----------------------------------
# API Endpoints
# -----------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    print("\n--- Incoming Prediction Request ---")
    if 'file' not in request.files:
        print("Error: No file part in request.files")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        print("Error: Empty filename")
        return jsonify({"error": "No file selected"}), 400

    temp_audio_path = None
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            file.save(tmp_file.name)
            temp_audio_path = tmp_file.name
            print(f"Temporary file created: {temp_audio_path}")

        print("Extracting features...")
        features = extract_features(temp_audio_path)
        features = np.expand_dims(features, axis=0)
        print(f"Input features shape: {features.shape}")
        
        print("Getting model instance...")
        m = get_model()
        
        print("Executing prediction...")
        prediction = m.predict(features, verbose=0)
        score = float(prediction[0][0])
        print(f"Prediction result: {score:.4f}")
        
        return jsonify({
            "score": score,
            "prediction": "Risk Detected" if score >= 0.5 else "Healthy Profile",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"CRITICAL ERROR in /predict: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                print("Temporary file cleaned up.")
            except:
                pass

@app.route('/download-report', methods=['POST'])
def download_report():
    try:
        data = request.json
        score = data.get('score', 0)
        prediction = data.get('prediction', 'Unknown')
        filename = data.get('filename', 'Patient_Audio')
        
        pdf = FPDF()
        pdf.add_page()
        
        # Header Styling
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(139, 92, 246) # Soft Lavender
        pdf.cell(200, 20, txt="NeuroAI Clinical Report", ln=True, align='C')
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(10)
        
        # Section 1: Information
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt="1. Audio Analysis Details", ln=True)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(200, 10, txt=f"Source Filename: {filename}", ln=True)
        pdf.ln(5)
        
        # Section 2: Result
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(200, 10, txt="2. AI Diagnostic Result", ln=True)
        pdf.set_font("Helvetica", "B", 18)
        if score >= 0.5:
            pdf.set_text_color(231, 76, 60) # Red
            status_text = "RISK DETECTED"
        else:
            pdf.set_text_color(46, 204, 113) # Green
            status_text = "HEALTHY PROFILE"
        
        pdf.cell(200, 15, txt=f"STATUS: {status_text}", ln=True)
        
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"Prediction Confidence: {score*100:.2f}%", ln=True)
        pdf.ln(5)

        # --- ADD GRAPH TO PDF ---
        plt.figure(figsize=(6, 4))
        categories = ['Healthy (Negative)', 'Risk (Positive)']
        values = [(1 - score) * 100, score * 100]
        colors = ['#2ecc71', '#e74c3c']
        
        plt.barh(categories, values, color=colors)
        plt.xlabel('Probability (%)')
        plt.title('AI Diagnostic Probability Distribution')
        plt.xlim(0, 100)
        plt.tight_layout()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            plt.savefig(tmp_img.name)
            plt.close()
            pdf.image(tmp_img.name, x=40, w=130)
            os.remove(tmp_img.name)
        
        pdf.ln(10)
        
        # Section 3: Recommendations
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(200, 10, txt="3. Recommended Next Steps", ln=True)
        pdf.set_font("Helvetica", "", 12)
        if score >= 0.5:
            recommendations = [
                "• Immediate clinical consultation with a neurologist.",
                "• Formal cognitive screening (MMSE or MoCA assessment).",
                "• Comprehensive blood panel for metabolic screening.",
                "• High-intensity cognitive training and aerobic exercise.",
                "• Adherence to the MIND diet protocols."
            ]
        else:
            recommendations = [
                "• Maintain current cognitive and social engagement.",
                "• Continue regular cardiovascular physical activity.",
                "• Routine annual cognitive screenings.",
                "• Balanced nutritional intake for brain health."
            ]
        
        for rec in recommendations:
            pdf.multi_cell(0, 10, txt=rec)
        
        pdf.ln(20)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 5, txt="Medical Disclaimer: This report is generated by the NeuroAI screening tool and is intended for screening support only. It does NOT constitute a clinical diagnosis. Please share this report with a qualified healthcare professional.")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf.output(tmp_pdf.name)
            return send_file(tmp_pdf.name, as_attachment=True, download_name="NeuroAI_Report.pdf")
            
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({"error": "Failed to generate report"}), 500

if __name__ == '__main__':
    print("\n--- Starting NeuroAI Flask Server ---")
    try:
        get_model() # Pre-load model
    except Exception as e:
        print(f"WARNING: Model could not be pre-loaded: {e}")
    
    app.run(port=5000, debug=True, use_reloader=False)