'use client';

import React from 'react';
import { Search } from 'lucide-react';

interface DeepResearchToggleProps {
  enabled: boolean;
  onChange: (enabled: boolean) => void;
}

export default function DeepResearchToggle({ enabled, onChange }: DeepResearchToggleProps) {
  return (
    <button
      onClick={() => onChange(!enabled)}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all border ${
        enabled
          ? 'bg-claude-orange text-white border-claude-orange'
          : 'bg-claude-surface hover:bg-gray-700 border-claude-border'
      }`}
    >
      <Search size={16} />
      <span className="text-sm font-medium">Deep Research</span>
      <div
        className={`w-10 h-5 rounded-full transition-colors relative ${
          enabled ? 'bg-orange-600' : 'bg-gray-600'
        }`}
      >
        <div
          className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-transform ${
            enabled ? 'translate-x-5' : 'translate-x-0.5'
          }`}
        />
      </div>
    </button>
  );
}
