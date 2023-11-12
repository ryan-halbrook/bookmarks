from bookmarks import create_app
import os

if __name__ == "__main__":
    create_app().run(
            debug=os.environ.get('DEBUG', False),
            host=os.environ.get('HOST', '127.0.0.1'),
            port=os.environ.get('PORT', 5000))
