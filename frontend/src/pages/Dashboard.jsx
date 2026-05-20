import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileAudio, CheckCircle, AlertTriangle, FileDown, RotateCcw, Brain, Activity, Heart, Info } from 'lucide-react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell, Tooltip } from 'recharts';

const API_BASE = '';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResult(null);
      setError(null);
    }
  };

  const startAnalysis = async () => {
    if (!file) return;
    setAnalyzing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/predict`, formData);
      setResult(response.data);
    } catch (err) {
      console.error("Analysis Error:", err);
      setError(err.response?.data?.error || "Failed to analyze audio. Check your connection to the Flask server.");
    } finally {
      setAnalyzing(false);
    }
  };

  const downloadReport = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/download-report",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            score: result.score,
            filename: file.name,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to download PDF");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "NeuroAI_Report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();

    } catch (error) {
      console.error(error);
      alert("Failed to download PDF");
    }
  };

  const reset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  const chartData = result ? [
    { name: 'Healthy (Negative)', value: (1 - result.score) * 100 },
    { name: 'Risk (Positive)', value: result.score * 100 }
  ] : [];

  return (
    <div className="pt-32 pb-20 max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="lg:col-span-12 bg-red-500/20 border border-red-500/50 text-red-200 p-4 rounded-2xl flex items-center gap-3 mb-4"
          >
            <AlertTriangle className="w-5 h-5" />
            <span>{error}</span>
            <button onClick={() => setError(null)} className="ml-auto hover:text-white">✕</button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Left Panel: Upload */}
      <div className="lg:col-span-4 space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-8"
        >
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Upload className="text-soft-lavender w-6 h-6" /> Upload Audio
          </h2>

          <div
            onClick={() => fileInputRef.current.click()}
            className={`border-2 border-dashed rounded-[20px] p-10 text-center cursor-pointer transition-all ${file ? 'border-mint-green/50 bg-mint-green/5' : 'border-white/10 hover:border-soft-lavender/50 hover:bg-white/5'}`}
          >
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="audio/*" />
            <FileAudio className={`w-12 h-12 mx-auto mb-4 ${file ? 'text-mint-green' : 'text-white/20'}`} />
            {file ? (
              <div>
                <p className="font-bold text-mint-green truncate mb-1">{file.name}</p>
                <p className="text-xs text-white/40">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
              </div>
            ) : (
              <div>
                <p className="font-bold mb-1">Drag & Drop or Browse</p>
                <p className="text-xs text-white/40">WAV, MP3, OGG supported</p>
              </div>
            )}
          </div>

          <button
            disabled={!file || analyzing}
            onClick={startAnalysis}
            className={`w-full mt-6 py-4 rounded-full font-bold transition-all shadow-xl ${!file || analyzing ? 'bg-white/5 text-white/20 cursor-not-allowed' : 'bg-soft-lavender hover:bg-soft-lavender/90 shadow-soft-lavender/30'}`}
          >
            {analyzing ? 'Processing Analysis...' : 'Start AI Prediction'}
          </button>

          {file && !analyzing && (
            <button onClick={reset} className="w-full mt-4 py-2 text-sm text-white/40 hover:text-white flex items-center justify-center gap-2 transition-colors">
              <RotateCcw className="w-4 h-4" /> Reset
            </button>
          )}
        </motion.div>

        <div className="glass-card p-6 bg-soft-lavender/5 border-soft-lavender/20">
          <h3 className="font-bold mb-2 flex items-center gap-2"><Info className="w-4 h-4" /> Why Voice?</h3>
          <p className="text-sm text-white/60 leading-relaxed">
            Speech patterns are highly sensitive to neurological health. Our AI analyzes pitch variance, pause frequency, and phonetic precision to detect early markers.
          </p>
        </div>
      </div>

      {/* Center Panel: Results */}
      <div className="lg:col-span-8 space-y-6">
        <AnimatePresence mode="wait">
          {!result && !analyzing ? (
            <motion.div
              key="placeholder"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="glass-card h-full flex flex-col items-center justify-center text-center p-20 border-white/5"
            >
              <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center mb-8">
                <Brain className="text-white/20 w-12 h-12" />
              </div>
              <h2 className="text-2xl font-bold mb-4 opacity-50">Awaiting Data</h2>
              <p className="max-w-xs text-white/30">Upload an audio recording on the left to begin the neurological assessment.</p>
            </motion.div>
          ) : analyzing ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="glass-card h-full flex flex-col items-center justify-center text-center p-20"
            >
              <div className="relative mb-12">
                <div className="w-32 h-32 border-4 border-soft-lavender/20 rounded-full animate-ping" />
                <div className="absolute inset-0 w-32 h-32 border-4 border-t-soft-lavender border-transparent rounded-full animate-spin" />
                <Brain className="absolute inset-0 m-auto text-soft-lavender w-12 h-12 floating" />
              </div>
              <h2 className="text-2xl font-bold mb-4">Analyzing Neural Patterns</h2>
              <p className="text-white/50">Processing acoustic features and comparing with clinical data...</p>
            </motion.div>
          ) : (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
              className="space-y-6"
            >
              {/* Result Card */}
              <div className={`glass-card p-10 relative overflow-hidden ${result.score >= 0.5 ? 'border-red-500/30' : 'border-mint-green/30'}`}>
                <div className={`absolute top-0 right-0 w-64 h-64 blur-[100px] -z-10 ${result.score >= 0.5 ? 'bg-red-500/10' : 'bg-mint-green/10'}`} />

                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
                  <div>
                    <span className={`px-4 py-1 rounded-full text-xs font-bold tracking-widest uppercase mb-4 inline-block ${result.score >= 0.5 ? 'bg-red-500/20 text-red-400' : 'bg-mint-green/20 text-mint-green'}`}>
                      {result.score >= 0.5 ? 'Risk Detected' : 'Healthy Profile'}
                    </span>
                    <h2 className="text-4xl font-extrabold font-manrope mb-2">
                      {result.score >= 0.5 ? 'Possible Cognitive Decline' : 'No Significant Decline'}
                    </h2>
                    <p className="text-white/60 mb-6">Prediction Score: {(result.score * 100).toFixed(2)}% Confidence</p>

                    <button
                      onClick={downloadReport}
                      className="bg-white/10 hover:bg-white/20 px-6 py-3 rounded-full font-bold flex items-center gap-2 transition-all border border-white/10"
                    >
                      <FileDown className="w-5 h-5" /> Download Clinical PDF
                    </button>
                  </div>

                  <div className="w-full md:w-64 h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} layout="vertical">
                        <XAxis type="number" hide domain={[0, 100]} />
                        <YAxis dataKey="name" type="category" hide />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#071028', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                          itemStyle={{ color: '#fff' }}
                        />
                        <Bar dataKey="value" radius={[0, 10, 10, 0]} barSize={30}>
                          {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={index === 0 ? '#34D399' : '#e74c3c'} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Recommendations Section */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-card p-8">
                  <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                    <Activity className="text-soft-lavender w-6 h-6" /> AI Insights
                  </h3>
                  <div className="space-y-4">
                    <div className="bg-white/5 p-4 rounded-2xl">
                      <p className="text-xs text-white/40 mb-1">Risk Assessment</p>
                      <p className="font-medium">{result.score >= 0.7 ? 'High Risk detected in speech variance' : result.score >= 0.5 ? 'Moderate markers identified' : 'All parameters within normal range'}</p>
                    </div>
                    <div className="bg-white/5 p-4 rounded-2xl">
                      <p className="text-xs text-white/40 mb-1">Phonetic Integrity</p>
                      <p className="font-medium">{result.score >= 0.5 ? 'Slight reduction in acoustic density' : 'Speech patterns show high phonetic clarity'}</p>
                    </div>
                  </div>
                </div>

                <div className="glass-card p-8">
                  <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                    <Heart className="text-mint-green w-6 h-6" /> Recommendations
                  </h3>
                  <div className="space-y-4 text-sm leading-relaxed text-white/70">
                    {result.score >= 0.5 ? (
                      <ul className="space-y-3">
                        <li className="flex items-start gap-2">
                          <AlertTriangle className="text-red-400 w-4 h-4 shrink-0 mt-0.5" />
                          <span>Schedule a consultation with a neurologist for a formal assessment.</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="text-mint-green w-4 h-4 shrink-0 mt-0.5" />
                          <span>Start daily cognitive exercises like puzzles or memory games.</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="text-mint-green w-4 h-4 shrink-0 mt-0.5" />
                          <span>Focus on a nutrient-rich MIND diet for brain health.</span>
                        </li>
                      </ul>
                    ) : (
                      <ul className="space-y-3">
                        <li className="flex items-start gap-2">
                          <CheckCircle className="text-mint-green w-4 h-4 shrink-0 mt-0.5" />
                          <span>Maintain your current active and healthy lifestyle.</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="text-mint-green w-4 h-4 shrink-0 mt-0.5" />
                          <span>Engage in regular social activities and learning.</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="text-mint-green w-4 h-4 shrink-0 mt-0.5" />
                          <span>Monitor your health with annual neurological check-ups.</span>
                        </li>
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Dashboard;
