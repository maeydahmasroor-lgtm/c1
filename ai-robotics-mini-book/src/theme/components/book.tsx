// src/components/BookChatbot.tsx
import React, { useState, useRef, useEffect } from 'react';
import styles from './book.module.css';

export default function BookChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: 'user'|'bot', text: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const ask = async () => {
    if (!input.trim() || loading) return;
    
    const userMsg = { role: 'user' as const, text: input };
    setMessages(m => [...m, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Get selected text (if any)
      const selected = window.getSelection()?.toString().trim() || undefined;

      const res = await fetch('http://localhost:8000/query/selected-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, selected_text: selected })
      });

      const data = await res.json();
      setMessages(m => [...m, { role: 'bot', text: data.answer }]);
    } catch (err) {
      setMessages(m => [...m, { role: 'bot', text: '❌ Failed to get answer.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.root}>
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className={styles.button}
          aria-label="Ask about this book"
        >
          ?
        </button>
      ) : (
        <div className={styles.window}>
          <div className={styles.header}>
            <span>📘 Ask the Book</span>
            <button 
              onClick={() => setIsOpen(false)} 
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          
          <div className={styles.messages}>
            {messages.length === 0 && (
              <p className={styles.placeholder}>
                Ask anything! 💡 Highlight text first for precise answers.
              </p>
            )}
            {messages.map((m, i) => (
              <div 
                key={i} 
                className={m.role === 'user' ? styles.user : styles.bot}
              >
                {m.text}
              </div>
            ))}
            {loading && (
              <div className={styles.thinking}>Thinking...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form 
            onSubmit={(e) => { e.preventDefault(); ask(); }} 
            className={styles.inputArea}
          >
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Type your question..."
              className={styles.input}
              disabled={loading}
            />
          </form>
        </div>
      )}
    </div>
  );
}