import DOMPurify from "dompurify";
import { Send } from "lucide-react";
import { marked } from "marked";
import { useEffect, useRef, useState } from "react";
import { langData, langOptions } from './constants';
import FlatopiaLogo from '/flatopia-logo.png';

export default function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [currentLang, setCurrentLang] = useState("en");
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  const recommendations = langData[currentLang].recommendations;

  const hasMessages = chatHistory.length > 0;

  // 自动滚动
  useEffect(() => {
    const scrollToBottom = (behavior = "smooth") => {
      bottomRef.current?.scrollIntoView({ behavior, block: "end" });
    };

    scrollToBottom();

    const handleResize = () => scrollToBottom("instant");
    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, [chatHistory]);

  const handleReplaceMessage = (newMessage) => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.focus();

    textarea.setSelectionRange(0, textarea.value.length);

    if (!document.execCommand('insertText', false, newMessage)) {
      textarea.value = newMessage;
      textarea.dispatchEvent(new InputEvent("input", {
        bubbles: true,
        cancelable: true,
        inputType: "insertReplacementText",
        data: newMessage,
      }));
    }
  };

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
    const msg = message.trim();
    if (!msg) return;

    setChatHistory(prev => [...prev, { role: "user", text: msg }]);
    const userMessage = message;
    setMessage("");

    const aiReply = await callLangFlowAPI(userMessage);

    setChatHistory(prev => [...prev, { role: "bot", text: aiReply }]);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div
        className={`bg-white shadow-lg flex flex-col transition-all duration-500 ${hasMessages
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
            </div>

            <div className="flex flex-col items-center space-y-3">
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                className="border rounded px-2 py-1 text-sm"
              >
                {Object.keys(langOptions).map((key) => (
                  <option key={key} value={key}>{langOptions[key]}</option>
                ))}
              </select>
              <div className="grid grid-cols-2 gap-3">
                {recommendations.map((text, idx) => (
                  <button
                    key={idx}
                    className="border rounded-lg px-3 py-2 text-sm text-left hover:bg-gray-100"
                    onClick={() => {
                      handleReplaceMessage(text);
                    }}
                  >
                    {text}
                  </button>
                ))}
              </div>
            </div>
          </>
        ) : (
          // ---------------- Chat View ----------------
          <>
            <div className="flex-1 overflow-y-auto p-6 space-y-3">
              {chatHistory.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`px-4 py-2 rounded-2xl text-sm whitespace-pre-wrap break-words max-w-[75%] ${msg.role === "user"
                      ? "bg-blue-500 text-white rounded-br-none"
                      : "bg-gray-200 text-gray-800 rounded-bl-none prose prose-sm max-w-none"
                      }`}
                    {...(msg.role === "bot"
                      ? { dangerouslySetInnerHTML: { __html: DOMPurify.sanitize(marked.parse(msg.text)) } }
                      : { children: msg.text })}
                  />
                </div>
              ))}

              <div ref={bottomRef} />
            </div>
          </>
        )}

        {/* Input bar */}
        <div className="flex items-center border-t px-3 py-3 space-x-3">
          <textarea
            autoFocus
            placeholder={langData[currentLang].placeholder || "Message Flatopia"}
            className="flex-1 border resize-none focus:ring-0 text-sm bg-white rounded-lg px-3 py-2"
            value={message}
            ref={textareaRef}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => !e.shiftKey && e.key === "Enter" && (e.preventDefault(), handleSend())}
          />
          <button
            className="text-gray-600 hover:text-gray-800"
            onClick={handleSend}
            type="button"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
