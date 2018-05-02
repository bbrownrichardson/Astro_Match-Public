from flask import Flask, jsonify, request, render_template, redirect
from flask.views import MethodView
import os
from db_module import DBHandler

DB = DBHandler()

app = Flask(__name__)


@app.cli.command('initdb')
def initiate_command():
    DB.initdb_command()


class RequestError(Exception):
    """
    This custom exception class is for easily handling errors in requests,
    such as when the user provides an ID that does not exist or omits a
    required field.
    """

    def __init__(self, status_code, error_message):
        # Call the parent class's constructor. Unlike in C++, this does not
        # happen automatically in Python.
        Exception.__init__(self)

        self.status_code = str(status_code)
        self.error_message = error_message

    def to_response(self):
        """
        Create a Response object containing the error message as JSON.
        :return: the response
        """

        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from a RequestError.
    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


class RegisterView(MethodView):

    @staticmethod
    def get():
        return render_template('Register.html')

    @staticmethod
    def post():
        if 'gender' not in request.form:
            raise RequestError(422, 'gender required')
        if 'sign' not in request.form:
            raise RequestError(422, 'sign required')
        if 'name' not in request.form:
            raise RequestError(422, 'name required')
        if 'age' not in request.form:
            raise RequestError(422, 'age required')
        if 'preference' not in request.form:
            raise RequestError(422, 'preference required')
        if 'bio' not in request.form:
            raise RequestError(422, 'bio required')
        DB.post(request.form['gender'], request.form['sign'],
                request.form['name'], request.form['age'],
                request.form['preference'], request.form['bio'])
        return redirect("/")


class AllUsers(MethodView):
    @staticmethod
    def get():
        if request.cookies.get('registered') is None:
            return render_template('Register.html')
        else:
            print('Return User')
        users = DB.get_all_users()
        return render_template('ViewAll.html', users=users)


class OneUser(MethodView):

    @staticmethod
    def get(uid):
        user = DB.get_by_id(uid)
        return render_template('ViewOne.html', user=user)


class APIView(MethodView):
    @staticmethod
    def get(uid):
        if(uid is not None):
            # Get one user
            user = DB.get_by_id(uid)
            return jsonify(user)
        else:
            # Get all users
            users = DB.get_all_users()
            return jsonify(users)

    @staticmethod
    def post():
        if 'gender' not in request.form:
            raise RequestError(422, 'gender required')
        if 'sign' not in request.form:
            raise RequestError(422, 'sign required')
        if 'name' not in request.form:
            raise RequestError(422, 'name required')
        if 'age' not in request.form:
            raise RequestError(422, 'age required')
        if 'preference' not in request.form:
            raise RequestError(422, 'preference required')
        if 'bio' not in request.form:
            raise RequestError(422, 'bio required')
        DB.post(request.form['gender'], request.form['sign'],
                request.form['name'], request.form['age'],
                request.form['preference'], request.form['bio'])
        return jsonify({'result': 'success'})


# Register RegisterView as the handler for all the /register/ requests
register_view = RegisterView.as_view('register_view')
app.add_url_rule('/register/', view_func=register_view, methods=['GET'])
app.add_url_rule('/register/', view_func=register_view, methods=['POST'])


# Register SignsView as the handler for all the /signs/ requests
all_users_view = AllUsers.as_view('all_users_view')
app.add_url_rule('/', view_func=all_users_view, methods=['GET'])
app.add_url_rule('/users/', view_func=all_users_view, methods=['GET'])

# Register GendersView as the handler for all the /genders/ requests
one_user_view = OneUser.as_view('one_user_view')
app.add_url_rule('/users/<int:uid>', view_func=one_user_view,
                 methods=['GET'])

# Register API as the handler for all the /genders/ requests
api_view = APIView.as_view('api_view')
app.add_url_rule('/api/users/', view_func=api_view, methods=['GET'],
                 defaults={'uid': None})
app.add_url_rule('/api/users/<int:uid>', view_func=api_view, methods=['GET'])
app.add_url_rule('/api/register/', view_func=api_view, methods=['POST'])
