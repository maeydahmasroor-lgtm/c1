import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import styles from './chatbot.module.css';

const Chatbot = ({ selectedText }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending a message (either general or selected text)
  const sendMessage = async (queryText, isSelectedTextQuery = false) => {
    if (queryText.trim() === '') return;

    setIsLoading(true);
    const newUserMessage = { text: queryText, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    setInput('');

    try {
      // Backend API URL
      const API_BASE_URL = 'https://c1-miez.vercel.app/';
      const endpoint = '/query/selected-text';
      const payload = isSelectedTextQuery
        ? { question: queryText, selected_text: selectedText }
        : { question: queryText };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errorDetail = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorDetail = errorData.detail || errorDetail;
        } catch (e) {
          // Ignore if response is not JSON or empty
        }
        throw new Error(errorDetail);
      }

      const data = await response.json();
      const botMessage = { text: data.answer, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = { text: `Sorry, an error occurred: ${error.message}`, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneralSend = (event) => {
    event.preventDefault();
    sendMessage(input, false);
  };

  const handleSelectedTextSend = () => {
    if (selectedText && selectedText.trim() !== '') {
      sendMessage(`Explain this text: "${selectedText.substring(0, 100)}${selectedText.length > 100 ? '...' : ''}"`, true);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          className={styles.fabButton}
          onClick={() => setIsOpen(true)}
          aria-label="Open AI Assistant"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      )}

      {/* Chat Widget */}
      {isOpen && (
        <div className={styles.chatWidget}>
          {/* Header */}
          <div className={styles.chatHeader}>
            <div className={styles.headerContent}>
              <div className={styles.statusIndicator}></div>
              <h3>AI Assistant</h3>
            </div>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          {/* Messages Area */}
          <div className={styles.messagesContainer}>
            {messages.length === 0 && (
              <div className={styles.emptyState}>
                <div className={styles.emptyIcon}>💬</div>
                <p>Ask me anything about Physical AI and Humanoid Robotics!</p>
              </div>
            )}
            {messages.map((msg, index) => (
              <div
                key={index}
                className={msg.sender === 'user' ? styles.userMessage : styles.botMessage}
              >
                <div className={styles.messageContent}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className={styles.botMessage}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Selected Text Display */}
          {selectedText && (
            <div className={styles.selectedTextBanner}>
              <div className={styles.selectedTextContent}>
                <span className={styles.selectedTextLabel}>Selected:</span>
                <span className={styles.selectedTextPreview}>
                  {selectedText.length > 60 ? selectedText.substring(0, 60) + '...' : selectedText}
                </span>
              </div>
              <button
                className={styles.askButton}
                onClick={handleSelectedTextSend}
              >
                Ask
              </button>
            </div>
          )}

          {/* Input Form */}
          <form onSubmit={handleGeneralSend} className={styles.inputForm}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              className={styles.messageInput}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isLoading || !input.trim()}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
};

Chatbot.propTypes = {
  selectedText: PropTypes.string
};

export default Chatbot;