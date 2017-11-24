import os, sys
from app import db


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


if __name__ == '__main__':
    db.create_all()