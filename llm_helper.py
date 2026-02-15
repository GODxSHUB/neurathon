import requests
import time

def get_ai_steps(task, mood):
    """
    Connects to local Ollama instance to generate steps.
    Fallback to mock data if connection fails.
    """
    # 1. Prompt Engineering based on Mood
    mood_adjustments = {
        "Calm": "Make steps clear, logical, and standard.",
        "Low Energy": "Make steps EXTREMELY easy, gentle, and require minimal physical effort. Break it down to the tiniest movement.",
        "Overwhelmed": "Make steps calming, very simple, and non-demanding. Focus on just starting.",
        "Motivated": "Make steps efficient and slightly more challenging."
    }
    
    adjustment = mood_adjustments.get(mood, "Make steps manageable.")
    
    prompt = f"""
    You are a helpful assistant for a neurodivergent user.
    Task: "{task}"
    User Mood: {mood}. ({adjustment})
    
    Break this task down into 10-12 very small, specific, physical action steps.
    Rules:
    - the answer should be genreated within 2 minutes
    - No conversational filler (don't say "Here are your steps")
    - Just a numbered list (1. Step one...)
    - Each step must be short (under 10 words)
    """

    try:
        # 2. Call Local Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:7b",  # CHANGE THIS if you use a different model
                "prompt": prompt,
                "stream": False
            }
        )
        
        # 3. Process Response
        if response.status_code == 200:
            text = response.json()["response"]
            steps = []
            for line in text.split("\n"):
                clean_line = line.strip()
                # Extract text from numbered lists (e.g., "1. Do this")
                if clean_line and (clean_line[0].isdigit() or clean_line.startswith("-")):
                    parts = clean_line.split(".", 1)
                    if len(parts) > 1:
                        steps.append(parts[1].strip())
                    else:
                        steps.append(clean_line.lstrip("- ").strip())
            
            return steps if steps else ["Take a deep breath", "Just do the first tiny thing"]
        else:
            return ["Error connecting to AI", "Try breaking it down yourself"]

    except Exception as e:
        # Fallback if Ollama isn't running
        return [
            "⚠️ Ollama not detected", 
            "Make sure 'ollama serve' is running", 
            "Fallback: Take a deep breath",
            "Start with the smallest step"
        ]