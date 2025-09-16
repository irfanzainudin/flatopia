import React, { useEffect, useRef, useState } from "react";
import FlatopiaLogo from '/flatopia-logo.png';
import { Send } from "lucide-react";
import { langOptions, langData } from './constants';

export default function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [currentLang, setCurrentLang] = useState("en");
  const [recommendations, setRecommendations] = useState(langData[currentLang].recommendations);
  const bottomRef = useRef(null);

  useEffect(() => {
    setRecommendations(langData[currentLang].recommendations);
  }, [currentLang]);

  const hasMessages = chatHistory.length > 0;

  // 自动滚动
  useEffect(() => {
    requestAnimationFrame(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
    });
  }, [chatHistory]);

  useEffect(() => {
    const onResize = () => bottomRef.current?.scrollIntoView({ behavior: "instant", block: "end" });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  // ---------------- API 调用函数 ----------------
const callLangFlowAPI = async (userMessage) => {
  if (!import.meta.env.VITE_REACT_APP_LANGFLOW_API_KEY) {
    console.error("REACT_APP_LANGFLOW_API_KEY environment variable not found.");
    return "⚠️ API key missing!";
  }

  const payload = {
    output_type: "chat",
    input_type: "chat",
    input_value: userMessage,
    tweaks: {
      "LMStudioEmbeddingsComponent-JMYUN": { model: "text-embedding-nomic-embed-text-v1.5" },
      "GroqModel-EPLOj": { model_name: import.meta.env.VITE_GROQ_MODEL_NAME }
    },
    session_id: "user_1"
  };

  const response = await fetch(`https://${import.meta.env.VITE_API_LINK}/api/v1/run/flatopia_deploy`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": import.meta.env.VITE_REACT_APP_LANGFLOW_API_KEY
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  // ✅ 正确解析 AI 消息
  const aiText =
    data?.outputs?.[0]?.outputs?.[0]?.results?.message?.text ||
    data?.outputs?.[0]?.outputs?.[0]?.results?.message?.default_value ||
    "No response from AI.";

  return aiText;
};

  // ---------------- 发送消息 ----------------
  const handleSend = async () => {
    if (!message.trim()) return;

    setChatHistory(prev => [...prev, { role: "user", text: message }]);
    const userMessage = message;
    setMessage("");

    const aiReply = await callLangFlowAPI(userMessage);

    setChatHistory(prev => [...prev, { role: "bot", text: aiReply }]);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div
        className={`bg-white shadow-lg flex flex-col transition-all duration-500 ${
          hasMessages
            ? "w-full h-screen max-w-none rounded-none"
            : "w-full max-w-lg rounded-xl p-6 space-y-6"
        }`}
      >
        {!hasMessages ? (
          // ---------------- Onboarding View ----------------
          <>
            <div className="flex flex-col items-center space-y-3">
              <img src={FlatopiaLogo} alt="Flatopia Logo" className="w-30 h-20" />
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

            <div className="grid grid-cols-2 gap-3">
              {recommendations.map((text, idx) => (
                <button
                  key={idx}
                  className="border rounded-lg px-3 py-2 text-sm text-left hover:bg-gray-100"
                  onClick={() => {
                    setMessage(text);
                    handleSend(); // 点击直接发送推荐消息
                  }}
                >
                  {text}
                </button>
              ))}
            </div>
          </>
        ) : (
          // ---------------- Chat View ----------------
          <>
            <div className="flex-1 overflow-y-auto p-6 space-y-3">
              {chatHistory.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`px-4 py-2 rounded-2xl text-sm break-words max-w-[75%] ${
                      msg.role === "user"
                        ? "bg-blue-500 text-white rounded-br-none"
                        : "bg-gray-200 text-gray-800 rounded-bl-none"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>
          </>
        )}

        {/* Input bar */}
        <div className="flex items-center border-t px-3 py-3 space-x-3">
          <input
            type="text"
            placeholder={langData[currentLang].placeholder || "Message Flatopia"}
            className="flex-1 border-none focus:ring-0 text-sm bg-white rounded-lg px-3 py-2"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            className="text-gray-600 hover:text-gray-800"
            onClick={handleSend}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
