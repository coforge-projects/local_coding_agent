import React, { useState, useRef, useEffect } from "react";

// Single-file Chat App with Sidebar (Tailwind CSS classes assumed)
export default function App() {
  const makeId = (p = "") => `${p}${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;

  const initialChats = [
    {
      id: makeId("c-"),
      title: "Welcome chat",
      createdAt: Date.now(),
      messages: [
        { role: "bot", content: "Welcome! Ask me anything about your project." },
      ],
    },
    {
      id: makeId("c-"),
      title: "React questions",
      createdAt: Date.now() - 1000 * 60 * 60,
      messages: [
        { role: "user", content: "How do I lift state up in React?" },
        { role: "bot", content: "You pass handlers from parent to children via props..." },
      ],
    },
  ];

  const [chats, setChats] = useState(initialChats);
  const [activeId, setActiveId] = useState(initialChats[0].id);
  const [input, setInput] = useState("");
  const chatScrollRef = useRef(null);

  useEffect(() => {
    // scroll to bottom when active chat changes or messages update
    chatScrollRef.current?.scrollTo({ top: chatScrollRef.current.scrollHeight, behavior: "smooth" });
  }, [activeId, chats]);

  const activeChat = chats.find((c) => c.id === activeId) || chats[0];

  function newChat() {
    const id = makeId("c-");
    const chat = { id, title: "New Chat", createdAt: Date.now(), messages: [] };
    setChats((s) => [chat, ...s]);
    setActiveId(id);
  }

  function selectChat(id) {
    setActiveId(id);
  }

  function sendMessage() {
    if (!input.trim()) return;
    const userMsg = { role: "user", content: input.trim() };
    const botId = makeId("b-");

    setChats((prev) =>
      prev.map((c) => (c.id === activeId ? { ...c, messages: [...c.messages, userMsg] } : c))
    );
    setInput("");

    // fake bot reply
    setTimeout(() => {
      const botMsg = { role: "bot", content: "(simulated) Thanks — I will look into that." };
      setChats((prev) => prev.map((c) => (c.id === activeId ? { ...c, messages: [...c.messages, botMsg] } : c)));
    }, 700 + Math.random() * 700);
  }

  function formatTime(ts) {
    if (!ts) return "";
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  return (
    <div className="h-screen flex bg-gray-50 text-slate-800">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex-shrink-0 flex flex-col">
        <div className="p-4 border-b border-gray-100">
          <button
            onClick={newChat}
            className="w-full inline-flex items-center justify-center gap-2 px-3 py-2 rounded-md bg-[#07223a] text-white text-sm font-semibold hover:opacity-95 transition"
            aria-label="New chat"
          >
            {/* simple plus icon */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          <div className="space-y-2">
            {chats.map((c) => {
              const last = c.messages[c.messages.length - 1];
              const lastTime = c.createdAt || (last ? Date.now() : null);
              const active = c.id === activeId;
              return (
                <button
                  key={c.id}
                  onClick={() => selectChat(c.id)}
                  className={`w-full text-left flex items-start gap-3 p-3 rounded-md transition-all duration-150 ${
                    active ? "bg-slate-50 border border-slate-100 shadow-sm" : "hover:bg-gray-50"
                  }`}
                >
                  <div className="flex-shrink-0 h-9 w-9 rounded-full bg-gradient-to-br from-[#006c8e] to-[#07223a] text-white flex items-center justify-center font-bold">
                    {c.title?.slice(0,1)?.toUpperCase() || "C"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-center">
                      <div className="text-sm font-semibold truncate">{c.title || "Untitled"}</div>
                      <div className="text-xs text-slate-400 ml-2">{formatTime(lastTime)}</div>
                    </div>
                    <div className="text-xs text-slate-500 truncate mt-1">
                      {last ? (last.role === "user" ? `You: ${last.content}` : `Bot: ${last.content}`) : <span className="text-slate-400">Start a new chat</span>}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-3 border-t border-gray-100 text-xs text-slate-500">Coforge-style chat • demo</div>
      </aside>

      {/* Chat area */}
      <main className="flex-1 flex flex-col">
        <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-white">
          <div>
            <h3 className="text-lg font-bold">{activeChat?.title || "New Chat"}</h3>
            <p className="text-xs text-slate-400">{activeChat?.messages?.length} messages</p>
          </div>
        </div>

        <div className="flex-1 overflow-hidden flex flex-col">
          <div ref={chatScrollRef} className="flex-1 overflow-y-auto p-6 space-y-4 bg-white">
            {activeChat?.messages?.length ? (
              activeChat.messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[70%] px-4 py-2 rounded-lg shadow-sm ${
                      m.role === "user" ? "bg-[#07223a] text-white rounded-br-sm" : "bg-gray-100 text-slate-800 rounded-bl-sm"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{m.content}</div>
                    <div className="text-[10px] text-slate-400 mt-1 text-right">{formatTime(activeChat.createdAt)}</div>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center text-slate-400 mt-20">No messages yet — say hello.</div>
            )}
          </div>

          <div className="p-4 bg-white border-t border-gray-100">
            <div className="flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") sendMessage(); }}
                placeholder="Type your message..."
                className="flex-1 px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-[#006c8e]"
              />
              <button onClick={sendMessage} className="px-4 py-2 rounded-md bg-[#07223a] text-white font-semibold hover:opacity-95">Send</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
