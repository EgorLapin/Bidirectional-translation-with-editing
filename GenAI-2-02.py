from transformers import pipeline
from typing import Optional
import sys

from translator import translate_en, translate_ru, _validate_text

def improve_russian_text(russian_text: str) -> str:
    """
    Allows the user to manually edit the Russian translation, or applies simple automatic improvements.
    This version uses an AI model to suggest an improved Russian text, and allows the user to accept or further edit it.
    """
    print(f"Original Russian translation: {russian_text}")

    try:
        # Translate Russian to English
        synthetic_en = translate_ru(russian_text)
        # Translate back to Russian (paraphrased)
        ai_improved_ru = translate_en(synthetic_en)
        print(f"AI-suggested improved Russian: {ai_improved_ru}\n")
    except Exception as e:
        print(f"AI improvement failed: {e}")
        ai_improved_ru = russian_text

    # Allow user to accept, edit, or keep original
    print("Press Enter to accept the AI suggestion, or edit the Russian text as desired.\n")
    improved = input(f"Edit Russian text (leave blank to accept AI suggestion): ").strip()
    if improved:
        return improved
    elif ai_improved_ru != russian_text:
        return ai_improved_ru
    else:
        return russian_text

def bidirectional_translation_loop(original_en: str, max_iterations: int = 5):
    """
    Performs iterative bidirectional translation and improvement.

    Args:
        original_en (str): The original English text.
        max_iterations (int): Maximum number of improvement iterations.
    """
    current_en = original_en
    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---\n")
        # 1. Translate en → ru
        ru = translate_en(current_en)
        print(f"English → Russian: {ru}\n")

        # 2. Translate ru → en
        back_en = translate_ru(ru)
        print(f"Russian → English: {back_en}\n")

        # 3. Compare with original
        print(f"Original English: {original_en}")
        print(f"Back-translated English: {back_en}\n")
        if back_en.strip().lower() == original_en.strip().lower():
            print("Back-translation matches the original. Stopping iteration.")
            break

        # 4. Improve Russian text
        ru = improve_russian_text(ru)

        # 5. Prepare for next iteration
        current_en = translate_ru(ru)

        # Ask user if they want to continue to the next iteration
        if iteration < max_iterations:
            user_input = input("Do you want to continue to the next iteration? (y/n): ").strip().lower()
            if user_input not in ("y", "yes", ""):
                print("Stopping iteration by user request.")
                break


def main():
    test_text = "Hello, how are you"

    bidirectional_translation_loop(test_text)


if __name__ == "__main__":
    main()