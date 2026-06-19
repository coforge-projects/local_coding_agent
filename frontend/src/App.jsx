import "./index.css";
import { useMsal } from "@azure/msal-react";
import { useState, useEffect } from "react";

function App() {
  const { instance, accounts } = useMsal();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // ✅ NEW: SKIP LOGIN STATE
  const [skipLogin, setSkipLogin] = useState(false);

  useEffect(() => {
    if (accounts.length > 0) {
      instance.setActiveAccount(accounts[0]);
    }
  }, [accounts, instance]);

  const login = () => {
    instance.loginRedirect({
      scopes: ["User.Read"],
    });
  };

  const logout = () => {
    instance.logoutRedirect();
  };

  // ✅ CHAT FUNCTION
  const sendMessage = () => {
    if (!input.trim()) return;

    const newMessages = [
      ...messages,
      { role: "user", text: input },
      { role: "bot", text: "This is a sample response (backend coming next 🚀)" }
    ];

    setMessages(newMessages);
    setInput("");
  };

  const account = instance.getActiveAccount();

  // ✅ LOGIN SCREEN (WITH SKIP OPTION)
  if (!account && !skipLogin) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h1>Azure Code Agent</h1>
          <p>Coforge Internal Platform</p>

          <button onClick={login}>
            Sign in with Microsoft
          </button>

          {/* ✅ SKIP BUTTON */}
          <button
            onClick={() => setSkipLogin(true)}
            style={{
              marginTop: "10px",
              background: "#e5e7eb",
              color: "#333"
            }}
          >
            Skip for now
          </button>

        </div>
      </div>
    );
  }

  // ✅ DASHBOARD
  return (
    <div className="app">

      <div className="top-bar"></div>

      <div className="header">
        <div className="logo">Coforge • Code Agent</div>

        <div className="user">
          <span>{account?.username || "Guest User"}</span>
          {account && <button onClick={logout}>Logout</button>}
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
          <h2>AI Assistant 💬</h2>

          <div className="chat-box">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={msg.role === "user" ? "chat user" : "chat bot"}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your prompt..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />

            <button onClick={sendMessage}>Send</button>
          </div>

        </div>

      </div>
    </div>
  );
}

export default App;
