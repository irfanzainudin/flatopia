import { useState, useEffect, useRef } from 'react';
import FlatEarthSocietyLogo from '/flat_earth_society.png';
import { Plus, Globe, Mic, Send } from "lucide-react";
import { langOptions, langData } from './constants';

export default function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [currentLang, setCurrentLang] = useState("en");
  const [recommendations, setRecommendations] = useState(langData[currentLang].recommendations);
  const canvasRef = useRef(null);

  // Update recommendations when language changes
  useEffect(() => {
    setRecommendations(langData[currentLang].recommendations);
  }, [currentLang]);

  // Handle sending message
  const handleSend = () => {
    if (!message.trim()) return;
    setChatHistory(prev => [...prev, { role: "user", text: message }]);
    const userMessage = message;
    setMessage("");

    // Simulate AI response
    setTimeout(() => {
      const aiReply = currentLang === "en"
        ? `🤖 Flatopia says: Here's a fun response to: ${userMessage}`
        : `🤖 Flatopia说: 这是对你的消息的有趣回复: ${userMessage}`;
      setChatHistory(prev => [...prev, { role: "bot", text: aiReply }]);
    }, 1200);
  };

  // Floating Flatopia canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Bubble {
      constructor(){
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random()-0.5)*0.5;
        this.vy = (Math.random()-0.5)*0.5;
        this.fontSize = 20 + Math.random()*40;
        this.angle = Math.random()*360;
        this.angleSpeed = (Math.random()-0.5)*0.02;
      }
      draw(){
        ctx.save();
        ctx.translate(this.x,this.y);
        ctx.rotate(this.angle);
        ctx.font = `${this.fontSize}px Comic Neue`;
        ctx.fillStyle = "rgba(255,255,255,0.15)";
        ctx.fillText("Flatopia",0,0);
        ctx.restore();
      }
      update(){
        this.x += this.vx;
        this.y += this.vy;
        this.angle += this.angleSpeed;
        if(this.x<0 || this.x>canvas.width) this.vx*=-1;
        if(this.y<0 || this.y>canvas.height) this.vy*=-1;
      }
    }

    const bubbles = [];
    for(let i=0;i<50;i++) bubbles.push(new Bubble());

    const animate = () => {
      ctx.clearRect(0,0,canvas.width,canvas.height);
      bubbles.forEach(b => { b.update(); b.draw(); });
      requestAnimationFrame(animate);
    };
    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="relative flex items-center justify-center min-h-screen bg-gray-50 overflow-hidden">
      <canvas ref={canvasRef} className="fixed top-0 left-0 w-full h-full z-0" />

      <div className="relative z-10 w-full max-w-lg bg-white rounded-xl shadow-lg p-6 flex flex-col space-y-6">
        {/* Logo */}
        <div className="flex flex-col items-center space-y-3">
          <img src={FlatEarthSocietyLogo} alt="Flatopia Logo" className="w-20 h-20" />
          <h2 className="text-lg font-semibold text-center">Find better opportunities overseas</h2>
          <p className="text-sm text-gray-500">By flatopia.co</p>
          <select
            value={currentLang}
            onChange={(e)=>setCurrentLang(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
          >
            {Object.keys(langOptions).map((key) => (
              <option key={key} value={key}>{langOptions[key]}</option>
            ))}
          </select>
        </div>

        {/* Quick action buttons */}
        <div className="grid grid-cols-2 gap-3">
          {recommendations.map((text, idx) => (
            <button
              key={idx}
              className="border rounded-lg px-3 py-2 text-sm text-left hover:bg-gray-100"
              onClick={() => {
                setMessage(text);
                handleSend();
              }}
            >
              {text}
            </button>
          ))}
        </div>

        {/* Chat history */}
        <div className="flex flex-col space-y-3 max-h-64 overflow-y-auto border-t pt-3">
          {chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role==="user" ? "justify-end" : "justify-start"}`}
            >
              <div className={`px-4 py-2 rounded-2xl text-sm ${
                msg.role==="user"
                  ? "bg-blue-500 text-white rounded-br-none"
                  : "bg-gray-200 text-gray-800 rounded-bl-none"
              }`}>
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* Input bar */}
        <div className="flex items-center border rounded-lg px-3 py-2 space-x-3">
          <button><Plus size={20} /></button>
          <button><Globe size={20} /></button>
          <input
            type="text"
            placeholder={langData[currentLang].placeholder || "Message Flatopia"}
            className="flex-1 border-none focus:ring-0 text-sm"
            value={message}
            onChange={(e)=>setMessage(e.target.value)}
            onKeyDown={(e)=>e.key==="Enter" && handleSend()}
          />
          <button><Mic size={20} /></button>
          <button onClick={handleSend}><Send size={20} /></button>
        </div>
      </div>
    </div>
  );
}
