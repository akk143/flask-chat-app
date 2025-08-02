from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit, join_room
from models import db, User, Message, Conversation
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
socketio = SocketIO(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('chat'))
        else:
            error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip().capitalize()
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            error = "Username already exists."
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    users = User.query.filter(User.id != session['user_id']).all()
    current_user = User.query.get(session['user_id'])
    return render_template('chat.html', users=users, current_username=current_user.username)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    messages = Message.query.filter_by(conversation_id=room).order_by(Message.timestamp).all()
    history = [{'sender': msg.sender.username, 'content': msg.content} for msg in messages]
    emit('chat_history', history)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    content = data['content']
    sender_id = session['user_id']
    msg = Message(content=content, sender_id=sender_id, conversation_id=room)
    db.session.add(msg)
    db.session.commit()
    sender = User.query.get(sender_id)
    emit('receive_message', {'sender': sender.username, 'content': content}, room=room)

@app.route('/start_conversation/<int:user_id>')
def start_conversation(user_id):
    current_user_id = session['user_id']
    conv = Conversation.query.filter(Conversation.users.any(id=current_user_id),
                                     Conversation.users.any(id=user_id)).first()
    if not conv:
        conv = Conversation()
        conv.users.append(User.query.get(current_user_id))
        conv.users.append(User.query.get(user_id))
        db.session.add(conv)
        db.session.commit()
    return {'room': conv.id}

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/delete_user/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username.capitalize()).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"User {username} deleted."
    return "User not found."

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)

