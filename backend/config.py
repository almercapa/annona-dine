from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY=os.getenv("SECRET_KEY")
REDIRECT_URI="http://localhost:8000/auth/google/callback"
ALGORITHM = "RS256"  # for decoding Google's token
JWT_ALGORITHM = "HS256"  # for encoding Annona's token