import os
from interndashboard import create_app

app = create_app()
app.secret_key = os.environ.get('secret_key')

if __name__ == '__main__':
    app.run(debug=True)