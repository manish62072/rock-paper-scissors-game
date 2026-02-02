from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    high_score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to game records
    game_records = db.relationship('GameRecord', backref='player', lazy=True)

# Game Record Model
class GameRecord(db.Model):
    __tablename__ = 'game_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player_choice = db.Column(db.String(20), nullable=False)
    computer_choice = db.Column(db.String(20), nullable=False)
    result = db.Column(db.String(20), nullable=False)  # 'win', 'loss', 'draw'
    player_lives_remaining = db.Column(db.Integer, nullable=False)
    computer_lives_remaining = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validation
        if not username or not email or not password:
            error = "All fields are required!"
        elif len(username) < 3:
            error = "Username must be at least 3 characters long!"
        elif len(password) < 6:
            error = "Password must be at least 6 characters long!"
        elif password != confirm_password:
            error = "Passwords don't match!"
        else:
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            
            if existing_user:
                error = "Username already exists!"
            elif existing_email:
                error = "Email already registered!"
            else:
                try:
                    # Create new user
                    new_user = User(
                        username=username,
                        email=email,
                        password=password,  # In production, use proper hashing!
                        high_score=0,
                        games_played=0,
                        wins=0,
                        losses=0
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    success = "Account created successfully! You can now login."
                    return render_template("register.html", error=error, success=success)
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred during registration!"
    
    return render_template("register.html", error=error, success=success)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    success = None
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        if not username or not password:
            error = "Username and password are required!"
        else:
            user = User.query.filter_by(username=username).first()
            
            if user and user.password == password:
                session['user_id'] = user.id
                session['username'] = user.username
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                error = "Invalid username or password!"
    
    return render_template("login.html", error=error, success=success)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
def index():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Initialize lives if not in session
    if "user_lives" not in session:
        session["user_lives"] = 3
        session["computer_lives"] = 3

    result = None
    user_choice = None
    computer_choice = None
    choices = ["rock", "paper", "scissors"]

    if request.method == "POST":
        user_choice_str = request.form.get("choice")
        if not user_choice_str:
            result = "Please select Rock, Paper, or Scissors!"
        else:
            # Convert string choice to number (0=rock, 1=paper, 2=scissors)
            user_choice = choices.index(user_choice_str)
            computer_choice = random.randrange(3)
            
            # Game logic
            round_result = None
            if user_choice == computer_choice:
                result = "It's a draw!"
                round_result = "draw"
            elif (
                (user_choice == 0 and computer_choice == 2) or
                (user_choice == 1 and computer_choice == 0) or
                (user_choice == 2 and computer_choice == 1)
            ):
                session["computer_lives"] -= 1
                result = "You won this round!"
                round_result = "win"
            else:
                session["user_lives"] -= 1
                result = "Computer won this round!"
                round_result = "loss"

            # Record the game move
            try:
                game_record = GameRecord(
                    user_id=session.get('user_id'),
                    player_choice=choices[user_choice],
                    computer_choice=choices[computer_choice],
                    result=round_result,
                    player_lives_remaining=session["user_lives"],
                    computer_lives_remaining=session["computer_lives"]
                )
                db.session.add(game_record)
                db.session.commit()
            except Exception as e:
                print(f"Error recording game: {e}")

            # Check for game over
            if session["user_lives"] == 0 or session["computer_lives"] == 0:
                # Update user stats
                user = User.query.get(session.get('user_id'))
                if user:
                    user.games_played += 1
                    if session["user_lives"] == 0:
                        result += " Game Over! Computer wins!"
                        user.losses += 1
                    else:
                        result += " Congratulations! You win!"
                        user.wins += 1
                        if session["computer_lives"] > user.high_score:
                            user.high_score = session["computer_lives"]
                    db.session.commit()
                
                # Reset lives for next game
                session.pop("user_lives")
                session.pop("computer_lives")

    return render_template(
        "index.html",
        result=result,
        user_choice=user_choice,
        computer_choice=computer_choice,
        user_lives=session.get("user_lives"),
        computer_lives=session.get("computer_lives"),
        username=session.get("username")
    )

# Stats route
@app.route("/stats")
def stats():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user = User.query.get(session.get('user_id'))
    game_records = GameRecord.query.filter_by(user_id=session.get('user_id')).all()
    
    return render_template(
        "stats.html",
        user=user,
        game_records=game_records
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)

