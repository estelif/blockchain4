import ollama
from typing import Optional

def generate_ai_response(prompt: str, context: str = "", format_instructions: str = "markdown") -> Optional[str]:
    """
    Generate AI response using Ollama with improved error handling
    
    Args:
        prompt: User question
        context: Contextual information for the AI
        
    Returns:
        Generated response or None if error occurs
    """
    full_prompt = f"""
    **Role**: You are an expert AI assistant specializing in cryptocurrency and blockchain technology.
    
    **Context**: {context}
    
    **User Question**: {prompt}
    
    **Response Requirements**:
    - Answer in {format_instructions} format
    - Provide comprehensive, accurate information
    - Use bullet points for lists
    - Include examples when appropriate
    - Highlight key terms in bold
    - Maintain professional yet accessible tone
    - Structure response with clear sections if needed
    
    **Response**:
    """
    
    try:
        response = ollama.generate(
            model='llama3:8b',
            prompt=full_prompt,
            options={
                'temperature': 0.7,
                'top_p': 0.9
            }
        )
        return response['response']
    except Exception as e:
        print(f"Error generating AI response: {str(e)}")
        return None