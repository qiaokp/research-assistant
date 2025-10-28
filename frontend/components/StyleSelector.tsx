'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Sparkles } from 'lucide-react';
import { Style } from '@/lib/types';

interface StyleSelectorProps {
  styles: Style[];
  selectedStyle: string;
  onStyleChange: (style: string) => void;
}

export default function StyleSelector({
  styles,
  selectedStyle,
  onStyleChange
}: StyleSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentStyle = styles.find(s => s.name === selectedStyle) || styles[0];

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-claude-surface hover:bg-gray-700 rounded-lg transition-colors border border-claude-border"
      >
        <Sparkles size={16} className="text-claude-orange" />
        <span className="text-sm font-medium">{currentStyle?.display_name}</span>
        <ChevronDown size={16} className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-64 bg-claude-surface border border-claude-border rounded-lg shadow-xl z-50 overflow-hidden">
          {styles.map((style) => (
            <button
              key={style.name}
              onClick={() => {
                onStyleChange(style.name);
                setIsOpen(false);
              }}
              className={`w-full text-left px-4 py-3 hover:bg-gray-700 transition-colors ${
                style.name === selectedStyle ? 'bg-gray-700' : ''
              }`}
            >
              <div className="font-medium text-sm mb-1">{style.display_name}</div>
              <div className="text-xs text-gray-400">{style.description}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
