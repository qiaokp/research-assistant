'use client';

import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import StyleSelector from '@/components/StyleSelector';
import DeepResearchToggle from '@/components/DeepResearchToggle';
import { Message, Style } from '@/lib/types';
import { streamChat, fetchStyles } from '@/lib/api';
import { Loader2, Github } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [styles, setStyles] = useState<Style[]>([]);
  const [selectedStyle, setSelectedStyle] = useState('default');
  const [deepResearch, setDeepResearch] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch available styles on mount
  useEffect(() => {
    async function loadStyles() {
      const fetchedStyles = await fetchStyles();
      if (fetchedStyles.length > 0) {
        setStyles(fetchedStyles);
      }
    }
    loadStyles();
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    setError(null);

    // Add user message
    const userMessage: Message = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Create placeholder for assistant message
    let assistantContent = '';
    const assistantMessage: Message = { role: 'assistant', content: '' };
    setMessages(prev => [...prev, assistantMessage]);

    try {
      await streamChat(
        {
          messages: [...messages, userMessage],
          style: selectedStyle,
          deep_research: deepResearch,
          temperature: 0.7,
          max_tokens: 3000,
        },
        (chunk) => {
          // Update assistant message with new chunk
          assistantContent += chunk;
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = {
              role: 'assistant',
              content: assistantContent,
            };
            return newMessages;
          });
        },
        (errorMsg) => {
          setError(errorMsg);
          setIsLoading(false);
        },
        () => {
          setIsLoading(false);
        }
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIsLoading(false);
      // Remove the empty assistant message on error
      setMessages(prev => prev.slice(0, -1));
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen bg-claude-bg text-gray-100">
      {/* Header */}
      <header className="border-b border-claude-border bg-claude-surface">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-semibold">Research Assistant</h1>
            {messages.length > 0 && (
              <button
                onClick={handleNewChat}
                className="px-3 py-1.5 text-sm bg-claude-bg hover:bg-gray-700 rounded-lg transition-colors"
              >
                New Chat
              </button>
            )}
          </div>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-gray-200 transition-colors"
          >
            <Github size={20} />
          </a>
        </div>
      </header>

      {/* Controls */}
      <div className="border-b border-claude-border bg-claude-surface">
        <div className="max-w-5xl mx-auto px-6 py-3 flex items-center gap-4">
          {styles.length > 0 && (
            <StyleSelector
              styles={styles}
              selectedStyle={selectedStyle}
              onStyleChange={setSelectedStyle}
            />
          )}
          <DeepResearchToggle
            enabled={deepResearch}
            onChange={setDeepResearch}
          />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full px-6">
              <div className="text-center max-w-2xl">
                <h2 className="text-3xl font-bold mb-4">
                  Welcome to Research Assistant
                </h2>
                <p className="text-gray-400 mb-8">
                  An open-source AI research assistant powered by local LLMs.
                  Ask questions, conduct deep research, and explore information with different conversation styles.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                  <div className="p-4 bg-claude-surface rounded-lg border border-claude-border">
                    <h3 className="font-semibold mb-2">🎨 Conversation Styles</h3>
                    <p className="text-sm text-gray-400">
                      Choose from different response styles: concise, explanatory, formal, creative, and more.
                    </p>
                  </div>
                  <div className="p-4 bg-claude-surface rounded-lg border border-claude-border">
                    <h3 className="font-semibold mb-2">🔍 Deep Research</h3>
                    <p className="text-sm text-gray-400">
                      Enable deep research mode to perform multi-step web searches and synthesize comprehensive answers.
                    </p>
                  </div>
                  <div className="p-4 bg-claude-surface rounded-lg border border-claude-border">
                    <h3 className="font-semibold mb-2">🌐 Web Search</h3>
                    <p className="text-sm text-gray-400">
                      Automatically searches the web for current information using Tavily API.
                    </p>
                  </div>
                  <div className="p-4 bg-claude-surface rounded-lg border border-claude-border">
                    <h3 className="font-semibold mb-2">🔓 Open Source</h3>
                    <p className="text-sm text-gray-400">
                      Powered by open-source LLMs (Ollama or OpenRouter) for complete privacy and control.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div>
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  role={message.role}
                  content={message.content}
                />
              ))}
              {isLoading && (
                <div className="flex gap-4 p-6">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 rounded-full bg-claude-orange flex items-center justify-center">
                      <Loader2 size={20} className="animate-spin" />
                    </div>
                  </div>
                  <div className="flex-1 pt-1 text-gray-400">
                    Thinking...
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="border-t border-claude-border bg-red-900/20">
          <div className="max-w-5xl mx-auto px-6 py-3 text-red-400 text-sm">
            Error: {error}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-claude-border bg-claude-surface">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
          <div className="mt-2 text-xs text-gray-500 text-center">
            Powered by open-source LLMs • Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  );
}
