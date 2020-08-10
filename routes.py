from app import *
from models import *
from method import *



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['psw']
        user = User(user_name, password)

        if user.is_username_valid():
            if user.is_password_valid():
                flash('Logged in')
                return redirect(url_for('home_page', user_id=user.get_user_id()[0], username=user_name))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/<username>/user_id-<user_id>/home-page', methods=['GET'])
def home_page(username, user_id):

    if request.method == 'GET':
        categories = get_all_categories()
        result = [dict(row) for row in categories]
        return jsonify(result)
