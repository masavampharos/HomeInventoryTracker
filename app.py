import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure MySQL connection
mysql_user = os.environ.get('MYSQL_USER', 'masavampharos')  # PythonAnywhereのユーザー名
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_host = 'masavampharos.mysql.pythonanywhere-services.com'
mysql_database = os.environ.get('MYSQL_DATABASE', 'masavampharos$default')  # データベース名

# Set Flask configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False  # デバッグモードをオフに

logger.info(f"Connecting to database at: {mysql_host}")
logger.info(f"Using database: {mysql_database}")
logger.info(f"Using user: {mysql_user}")

# Initialize SQLAlchemy
db = SQLAlchemy(app)

try:
    with app.app_context():
        db.create_all()
    logger.warning("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)