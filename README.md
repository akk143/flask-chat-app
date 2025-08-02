# flask-chat-app

A simple real-time messaging web application built with **Flask**, **Flask-SocketIO**, and **SQLAlchemy**.  
Users can sign up, log in, and chat with other users in real time.

## ✨ Features
- User registration and login (with secure password hashing)
- Real-time private chat using Socket.IO
- Conversation history saved in a SQLite database
- View list of other users and start private conversations
- Simple admin route to delete users

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/akk143/flask-chat-app.git
cd flask-chat-app


2. Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate        # On Windows use: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt


4. Run the app
python app.py


** By default, the app runs on: http://localhost:5001 **