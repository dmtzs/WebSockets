try:
    from flask import Flask
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

app = Flask(__name__)

from app import routes, error_handlers