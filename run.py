from config import ProductionConfig, TestConfig
from create import create_app
import os

app = create_app(TestConfig)

if __name__ == "__main__":
    app.run(debug=True)