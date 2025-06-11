import requests
import pandas as pd
import json
from typing import Optional
import re


DEEPSEEK_API_KEY = "sk-612784d0a4e1415e987a39dd4657426e"  # Replace with your actual API key
API_URL = "https://api.deepseek.com/v1/chat/completions"

def deepseek_chat(prompt: str, df: Optional[pd.DataFrame] = None) -> str:
    """
    Sends a prompt to DeepSeek API, optionally including a pandas DataFrame.
    
    Args:
        prompt: Input string prompt
        df: Optional pandas DataFrame to include in the prompt
    
    Returns:
        Generated text response from DeepSeek
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Process DataFrame if provided
    data_content = ""
    if df is not None:
        try:
            # Convert DataFrame to markdown format
            data_content = "DATA CONTENT:\n"
            data_content += df.to_markdown(index=False)
            data_content += "\n\n"
        except Exception as e:
            return f"Error processing DataFrame: {str(e)}"

    # Combine data content with user prompt
    full_prompt = data_content + prompt

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000  # Increased for potential large data content
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {str(e)}"



