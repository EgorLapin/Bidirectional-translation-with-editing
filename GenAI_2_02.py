from typing import Optional, Tuple, List
from transformers import pipeline
import requests
import json
import os

from translator import translate_en, translate_ru

# Simple class to store translation results
class TranslationResult:
    def __init__(self, original_en, russian_translation, back_translated_en, similarity_score, improvement_suggestions, iteration):
        self.original_en = original_en
        self.russian_translation = russian_translation
        self.back_translated_en = back_translated_en
        self.similarity_score = similarity_score
        self.improvement_suggestions = improvement_suggestions
        self.iteration = iteration

class TranslationImprover:
    """
    A class that uses Sberbank AI's GigaChat
    to improve Helsinki-NLP translations through iterative back-translation and comparison.
    """
    
    def __init__(self, gigachat_token: Optional[str] = None):
        """
        Initialize the translation improver with GigaChat.
        
        Args:
            gigachat_token: GigaChat API token. If None, will try to get from environment.
        """
        
        self.token = gigachat_token or os.getenv('GIGACHAT_TOKEN')
        
        if not self.token:
            print("No GigaChat token found. Using fallback mode.")
            print("To get a free token: https://developers.sber.ru/portal/products/gigachat")
            self.token = None
        
        # Setup API
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        } if self.token else {}
        
        print("Using Sberbank AI GigaChat for translation improvement")
    
    def _call_gigachat(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Call GigaChat API with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens to generate
            
        Returns:
            The model's response as a string
        """
        if not self.token:
            return self._fallback_response(prompt)
        
        try:
            payload = {
                "model": "GigaChat:latest",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            else:
                print(f"GigaChat API error: {response.status_code}")
                return self._fallback_response(prompt)
                
        except Exception as e:
            print(f"Error calling GigaChat: {e}")
            return self._fallback_response(prompt)
    
    def fallback_response(self, prompt: str) -> str:
        """
        Fallback response when GigaChat is not available.
        
        Args:
            prompt: The original prompt
            
        Returns:
            A simple fallback response
        """
        if "similarity score" in prompt.lower():
            return "SIMILARITY: 0.7\nSUGGESTIONS: Consider improving word choice and sentence structure."
        elif "improve" in prompt.lower() and "russian" in prompt.lower():
            # Extract the current Russian text and return it as-is
            lines = prompt.split('\n')
            for line in lines:
                if "CURRENT RUSSIAN:" in line:
                    return line.split("CURRENT RUSSIAN:")[1].strip().strip('"')
            return "Привет, как дела?"
        else:
            return "I'm sorry, I cannot process this request at the moment."
    
    def compare_translations(self, original: str, back_translated: str) -> Tuple[float, str]:
        """
        Compare original English text with back-translated English text using GigaChat.
        
        Args:
            original: Original English text
            back_translated: Back-translated English text
            
        Returns:
            Tuple of (similarity_score, improvement_suggestions)
        """
        prompt = f"""You are a translation quality assessment expert. Compare these two English texts:

ORIGINAL: "{original}"
BACK-TRANSLATED: "{back_translated}"

Please provide:
1. A similarity score from 0.0 to 1.0 (where 1.0 means identical meaning)
2. Specific suggestions for improving the Russian translation to better preserve the original meaning

Format your response as:
SIMILARITY: [score]
SUGGESTIONS: [your suggestions]"""
        
        try:
            result = self._call_gigachat(prompt, max_tokens=500)
            
            # Parse the response
            similarity_score = 0.5  # Default
            suggestions = "No specific suggestions available."
            
            lines = result.split('\n')
            for line in lines:
                if line.startswith('SIMILARITY:'):
                    try:
                        similarity_score = float(line.split(':')[1].strip())
                    except:
                        pass
                elif line.startswith('SUGGESTIONS:'):
                    try:
                        suggestions = line.split(':', 1)[1].strip()
                    except:
                        pass
            
            return similarity_score, suggestions
            
        except Exception as e:
            print(f"Error in comparison process: {e}")
            return 0.5, f"Error occurred during comparison: {e}"
    
    def improve_russian_translation(self, original_en: str, current_ru: str, suggestions: str) -> str:
        """
        Use GigaChat to improve the Russian translation based on suggestions.
        
        Args:
            original_en: Original English text
            current_ru: Current Russian translation
            suggestions: Improvement suggestions from comparison
            
        Returns:
            Improved Russian translation
        """
        prompt = f"""You are a professional translator. Improve this Russian translation based on the suggestions:

        ORIGINAL ENGLISH: "{original_en}"
        CURRENT RUSSIAN: "{current_ru}"
        IMPROVEMENT SUGGESTIONS: "{suggestions}"

        Provide an improved Russian translation that better preserves the original meaning.
        Return only the improved Russian text, nothing else."""
        
        try:
            result = self._call_gigachat(prompt, max_tokens=200)
            return result.strip()
            
        except Exception as e:
            print(f"Error in GigaChat improvement: {e}")
            return current_ru  # Return original if improvement fails
    
    def iterative_translation_improvement(self,
                                       original_en: str, 
                                       max_iterations: int = 3,
                                       similarity_threshold: float = 0.9) -> List[TranslationResult]:
        """
        Perform iterative translation improvement.
        
        Args:
            original_en: Original English text to translate
            max_iterations: Maximum number of improvement iterations
            similarity_threshold: Stop when similarity reaches this threshold
            
        Returns:
            List of TranslationResult objects for each iteration
        """
        results = []
        current_ru = translate_en(original_en)
        
        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            
            # Back-translate to English
            back_translated_en = translate_ru(current_ru)
            print(f"Russian: {current_ru}")
            print(f"Back-translated: {back_translated_en}")
            
            # Compare with original
            similarity_score, suggestions = self.compare_translations(original_en, back_translated_en)
            print(f"Similarity score: {similarity_score:.2f}")
            print(f"Suggestions: {suggestions}")
            
            # Store result
            result = TranslationResult(
                original_en=original_en,
                russian_translation=current_ru,
                back_translated_en=back_translated_en,
                similarity_score=similarity_score,
                improvement_suggestions=suggestions,
                iteration=iteration + 1
            )
            results.append(result)
            
            # Check if we've reached the threshold
            if similarity_score >= similarity_threshold:
                print(f"Target similarity ({similarity_threshold}) reached!")
                break
            
            # Improve the Russian translation
            if iteration < max_iterations - 1:  # Don't improve on last iteration
                print("Improving Russian translation...")
                current_ru = self.improve_russian_translation(original_en, current_ru, suggestions)
                print(f"Improved Russian: {current_ru}")
        
        return results

def main():
    """
    Main function to demonstrate the translation improvement system using GigaChat.
    """
    try:
        print("Starting Translation Improvement System with GigaChat")
        print("=" * 60)
        
        # Initialize the improver
        improver = TranslationImprover()
        
        # Test with a sample text
        while True:
            filename = input("Enter the filename containing the English text (e.g., file.txt): ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    test_text = f.read().strip()
                break
            except FileNotFoundError:
                print(f"File '{filename}' not found. Please try again.")
            except Exception as e:
                print(f"Error reading file: {e}. Please try again.")
                
        print(f"\nOriginal English: {test_text}")
        print("\nStarting iterative translation improvement...")
        
        # Perform iterative improvement
        results = improver.iterative_translation_improvement(
            original_en=test_text,
            max_iterations=3,
            similarity_threshold=0.85
        )
        
        # Show the best result
        best_result = max(results, key=lambda x: x.similarity_score)
        print(f"\nBest result (similarity: {best_result.similarity_score:.2f}):")
        print(f"  Final Russian translation: {best_result.russian_translation}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nTroubleshooting tips:")
        print("1. Get a free GigaChat token: https://developers.sber.ru/portal/products/gigachat")
        print("2. Set environment variable: set GIGACHAT_TOKEN=your_token_here")

if __name__ == "__main__":
    main()