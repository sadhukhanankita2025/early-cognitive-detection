import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Activity, FileText, ArrowRight, ShieldCheck, Lock, Search } from 'lucide-react';
import brainHologram from '../assets/brain_hologram.png';

const LandingPage = ({ setPage }) => {
  return (
    <div className="pt-24 pb-20">
      {/* Background Blobs */}
      <div className="blob top-[-200px] left-[-200px]" />
      <div className="blob bottom-[-200px] right-[-200px] opacity-50" />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl lg:text-7xl font-extrabold font-manrope leading-[1.1] mb-6">
            AI-Powered Early <br />
            <span className="gradient-text">Cognitive Health</span> <br />
            Screening
          </h1>
          <p className="text-lg text-white/70 mb-8 max-w-xl font-poppins leading-relaxed">
            Upload a short voice recording and receive intelligent neurological insights in seconds. 
            Our advanced AI detects subtle patterns in speech associated with early cognitive decline.
          </p>
          <div className="flex gap-4 mb-12">
            <button 
              onClick={() => setPage('dashboard')}
              className="group bg-soft-lavender px-8 py-4 rounded-full font-bold flex items-center gap-2 hover:scale-105 transition-all shadow-xl shadow-soft-lavender/30"
            >
              Start Analysis <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="px-8 py-4 rounded-full border border-white/20 font-bold hover:bg-white/5 transition-all">
              Learn More
            </button>
          </div>
          
          <div className="flex gap-12 border-t border-white/10 pt-8">
            <div>
              <p className="text-3xl font-bold font-manrope tracking-tighter">96.8%</p>
              <p className="text-sm text-white/50">Accuracy</p>
            </div>
            <div>
              <p className="text-3xl font-bold font-manrope tracking-tighter">&lt;5s</p>
              <p className="text-sm text-white/50">Analysis Time</p>
            </div>
            <div>
              <p className="text-3xl font-bold font-manrope tracking-tighter">15K+</p>
              <p className="text-sm text-white/50">Samples Trained</p>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1 }}
          className="relative"
        >
          <img 
            src={brainHologram} 
            alt="Brain Hologram" 
            className="w-full h-auto floating neural-glow"
          />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-soft-lavender/20 blur-[100px] -z-10 rounded-full animate-pulse" />
        </motion.div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 mt-32">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold font-manrope mb-4">Intelligent Features</h2>
          <p className="text-white/50">Modern tools designed for neurological health.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { icon: Activity, title: "Voice-Based Detection", desc: "Analyzing acoustic features and speech patterns." },
            { icon: Brain, title: "AI Cognitive Analysis", desc: "Deep learning models trained on clinical datasets." },
            { icon: FileText, title: "PDF Clinical Report", desc: "Downloadable professional reports for medical consultation." }
          ].map((feature, i) => (
            <motion.div 
              key={i}
              whileHover={{ y: -10 }}
              className="glass-card p-8 group hover:border-soft-lavender/50 transition-all"
            >
              <div className="bg-soft-lavender/10 w-16 h-16 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <feature.icon className="text-soft-lavender w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
              <p className="text-white/60 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Trust Section */}
      <section className="max-w-7xl mx-auto px-6 mt-40 mb-20">
        <div className="glass-card p-12 bg-gradient-to-br from-white/5 to-soft-lavender/10 border-soft-lavender/20 flex flex-col md:flex-row items-center gap-12">
          <div className="flex-1 text-center md:text-left">
            <h2 className="text-4xl font-bold mb-6">Built on Trust & Security</h2>
            <div className="space-y-6">
              {[
                { icon: ShieldCheck, text: "HIPAA-compliant data processing" },
                { icon: Lock, text: "End-to-end encryption for voice data" },
                { icon: Search, text: "Research-backed AI methodology" }
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 justify-center md:justify-start">
                  <div className="bg-mint-green/20 p-2 rounded-full">
                    <item.icon className="text-mint-green w-5 h-5" />
                  </div>
                  <span className="text-lg text-white/80">{item.text}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white/10 p-8 rounded-[32px] backdrop-blur-3xl border border-white/20 max-w-sm w-full">
             <h3 className="text-2xl font-bold mb-4 text-center">Ready to check?</h3>
             <p className="text-center text-white/60 mb-8">It takes less than a minute to get your first diagnostic insight.</p>
             <button 
                onClick={() => setPage('dashboard')}
                className="w-full bg-white text-navy-bg py-4 rounded-full font-bold hover:bg-white/90 transition-all"
             >
                Launch Analyzer
             </button>
          </div>
        </div>
      </section>
      
      {/* Footer Disclaimer */}
      <footer className="text-center text-white/30 text-xs px-6 py-10 border-t border-white/5">
        <p className="max-w-2xl mx-auto">
          Medical Disclaimer: This tool is intended for screening support only and not as a definitive medical diagnosis. 
          Please consult with a qualified healthcare professional for a complete evaluation.
        </p>
      </footer>
    </div>
  );
};

export default LandingPage;
