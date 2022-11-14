from app import app
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', encoding='UTF-8', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    app.run()