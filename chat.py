import requests
import json

def format_conversation(history):
    """Format chat history into a single prompt string."""
    formatted = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted += f"{role}: {msg['content']}\n"
    formatted += "Assistant: "
    return formatted

def call_ollama(prompt, model='deepseek-r1:1.5b'):
    """Call Ollama with the full prompt and stream the response."""
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': model,
        'prompt': prompt,
        'stream': True
    }

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()

        reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    token = chunk.get('response', '')
                    print(token, end='', flush=True)
                    reply += token
                except json.JSONDecodeError:
                    continue
        print()
        return reply

    except requests.RequestException as e:
        print(f"[ERROR] Failed to connect to Ollama: {e}")
        return ""

def chat_loop(model='deepseek-r1:1.5b'):
    print(f"\nChatting with: {model}")
    print("Type '/exit' to quit, '/clear' to reset conversation.\n")

    history = []

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/exit":
            break
        if user_input.lower() == "/clear":
            history = []
            print("Conversation cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})
        prompt = format_conversation(history)
        assistant_reply = call_ollama(prompt, model=model)
        history.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    chat_loop()