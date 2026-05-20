import React from 'react';
import { Brain } from 'lucide-react';

const Navbar = ({ setPage }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-navy-bg/50 backdrop-blur-md border-b border-white/10 px-6 py-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => setPage('home')}>
          <Brain className="text-soft-lavender w-8 h-8" />
          <span className="text-xl font-bold font-manrope tracking-tight">NeuroAI</span>
        </div>
        <div className="flex gap-8 items-center text-sm font-medium">
          <button onClick={() => setPage('home')} className="hover:text-soft-lavender transition-colors">Home</button>
          <button onClick={() => setPage('dashboard')} className="hover:text-soft-lavender transition-colors">Analyzer</button>
          <button onClick={() => setPage('contact')} className="hover:text-soft-lavender transition-colors">Contact</button>
          <button 
            onClick={() => setPage('dashboard')}
            className="bg-soft-lavender hover:bg-soft-lavender/90 px-5 py-2 rounded-full transition-all shadow-lg shadow-soft-lavender/20"
          >
            Get Started
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
