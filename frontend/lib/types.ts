export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  messages: Message[];
  style: string;
  deep_research: boolean;
  temperature?: number;
  max_tokens?: number;
}

export interface Style {
  name: string;
  display_name: string;
  description: string;
}
