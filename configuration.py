import os

class ConfigurationVariables:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    JWT_SECRET = "kjyFUYRFUKJn98y986fiVJHFCYRu79hbjGFCGRESZYT76tfrwzGFDXCHGF"
    SQLITE3_DATABASE = BASEDIR + "/database.db"