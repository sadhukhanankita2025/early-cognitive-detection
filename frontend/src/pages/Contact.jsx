import React from 'react';
import { motion } from 'framer-motion';
import { Mail, Phone, MapPin, Send } from 'lucide-react';

const Contact = () => {
  return (
    <div className="pt-32 pb-20 max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-5xl font-extrabold font-manrope mb-6">Get in Touch</h1>
        <p className="text-lg text-white/60 mb-12 max-w-md">
          Have questions about our AI technology or medical methodology? Our team of specialists is here to help.
        </p>
        
        <div className="space-y-8">
          <div className="flex items-center gap-6">
            <div className="w-14 h-14 bg-soft-lavender/10 rounded-2xl flex items-center justify-center border border-soft-lavender/20">
              <Mail className="text-soft-lavender w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-white/40 mb-1">Email us at</p>
              <p className="text-lg font-bold">support@neuroai.health</p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="w-14 h-14 bg-calm-blue/10 rounded-2xl flex items-center justify-center border border-calm-blue/20">
              <Phone className="text-calm-blue w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-white/40 mb-1">Call us at</p>
              <p className="text-lg font-bold">+1 (555) 000-0000</p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="w-14 h-14 bg-mint-green/10 rounded-2xl flex items-center justify-center border border-mint-green/20">
              <MapPin className="text-mint-green w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-white/40 mb-1">Visit us</p>
              <p className="text-lg font-bold">Silicon Valley, CA, USA</p>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass-card p-10"
      >
        <form className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white/60">Full Name</label>
              <input type="text" placeholder="John Doe" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-soft-lavender transition-all" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-white/60">Email Address</label>
              <input type="email" placeholder="john@example.com" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-soft-lavender transition-all" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-white/60">Subject</label>
            <input type="text" placeholder="Inquiry about..." className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-soft-lavender transition-all" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-white/60">Message</label>
            <textarea rows="4" placeholder="How can we help you?" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-soft-lavender transition-all resize-none"></textarea>
          </div>
          <button className="w-full bg-soft-lavender hover:bg-soft-lavender/90 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-soft-lavender/20">
            Send Message <Send className="w-5 h-5" />
          </button>
        </form>
      </motion.div>
    </div>
  );
};

export default Contact;
