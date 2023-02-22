from flask import Flask, request, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import uuid
import base64
from PIL import Image
import io


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/coding_thunder"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# user model


class User(db.Model):
    '''
    this class creates users
    '''
    si_no = db.Column(db.Integer, unique=True,
                      primary_key=True, nullable=False)
    id = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(12), unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)

# blog model


class Blog(db.Model):
    '''
    this class creates blogs
    '''
    si_no = db.Column(db.Integer, unique=True,
                      primary_key=True, nullable=False)
    id = db.Column(db.Text, unique=True, nullable=False)
    thumbnail = db.Column(db.LargeBinary, unique=False, nullable=False)
    title = db.Column(db.Text, unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    view = db.Column(db.Integer, unique=False, nullable=False)

    def serialize(self):
        return {
            "si_no": self.si_no,
            'id': self.id,
            'thumbnail': base64.b64encode(self.thumbnail).decode('utf-8'),
            'title': self.title,
            'description': self.description,
        }


# create all the db model
with app.app_context():
    db.create_all()


def new_uuid():
    '''
    Generates a new id every time
    '''
    unique_id = str(uuid.uuid4())
    return unique_id


@app.route('/')
def home():
    '''
    home route to show the home page
    '''
    return render_template('index.html')


@app.route('/blogs')
def blogs():
    '''
    blogs route to show the blog page
    '''
    return render_template('blogs.html')


@app.route('/contact-us')
def contact():
    '''
    contact us route to show the contact page
    '''
    return render_template('contact.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    '''
    registration route to show the registration page
    '''
    if request.method == 'POST':
        '''
        if user make a post request to registration route then get the data from input value , verify the entered email is already exist or not. If email already exist ten show an error message, else generate a hashed of user password and save the user to the database
        '''
        try:
            data = request.get_json()
            user_name, user_address, user_email, user_password = data.values()

            user = User.query.filter_by(email=user_email).first()

            if user:
                data = {'message': 'Email already exist!'}
                response = make_response(jsonify(data), 409)
                return response
            else:

                hashed_password = bcrypt.generate_password_hash(
                    user_password, 12)

                user = User(
                    id=new_uuid(),
                    name=user_name,
                    address=user_address,
                    email=user_email,
                    password=hashed_password,
                )
                db.session.add(user)
                db.session.commit()

                data = {'message': 'Status OK'}
                response = make_response(jsonify(data), 201)
                return response

        except Exception as e:
            print(f'error in registration post request - {e}')

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    login route to show the login page
    '''
    try:

        if request.method == 'POST':
            '''
            if user make a post request to login route then get the entered value from the input and check is there any user has registered or not. if user found then check the password with the saved hashed password and then login the user. else give an error message
            '''
            data = request.get_json()
            user_email, user_password = data.values()
            user = User.query.filter_by(email=user_email).first()

            password = user.password
            verify_password = bcrypt.check_password_hash(
                password, user_password)

            if user and verify_password:
                data = {'message': 'Status OK'}
                response = make_response(jsonify(data), 200)
                return response

    except Exception as e:
        print(f'Error from login - {e}')
        data = {'message': 'Bad request'}
        response = make_response(jsonify(data), 404)
        return response

    return render_template('login.html')


@ app.route('/dashboard')
def dashboard():
    '''
    dashboard route to show the dashboard page
    '''
    return render_template('dashboard.html')


@ app.route('/create/blog', methods=['GET', 'POST'])
def create_blog():
    '''
    blog create route to show the blog create page and create a new blog
    '''
    if request.method == 'POST':
        '''
        if create blog get a post request then get the input values and convert image file size to 50kib size and then create a new blog to database
        '''
        try:
            file = request.files['file']
            title = request.form.get('title')
            description = request.form.get('description')

            file = request.files['file']
            image = Image.open(file.stream)
            image = image.resize((1440, 720))
            image = image.convert('RGB')
            buffer = io.BytesIO()

            image.save(buffer, format='JPEG', quality=50)
            image_data = buffer.getvalue()

            blog = Blog(
                id=new_uuid(),
                thumbnail=image_data,
                title=title,
                description=description,
                view=0
            )
            db.session.add(blog)
            db.session.commit()

            data = {'message': 'Status OK'}
            response = make_response(jsonify(data), 201)
            return response

        except Exception as e:
            print(f'Error from create blog = {e}')
    return render_template('create-blog.html', item=False)


@ app.route('/fetch_blogs')
def fetch_blogs():
    '''
    to get all the blogs from the database and make object to list by serialize function
    '''
    blogs = Blog.query.all()
    serialized_blogs = [blog.serialize() for blog in blogs]

    return jsonify(serialized_blogs), 200


@ app.route('/blog/<title>/<id>')
def fetch_single_blog(title, id):
    '''
    find a single blog from the database based on blog title and id and serialize the blog
    '''
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize()

    blog.view = blog.view + 1
    db.session.commit()

    return render_template('single-blog-page.html', item=(serialized_blog))


@ app.route('/update/<title>/<id>', methods=['GET', 'POST'])
def update_blog(title, id):
    '''
    if admin wants to update the blog then get the blog title and id and then retrive the blog from the database and update the blog if admin click on the update buttonn
    '''
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize()
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')

            blog.title = title
            blog.description = description

            db.session.commit()
            return 'success', 200
        except Exception as e:
            print(f'Error from update route - {e}')

    return render_template('create-blog.html', item=(serialized_blog))


@ app.route('/delete/<title>/<id>')
def delete_blog(title, id):
    ''''
    if admin wants to delete a blog then gate blog title and id and then delete the blog and get all the blog from the datebase and show all the blog
    '''
    blog = Blog.query.filter_by(id=id).first()
    if blog:
        try:
            db.session.delete(blog)
            db.session.commit()

            blogs = Blog.query.all()
            serialized_blog = [blog.serialize() for blog in blogs]

            return render_template('all-blogs.html', item=serialized_blog)
        except Exception as e:
            print(f'Error from delete route - {e}')
            return render_template('all-blogs.html', item=serialized_blog), 403

    return render_template('all-blogs.html', item=serialized_blog)


@ app.route('/all-blogs')
def all_blogs():
    '''
    get the all blogs to show the admin panel 
    '''
    blogs = Blog.query.all()
    serialized_blog = [blog.serialize() for blog in blogs]

    return render_template('all-blogs.html', item=(serialized_blog))


if __name__ == "__main__":
    app.run(debug=True)  # run the server
