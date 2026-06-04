from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "team_star_pro_mode"

# --- DATABASE SETUP ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team_star_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# --- DATABASE SETUP ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team_star_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# --- UPLOAD FOLDER ---
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(UPLOAD_FOLDER, 'strategies'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'achievements'), exist_ok=True)

# --- MODELS (Database Tables) ---

class Scrim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    time = db.Column(db.String(20))
    entry_fee = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    profit = db.Column(db.Integer)

class StrategyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) # meta, drop, rotation
    filename = db.Column(db.String(100))

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    title = db.Column(db.String(100))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    player_name = db.Column(db.String(50))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html', active_page='home')

# --- FUNDS & HISTORY ---
@app.route('/funds')
def funds():
    all_scrims = Scrim.query.all()
    total_fund = sum(scrim.profit for scrim in all_scrims)
    return render_template('funds.html', total_fund=total_fund, active_page='funds')

@app.route('/history')
def history():
    all_scrims = Scrim.query.order_by(Scrim.id.desc()).all()
    return render_template('history.html', scrims=all_scrims, active_page='funds')

@app.route('/delete_scrim/<int:id>')
def delete_scrim(id):
    if session.get('is_admin'):
        scrim = Scrim.query.get(id)
        db.session.delete(scrim)
        db.session.commit()
    return redirect(url_for('history'))

@app.route('/add_scrim', methods=['POST'])
def add_scrim():
    if not session.get('is_admin'): return redirect(url_for('funds'))
    fee = int(request.form.get('entry_fee'))
    rank = int(request.form.get('rank'))
    profit = int(request.form.get('profit')) if rank <= 3 else -fee
    new_scrim = Scrim(date=request.form.get('date'), time=request.form.get('time'), entry_fee=fee, rank=rank, profit=profit)
    db.session.add(new_scrim)
    db.session.commit()
    return redirect(url_for('funds'))

# --- STRATEGIES & UPLOADS ---
@app.route('/strategies')
def strategies():
    return render_template('strategies.html', active_page='strategies')

@app.route('/strategy_view/<category>')
def strategy_view(category):
    images = StrategyImage.query.filter_by(category=category.lower()).all()
    comments = Comment.query.filter_by(category=category.lower()).order_by(Comment.id.desc()).all()
    return render_template('strategy_view.html', category=category.upper(), images=images, comments=comments, active_page='strategies')

@app.route('/upload_strategy', methods=['GET', 'POST'])
def upload_strategy():
    if not session.get('is_admin'): return redirect(url_for('strategies'))
    if request.method == 'POST':
        category = request.form.get('category')
        files = request.files.getlist('strategy_images') # Multiple images
        for file in files:
            if file:
                filename = f"{datetime.now().timestamp()}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'strategies', filename))
                db.session.add(StrategyImage(category=category, filename=filename))
        db.session.commit()
        return redirect(url_for('strategies'))
    return render_template('upload_strategy.html')

# --- ACHIEVEMENTS ---
@app.route('/achievements')
def achievements():
    all_ach = Achievement.query.all()
    return render_template('achievements.html', achievements=all_ach, active_page='achievements')

@app.route('/upload_achievement', methods=['POST'])
def upload_achievement():
    if session.get('is_admin'):
        file = request.files.get('ach_image')
        title = request.form.get('title')
        if file:
            filename = f"ach_{datetime.now().timestamp()}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'achievements', filename))
            db.session.add(Achievement(filename=filename, title=title))
            db.session.commit()
    return redirect(url_for('achievements'))

@app.route('/delete_achievement/<int:id>')
def delete_achievement(id):
    if session.get('is_admin'):
        ach = Achievement.query.get(id)
        db.session.delete(ach)
        db.session.commit()
    return redirect(url_for('achievements'))

# --- COMMENTS/CHAT ---
@app.route('/add_comment/<category>', methods=['POST'])
def add_comment(category):
    name = request.form.get('playerName')
    msg = request.form.get('playerMessage')
    if name and msg:
        db.session.add(Comment(category=category.lower(), player_name=name, message=msg))
        db.session.commit()
    return redirect(url_for('strategy_view', category=category))

@app.route('/delete_comment/<int:id>/<category>')
def delete_comment(id, category):
    if session.get('is_admin'):
        comment = Comment.query.get(id)
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('strategy_view', category=category))

# --- AUTH ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'star123':
            session['is_admin'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))
# --- STRATEGY IMAGE DELETE LOGIC ---
@app.route('/delete_strategy_image/<int:id>/<category>')
def delete_strategy_image(id, category):
    if session.get('is_admin'):
        img = StrategyImage.query.get(id)
        if img:
            # File ko folder se delete karna
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'strategies', img.filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"File delete error: {e}")
            
            # Database se entry delete karna
            db.session.delete(img)
            db.session.commit()
            flash("Image removed from Intel.")
    return redirect(url_for('strategy_view', category=category))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
