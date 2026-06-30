import "./index.css";
import "./App.css";
import coforgeLogo from "./assets/coforge-logo.png";
import { useMsal } from "@azure/msal-react";
import { useState, useEffect, useRef } from "react";


function App() {
  const { instance, accounts } = useMsal();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [skipLogin, setSkipLogin] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  const chatEndRef = useRef(null);
  const typingRef = useRef(null);
  const menuRef = useRef(null);
  // simple unique id generator for messages
  const makeId = (prefix = "") => `${prefix}${Date.now().toString(36)}-${Math.random().toString(36).slice(2,9)}`;

  useEffect(() => {
    if (accounts.length > 0) {
      instance.setActiveAccount(accounts[0]);
    }
  }, [accounts, instance]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const account = instance.getActiveAccount();

  const login = () => {
    instance.loginRedirect({
      scopes: ["User.Read"],
    });
  };

  const logout = () => {
    // If user is authenticated via MSAL, perform logout redirect.
    if (account) {
      instance.logoutRedirect();
      return;
    }
    // If running in skip-login/demo mode, just return to login screen.
    setSkipLogin(false);
    setShowMenu(false);
    setMessages([]);
  };

  const generateDummyResponse = (userInput) => {
    const text = userInput.toLowerCase();

    if (text.includes("hello") || text.includes("hi")) {
      return "Hello! I am your coding assistant. How can I help you today?";
    }

    if (text.includes("react")) {
      return "React is a JavaScript library used for building user interfaces. In this project, we are using React with Vite for the frontend.";
    }

    if (text.includes("api") || text.includes("backend")) {
      return "Backend integration is currently pending. Once the API endpoint, token, and project ID are available, this chat will be connected to the backend.";
    }

    if (text.includes("error")) {
      return "Please share the error message or screenshot, and I can help you debug it step by step.";
    }

    if (text.includes("code")) {
      return "Sure. I can help you generate, review, or modify code once backend integration is connected. For now, this is a frontend demo response.";
    }

    return "This is a frontend demo response. Backend integration will be added later once the backend credentials and API details are available.";
  };

  const sendMessage = (customPrompt) => {
    const messageToSend = customPrompt || input;

    if (!messageToSend.trim() || loading) return;

    const currentInput = messageToSend.trim();

    const userMessage = {
      id: makeId("u-"),
      role: "user",
      text: currentInput,
      createdAt: Date.now(),
    };

    console.log("User message sent:", currentInput);
    console.log("Typing started");

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    // small thinking delay then type out the response character-by-character
    setTimeout(() => {
      const fullResponse = generateDummyResponse(currentInput);

      // append an empty bot message placeholder with id
      const botId = makeId("b-");
      setMessages((prev) => [...prev, { id: botId, role: "bot", text: "", createdAt: Date.now() }]);

      let i = 0;
      const speed = 24; // ms per character

      // clear any existing typing interval
      if (typingRef.current) {
        clearInterval(typingRef.current);
      }

      typingRef.current = setInterval(() => {
        i += 1;

        setMessages((prev) => prev.map((m) => (m.id === botId ? { ...m, text: fullResponse.slice(0, i) } : m)));

        if (i >= fullResponse.length) {
          clearInterval(typingRef.current);
          typingRef.current = null;
          setLoading(false);
        }
      }, speed);
    }, 800);
  };

  const clearChat = () => {
    setMessages([]);
    setInput("");
    setLoading(false);
    if (typingRef.current) {
      clearInterval(typingRef.current);
      typingRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (typingRef.current) {
        clearInterval(typingRef.current);
        typingRef.current = null;
      }
    };
  }, []);

  // close menu when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (!menuRef.current) return;
      if (!menuRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", handler);
    return () => document.removeEventListener("click", handler);
  }, [menuRef]);

  // keyboard accessibility: close menu on Escape, open via keyboard
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") setShowMenu(false);
      if ((e.key === "Enter" || e.key === " ") && document.activeElement && document.activeElement.classList.contains("avatar-wrapper")) {
        e.preventDefault();
        setShowMenu((s) => !s);
      }
    };

    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);

  if (!account && !skipLogin) {
    return (
      <div className="login-container">
        <div className="top-bar-fixed">
          <img src={coforgeLogo} alt="Coforge" style={{ height: 36 }} />
        </div>

        <div className="login-card">
          <h1>Welcome</h1>
          <p>Coforge Platform</p>

          <button className="ms-login-btn" onClick={login}>Sign in with Microsoft</button>

          <button className="skip-btn" onClick={() => setSkipLogin(true)}>
            Skip
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">
        <div className="logo">
          <img src={coforgeLogo} alt="Coforge" style={{ height: 28 }} />
        </div>

        <div className="user" ref={menuRef}>
          <div className="avatar-wrapper" onClick={() => setShowMenu((s) => !s)} aria-haspopup="true" aria-expanded={showMenu}>
            <div className="avatar">{(account?.name || account?.username || "G").slice(0,1).toUpperCase()}</div>
          </div>

          {messages.length > 0 && (
            <button onClick={clearChat}>Clear Chat</button>
          )}

          {/* show menu for both authenticated and skip-login/demo users */}
          <div className={`user-menu ${showMenu ? "open" : ""}`}>
            <div className="menu-item" onClick={logout}>Logout</div>
          </div>
        </div>
      </div>

      <div className="layout">
        <div className="sidebar">
          <h3>Workspace</h3>

          <ul>
            <li>AI Chat</li>
            <li>Projects</li>
            <li>Logs</li>
          </ul>
        </div>

        <div className="main">
          <div className="chat-title-row">
            <div>
              <h2>AI Assistant</h2>
            </div>
          </div>

          <div className="chat-box">
            {messages.length === 0 && !loading && (
              <div className="empty-state">
                <h3>How can I help you today?</h3>

                <p>
                  Ask anything about code, React, errors, or backend integration.
                </p>

                <div className="suggestions">
                  <button type="button" onClick={() => sendMessage("Hello")}>
                    Hello
                  </button>

                  <button
                    type="button"
                    onClick={() => sendMessage("Explain React")}
                  >
                    Explain React
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      sendMessage("Backend integration status")
                    }
                  >
                    Backend Status
                  </button>
                </div>
              </div>
            )}

            {messages.map((msg) => (
              <div key={msg.id || msg.createdAt} className={`chat ${msg.role}`} role="article" aria-label={`${msg.role} message`}>
                {msg.text}
              </div>
            ))}

            {loading && (
              <div className="typing-bubble">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            )}           
            <div ref={chatEndRef}></div>
          </div>

          <div className="chat-input">
            <input
              value={input}
              placeholder="Type your prompt..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading) {
                  sendMessage();
                }
              }}
            />

            <button onClick={() => sendMessage()} disabled={loading}>
              {loading ? "Typing..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;