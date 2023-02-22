# Flask Blog Website

This is a blog website created using Flask, JavaScript, HTML, and SCSS. The website allows users to register, login, create posts, update posts, and delete posts.

## Requirements

To run this website, you need to have the following installed:

- Python (version 3.6 or higher)
- Flask (version 1.1.2 or higher)
- Flask-Bcrypt (version 0.7.1 or higher)
- Flask-SQLAlchemy
- Flask-WTF
- Pillow

## Installation

1. Clone the repository:
   git clone https://github.com/your_username/flask-blog-website.git

2. Create a virtual environment:
   python -m venv env

3. Activate the virtual environment:

- On Windows:
  env\Scripts\activate

- On macOS or Linux:
  source env/bin/activate

4. Install the required packages:
   pip install -r requirements.txt

5. Create the database:
   python
   > > > from app import db
   > > > db.create_all()
   > > > exit()

## Usage

#### To run the website, execute the following command:

python app.py
Then, go to http://localhost:5000/ in your web browser to access the website.

## Features

- User registration
- User login/logout
- Create posts
- Update posts
- Delete posts
- View all posts
- View individual posts

## Technologies

This website was built using the following technologies:

- Flask
- Flask-Bcrypt
- Flask-SQLAlchemy
- Pillow
- JavaScript
- HTML
- SCSS

## Contribution

Feel free to fork the repository and contribute to this project by submitting a pull request. Any contributions, whether they are bug fixes or new features, are greatly appreciated!

## Licensing

This project has no License.

## Contact

If you have any questions or suggestions, feel free to contact me at [mdp020479@gmail.com](mailto:mdp020479@gmail.com)
