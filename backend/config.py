from dotenv import load_dotenv # used to load env file
import os # used to interact with operating system, specifically env file

load_dotenv() # loads env file
CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID") # defines name of the app to Google
CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET") # app password for verification to Google
SECRET_KEY=os.getenv("SECRET_KEY") # for signing Annona's JWTs
REDIRECT_URI="http://localhost:8000/auth/google/callback" # for site redirecting
ALGORITHM = "RS256"  # for decoding Google's token
JWT_ALGORITHM = "HS256"  # for encoding Annona's token