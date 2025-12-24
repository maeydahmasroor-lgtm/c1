import React, { useState, useRef, useEffect } from "react";
import "./chat.css";

type Message = {
  role: "user" | "bot";
  text: string;
};

export default function ChatbotPopup() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send() {
    if (!input.trim() || loading) return;

    const userMsg = { role: "user" as const, text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.text }),
      });

      const data = await res.json();

      setMessages((m) => [...m, { role: "bot", text: data.answer }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "bot", text: "❌ Server error. Try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {!open && (
        <button className="chat-fab" onClick={() => setOpen(true)}>
          💬
        </button>
      )}

      {open && (
        <div className="chat-window">
          <div className="chat-header">
            <span>📘 Ask the Book</span>
            <button onClick={() => setOpen(false)}>×</button>
          </div>

          <div className="chat-messages">
            {messages.length === 0 && (
              <p className="chat-placeholder">
                Ask anything about the book…
              </p>
            )}

            {messages.map((m, i) => (
              <div key={i} className={`chat-msg ${m.role}`}>
                {m.text}
              </div>
            ))}

            {loading && <div className="chat-msg bot">Thinking…</div>}
            <div ref={endRef} />
          </div>

          <form
            className="chat-input"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a question…"
            />
          </form>
        </div>
      )}
    </>
  );
}
