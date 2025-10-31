import requests
import json

def query_ollama(prompt, model='deepseek-r1:1.5b', stream=True):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': model,
        'prompt': prompt,
        'stream': stream
    }

    try:
        if stream:
            response = requests.post(url, headers=headers, json=data, stream=True)
            response.raise_for_status()

            collected = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        token = chunk.get('response', '')
                        print(token, end='', flush=True)
                        collected += token
                    except json.JSONDecodeError:
                        continue
            print()  # Clean newline after streaming
            return collected

        else:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get('response')

    except requests.RequestException as e:
        print(f"[ERROR] Ollama request failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "Can you summarize this current chat so far"
    result = query_ollama(prompt, stream=True)
    print("\n\n[Final Output]:", result)