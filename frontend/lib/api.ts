import { ChatRequest } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function streamChat(
  request: ChatRequest,
  onChunk: (chunk: string) => void,
  onError: (error: string) => void,
  onComplete: () => void
) {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No reader available');
    }

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        onComplete();
        break;
      }

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          try {
            const parsed = JSON.parse(data);
            if (parsed.content) {
              onChunk(parsed.content);
            } else if (parsed.error) {
              onError(parsed.error);
            } else if (parsed.done) {
              onComplete();
            }
          } catch (e) {
            // Skip invalid JSON
          }
        }
      }
    }
  } catch (error) {
    onError(error instanceof Error ? error.message : 'Unknown error');
  }
}

export async function fetchStyles() {
  try {
    const response = await fetch(`${API_URL}/styles`);
    if (!response.ok) {
      throw new Error('Failed to fetch styles');
    }
    const data = await response.json();
    return data.styles;
  } catch (error) {
    console.error('Error fetching styles:', error);
    return [];
  }
}
