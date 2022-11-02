import unittest
from project import db, create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=False)
    # app.run()
