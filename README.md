# Rock Paper Scissors Game 🎮

A fun and interactive Rock Paper Scissors game built with Flask!

## Features
- User registration and login system
- Play Rock Paper Scissors against AI
- Track your wins, losses, and high scores
- View detailed game statistics
- Beautiful animated UI

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Start the Flask development server:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## How to Play
1. Register a new account or login
2. Click Rock (✊), Paper (📄), or Scissors (✂️) to make your move
3. First to lose all 3 lives loses the game!
4. View your stats and game history on the stats page

## Project Structure
```
rps-game/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css       # CSS styles
└── templates/
    ├── index.html      # Main game page
    ├── login.html      # Login page
    ├── register.html   # Registration page
    └── stats.html      # Player statistics
```

