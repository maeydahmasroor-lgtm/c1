import React, { useState, useRef } from 'react';
import './chatbot.module.css'
export default function BookChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: 'user'|'bot', text: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  const ask = async () => {
    if (!input.trim() || loading) return;
    
    const userMsg = { role: 'user' as const, text: input };
    setMessages(m => [...m, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Get selected text (if any)
      const selected = window.getSelection()?.toString().trim() || null;

      const res = await fetch('http://localhost:8000/ask', {
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
    <div className="fixed bottom-6 right-6 z-50 bg-red">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-indigo-600 text-white w-14 h-14 rounded-full flex items-center justify-center shadow-lg hover:bg-indigo-700 text-xl"
          aria-label="Ask about this book"
        >
          ?
        </button>
      ) : (
        <div className="w-80 h-96 bg-white border rounded-xl shadow-xl flex flex-col overflow-hidden">
          <div className="bg-indigo-700 text-white p-3 flex justify-between items-center">
            <span>📘 Ask the Book</span>
            <button onClick={() => setIsOpen(false)} className="text-white">×</button>
          </div>
          
          <div className="flex-1 p-3 overflow-y-auto bg-gray-50">
            {messages.length === 0 && (
              <p className="text-gray-500 text-sm">
                Ask anything! 💡 Highlight text first for precise answers.
              </p>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`my-2 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
                <span className={`inline-block p-2 rounded-lg max-w-[80%] ${
                  m.role === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200'
                }`}>
                  {m.text}
                </span>
              </div>
            ))}
            {loading && <div className="text-gray-500 italic">Thinking...</div>}
            <div ref={endRef} />
          </div>

          <form onSubmit={(e) => { e.preventDefault(); ask(); }} className="p-2 border-t">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Type your question..."
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
          </form>
        </div>
      )}
    </div>
  );
}