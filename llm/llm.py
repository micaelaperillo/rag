import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

from core.models.recommendation import RecommendationList


class OpenAILLM:

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7, max_tokens: Optional[int] = None):
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate_text(self, prompt: str, system_message: Optional[str] = None) -> str:
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")

    def generate_recommendations(self, prompt: str, system_message: Optional[str] = None) -> str:
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.parse(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format=RecommendationList
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
        
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Perform chat completion with a list of messages.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys.
            
        Returns:
            str: The generated response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
    
    def generate_with_context(self, query: str, context: str, system_message: Optional[str] = None) -> str:
        """
        Generate a response using the provided context.
        
        Args:
            query (str): The user's question or request.
            context (str): Relevant context information.
            system_message (Optional[str]): Optional system message.
            
        Returns:
            str: The generated response.
        """
        prompt = f"Context: {context}\n\nQuestion: {query}"
        return self.generate_text(prompt, system_message)
    
    def set_parameters(self, temperature: Optional[float] = None, max_tokens: Optional[int] = None):
        """
        Update model parameters.
        
        Args:
            temperature (Optional[float]): New temperature value.
            max_tokens (Optional[int]): New max_tokens value.
        """
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dict[str, Any]: Model configuration information.
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }


