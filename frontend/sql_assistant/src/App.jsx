// App.jsx
import React, { useState, useRef, useEffect } from "react";
import { fetchQuery } from "./api";
import DashboardChart from "./components/DashboardChart";
import { Send, Bot, User, Sparkles, BarChart3, Loader2 } from "lucide-react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: "user",
      content: question,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const data = await fetchQuery(question);

      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content: data.summary,
        chart: data.chart,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: "error",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-linear-to-r from-blue-600 to-indigo-600 p-2 rounded-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-linear-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Talk to your data
            </h1>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered CRM Analytics</span>
          </div>
        </div>
      </header>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-4 py-8">
          {messages.length === 0 ? (
            // Welcome Screen
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
              <div className="bg-linear-to-r from-blue-600 to-indigo-600 p-4 rounded-full mb-6">
                <Bot className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-3">
                How can I help you today?
              </h2>
              <p className="text-gray-500 max-w-md mb-8">
                Ask me anything about your sales data, campaigns, or customer insights
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                {[
                  "Show total revenue",
                  "Which products generated the most revenue",
                  "list all february 2026 orders with customer names",
                  "Monthly revenue trend",
                  "How many each activities did each employee complete",
                  "Quarterly performance report",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => {
                      setQuestion(suggestion);
                      inputRef.current?.focus();
                    }}
                    className="text-left px-4 py-3 bg-white border border-gray-200 rounded-xl hover:border-blue-400 hover:shadow-sm transition-all"
                  >
                    <span className="text-gray-700">{suggestion}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            // Chat Messages
            <div className="space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-4 ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.type !== "user" && (
                    <div className="shrink-0">
                      <div className="w-8 h-8 rounded-full bg-linear-to-r from-blue-600 to-indigo-600 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                      </div>
                    </div>
                  )}
                  
                  <div
                    className={`max-w-3xl ${
                      message.type === "user"
                        ? "bg-blue-600 text-white rounded-2xl rounded-tr-none"
                        : message.type === "error"
                        ? "bg-red-50 text-red-800 rounded-2xl rounded-tl-none border border-red-200"
                        : "bg-white rounded-2xl rounded-tl-none shadow-sm"
                    } px-6 py-4`}
                  >
                    {message.type === "user" && (
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs text-blue-100">
                          {message.timestamp}
                        </span>
                      </div>
                    )}
                    
                    <div className="prose max-w-none">
                      {message.type === "user" ? (
                        <p className="text-white">{message.content}</p>
                      ) : (
                        <>
                          <p className="text-gray-800 mb-4">{message.content}</p>
                          {message.chart && (
                            <div className="mt-4 border-t pt-4">
                              <DashboardChart chart={message.chart} />
                            </div>
                          )}
                        </>
                      )}
                    </div>
                    
                    {message.type === "assistant" && (
                      <div className="mt-2 text-xs text-gray-400">
                        {message.timestamp}
                      </div>
                    )}
                  </div>

                  {message.type === "user" && (
                    <div className="shrink-0">
                      <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                        <User className="w-5 h-5 text-white" />
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="flex gap-4">
                  <div className="shrink-0">
                    <div className="w-8 h-8 rounded-full bg-linear-to-r from-blue-600 to-indigo-600 flex items-center justify-center">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  </div>
                  <div className="bg-white rounded-2xl rounded-tl-none px-6 py-4 shadow-sm">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                      <span className="text-gray-600">Analyzing your data...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white px-4 py-4">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <input
              ref={inputRef}
              type="text"
              className="w-full border border-gray-300 rounded-xl pl-6 pr-24 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
              placeholder="Ask a question about your data..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
              <button
                type="submit"
                disabled={!question.trim() || loading}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
                  !question.trim() || loading
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-linear-to-r from-blue-600 to-indigo-600 text-white hover:shadow-md"
                }`}
              >
                <Send className="w-4 h-4" />
                <span className="hidden sm:inline">Send</span>
              </button>
            </div>
          </form>
          <p className="text-xs text-gray-400 mt-2 text-center">
            Press Enter to send • Ask about sales, campaigns, customers, or any business metric
          </p>
        </div>
      </div>
    </div>
  );
}