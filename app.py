import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Configure database
database_url = os.environ.get('DATABASE_URL', '')
if not database_url:
    database_url = f"postgresql://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}"

if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Configure session for production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SESSION_COOKIE_SECURE'] = False  # Changed to False for local development
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev-key'),
    SQLALCHEMY_DATABASE_URI=database_url,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

logger.info(f"Using database URL: {database_url}")

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes
from routes import *

# Initialize database tables
with app.app_context():
    try:
        db.engine.connect()
        logger.info("Database connection successful")
        db.create_all()
        logger.info("All database tables created successfully")
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)