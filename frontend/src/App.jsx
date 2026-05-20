import React, { useState } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import Contact from './pages/Contact';

function App() {
  const [page, setPage] = useState('home');

  return (
    <div className="min-h-screen">
      <Navbar setPage={setPage} />
      
      {page === 'home' && <LandingPage setPage={setPage} />}
      {page === 'dashboard' && <Dashboard />}
      {page === 'contact' && <Contact />}
      
      {/* Background Neural Particles Simulation (Simplified) */}
      <div className="fixed inset-0 -z-20 overflow-hidden pointer-events-none opacity-20">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i}
            className="absolute rounded-full bg-soft-lavender blur-xl animate-pulse"
            style={{
              width: Math.random() * 300 + 100,
              height: Math.random() * 300 + 100,
              top: Math.random() * 100 + '%',
              left: Math.random() * 100 + '%',
              animationDuration: Math.random() * 5 + 5 + 's',
              animationDelay: Math.random() * 5 + 's',
            }}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
