# LowChol Agent 🥗

An AI-powered tool to analyze cholesterol risk in food dishes using OCR and natural language processing.

## Features

- 🔍 **Dish Analysis**: Analyze any dish name for cholesterol/saturated fat risk
- 📱 **OCR Support**: Extract text from menu images and analyze multiple dishes
- 🤖 **AI-Powered**: Uses GPT-4o-mini for intelligent ingredient extraction
- 📊 **Risk Scoring**: Categorizes dishes as 🟢 Low, 🟡 Medium, or 🔴 High risk

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/shadmau/lowchol-agent
   cd lowchol-agent
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv

   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install the package and dependencies**:

   ```bash
   pip install -e .
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.sample .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Usage

### Analyze a Single Dish

```bash
lowchol-agent "Grilled Chicken Caesar Salad"
```

### Analyze Menu from Image

```bash
lowchol-agent --ocr menu_image.jpg
```

### Examples

```bash
# Analyze various dishes
lowchol-agent "Bacon Cheeseburger"
lowchol-agent "Quinoa Buddha Bowl"
lowchol-agent "Creamy Mushroom Risotto"

# Process a restaurant menu
lowchol-agent --ocr examples/test_menu.png
```

### Alternative: Direct Script Usage

If you prefer not to install the package, you can also run:

```bash
python main.py "Dish Name"
python main.py --ocr image_path.jpg
```

## How It Works

1. **Ingredient Extraction**: Uses AI to identify likely ingredients from dish names
2. **Risk Assessment**: Scores ingredients based on saturated fat content:
   - **High Risk** (🔴): Butter, cream, cheese, red meat, etc.
   - **Low Risk** (🟢): Vegetables, legumes, lean proteins, etc.
   - **Medium Risk** (🟡): Mixed ingredients
3. **OCR Processing**: Extracts text from images using PaddleOCR
4. **Batch Analysis**: Processes multiple dishes from menu images

## Project Structure

```
lowchol-agent/
├── src/
│   └── lowchol_agent/
│       ├── __init__.py
│       ├── agent.py              # Main agent orchestration
│       ├── dish_analyzer.py      # Ingredient extraction
│       ├── cholesterol_scorer.py # Risk scoring logic
│       └── ocr_processor.py      # Image text extraction
├── examples/                     # Sample images
├── tests/                        # Unit tests
├── main.py                       # CLI interface
├── requirements.txt              # Dependencies
├── setup.py                      # Package configuration
├── .env.sample                   # Environment template
└── README.md                     # This file
```

## Dependencies

- **LangChain**: AI agent framework
- **OpenAI**: GPT-4o-mini for ingredient analysis
- **PaddleOCR**: Text extraction from images
- **Pillow**: Image processing
- **python-dotenv**: Environment variable management
