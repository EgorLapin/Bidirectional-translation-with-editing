from transformers import pipeline
from typing import Optional
import sys


print("Initializing models...")
try:
    pipe_en2ru = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
    pipe_ru2en = pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en")
except Exception as e:
    print(f"Error occured while downloading model: {e}")
    sys.exit(1)
    

def _validate_text(text: Optional[str]) -> str:
	if not isinstance(text, str) or not text.strip():
		raise ValueError("Input text must be a non-empty string.")
	return text


def translate_en(en: str) -> str:
    """
    Translates English text to Russian.

    Args:
        en (str): The English text to translate.

    Returns:
        str: The translated Russian text.
    """
    en = _validate_text(en)
    return pipe_en2ru(en)[0]['translation_text']

def translate_ru(ru: str) -> str:
    """
    Translates Russian text to English.

    Args:
        ru (str): The Russian text to translate.

    Returns:
        str: The translated English text.
    """
    ru = _validate_text(ru)
    return pipe_ru2en(ru)[0]['translation_text']

def main():
    try:
        test_text = "Hello, how are you"
        print(f"Translating test phrase '{test_text}' from English to Russian...")
        translation_result = translate_en(test_text)
        print(f"Result:{translation_result}")
        back_translation_result = translate_ru(translation_result)
        print(f"Back translation result: {back_translation_result}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()