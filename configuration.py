import os.path

PROJECT_ROOT = os.path.dirname(__file__)
TEST_DATA_PATH = os.path.join(PROJECT_ROOT, "test_data")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "logs")

LOGGING_LEVEL = "INFO"

API_USERNAME = "opencart_api_user"
API_KEY = "Re8xUci1xCCWY92AW3KHII6anKVNGDk7mCvrDl00ZY5obatugmqBH2w9CW2geDGUg4D9VxMMkF732Xep8Ee6mcj19CNVL3ggvA5vwvW2BOGrcB9eydWpEWdR3vLKolTDibhAOHDowckHPoNXHJlpbH2UWPYwN3guQKysjlaKxB6pU6mz9baKXYuaOPbmstmXRKyjgCB4nD7wNVPdSVAxYR5wEIFkbNEZu9sO3y336gLlGxLU8boQk1Vwk0KMDcYE"

MYSQL_CREDENTIALS = {
    "user": "bn_opencart",
    "password": "",
    "host": "192.168.1.127",
    "database": "bitnami_opencart",
    "port": "3306",
}
