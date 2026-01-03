# NCERT-CHAT-Bot

This project is an AI-powered chatbot designed to help users interact with and access NCERT books and educational content. It provides a conversational interface for students, teachers, and anyone interested in NCERT materials.

## Features
- Access to NCERT books (currently includes Class 9 Hindi: Kritika, Kshitij, Sparsh)
- Organized book structure for easy navigation
- Ready for integration with AI/ML models for Q&A, summarization, and more

## Project Structure
```
app.py                # Main application file
Books/                # Directory containing NCERT books
  CLASS 9TH/
    Hindi/
      KRTIKA/
      Kshitij/
      SPARSH/
```

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/alokkmohan/NCERT-CHAT-Bot.git
   cd NCERT-CHAT-Bot
   ```
2. Install dependencies (if any, e.g., Python packages listed in requirements.txt).
3. Run the application:
   ```bash
   python app.py
   ```

## Environment Variables
- Create a `.env` file for your API keys and secrets. **Do not commit this file.**
- Example:
  ```env
  GROQ_API_KEY=your_api_key_here
  ```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
