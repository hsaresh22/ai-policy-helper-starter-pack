export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function apiAsk(query: string, k: number = 4) {
  const r = await fetch(`${API_BASE}/api/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, k })
  });
  if (!r.ok) throw new Error('Ask failed');
  return r.json();
}

export async function apiAskStream(query: string, k: number = 4, onChunk: (chunk: any) => void) {
  const r = await fetch(`${API_BASE}/api/ask-stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, k })
  });
  if (!r.ok) throw new Error('Ask stream failed');
  
  const reader = r.body?.getReader();
  if (!reader) throw new Error('No response body');
  
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      console.log('Stream ended');
      break;
    }
    
    buffer += decoder.decode(value, { stream: true });
    console.log('Received chunk, buffer length:', buffer.length);
    
    // Process complete lines
    while (true) {
      const lineEnd = buffer.indexOf('\n');
      if (lineEnd === -1) break;
      
      const line = buffer.slice(0, lineEnd).trim();
      buffer = buffer.slice(lineEnd + 1);
      
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        console.log('Parsed SSE data:', data.slice(0, 100));
        if (data === '[DONE]') {
          console.log('Received DONE signal');
          return;
        }
        try {
          const parsed = JSON.parse(data);
          console.log('Calling onChunk with type:', parsed.type);
          onChunk(parsed);
        } catch (e) {
          console.error('Failed to parse chunk:', e, 'data:', data);
        }
      }
    }
  }
}

export async function apiIngest() {
  const r = await fetch(`${API_BASE}/api/ingest`, { method: 'POST' });
  if (!r.ok) throw new Error('Ingest failed');
  return r.json();
}

export async function apiMetrics() {
  const r = await fetch(`${API_BASE}/api/metrics`);
  if (!r.ok) throw new Error('Metrics failed');
  return r.json();
}
