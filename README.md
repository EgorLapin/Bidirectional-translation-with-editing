# Bidirectional Translation with Editing

A Python application for iterative translation improvement using bidirectional translation (English ↔ Russian) with AI-powered quality assessment and enhancement. This project demonstrates advanced natural language processing techniques and machine translation optimization using Helsinki-NLP models and Sberbank's GigaChat AI.

## Requirements

### Python Dependencies

The following Python packages are required to run this application:

```
transformers>=4.21.0
torch>=1.12.0
requests>=2.28.0
numpy>=1.21.0
```

### System Requirements

- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux
- Minimum 4GB RAM (recommended for transformer models)
- Internet connection for model downloads and GigaChat API

### API Requirements

- **GigaChat Token**: Optional but recommended for enhanced translation improvement
  - Get a free token at: https://developers.sber.ru/portal/products/gigachat
  - Set environment variable: `GIGACHAT_TOKEN=your_token_here`

## Installation

### Method 1: Using pip (Recommended)

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd Bidirectional-translation-with-editing
   ```

2. Install the required dependencies:
   ```bash
   pip install transformers torch requests numpy
   ```

### Method 2: Using requirements.txt

1. Create a requirements.txt file with the following content:
   ```
   transformers>=4.21.0
   torch>=1.12.0
   requests>=2.28.0
   numpy>=1.21.0
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Using conda

```bash
conda install pytorch transformers requests numpy -c pytorch -c huggingface
```

## Usage

### Basic Usage

1. Run the main translation improvement script:
   ```bash
   python GenAI_2_02.py
   ```

2. Enter the filename containing your English text when prompted:
   ```
   Enter the filename containing the English text (e.g., file.txt): text.txt
   ```

3. The application will perform iterative translation improvement and display results.

### Supported Text Formats

The application supports any text file format, including:
- Plain text (.txt)
- UTF-8 encoded files
- Multi-line text documents

## Implementation Details

### Core Components

- **`translator.py`**: Basic bidirectional translation using Helsinki-NLP models
  - `translate_en()`: English to Russian translation
  - `translate_ru()`: Russian to English translation
  - *Note: This module was adapted from [NSUTasks-GenAI-1-02](https://github.com/serge46b/NSUTasks-GenAI-1-02) as required by the task specifications*

- **`GenAI_2_02.py`**: Advanced iterative translation improvement system
  - `TranslationImprover`: Main class for AI-powered translation enhancement
  - `compare_translations()`: Quality assessment using GigaChat
  - `improve_russian_translation()`: AI-powered translation refinement
  - `iterative_translation_improvement()`: Multi-iteration improvement process

### Translation Models

- **Helsinki-NLP/opus-mt-en-ru**: English to Russian translation
- **Helsinki-NLP/opus-mt-ru-en**: Russian to English translation
- **GigaChat AI**: Quality assessment and translation improvement

## Examples

### Sample Workflow

1. **Input**: "Hello you beautiful people!"
2. **Initial Translation**: "Привет, вы красивые люди!"
3. **Back Translation**: "Hello, you beautiful people!"
4. **Quality Assessment**: Similarity score and improvement suggestions
5. **Iterative Improvement**: Enhanced Russian translation based on AI feedback

### Expected Output Format

```
--- Iteration 1 ---
Russian: Привет, вы красивые люди!
Back-translated: Hello, you beautiful people!
Similarity score: 0.85
Suggestions: Consider improving word choice and sentence structure.
```

## Educational Context

**Novosibirsk State University (NSU)**  
**Bachelor's Program**: 15.03.06 - Mechatronics and Robotics (AI Profile)

*Project Activity Course - Task 2*  
*Generative AI*

## Features

- **Bidirectional Translation**: English ↔ Russian using state-of-the-art models
- **AI-Powered Quality Assessment**: Automatic similarity scoring and improvement suggestions
- **Iterative Improvement**: Multi-round translation enhancement
- **Fallback Mode**: Works without GigaChat API (basic functionality)
- **Error Handling**: Robust error management and user feedback

## Troubleshooting

### Common Issues

1. **Model Download Errors**: Ensure stable internet connection for initial model downloads
2. **Memory Issues**: Close other applications if experiencing memory problems
3. **GigaChat API Errors**: Check token validity and internet connection
4. **File Not Found**: Ensure text file exists in the correct directory

### Performance Tips

- First run may take longer due to model downloads
- Subsequent runs are faster as models are cached
- For large texts, consider breaking into smaller chunks

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is part of an educational curriculum at Novosibirsk State University.