import psycopg2
from datetime import datetime

connection = psycopg2.connect(
    dbname="BLOG",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432,
)
cursor = connection.cursor()

date_pub = datetime.now()


UPLOAD_FOLDER = "core/static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_posts(search=None):
    if search:
        cursor.execute(
            f"""
            SELECT posts.id, title, description, username, date_pub FROM posts INNER JOIN users ON posts.author_id=users.id WHERE title LIKE '%{search}%';
            """
        )
    else:
        cursor.execute(
            """
            SELECT posts.id, title, description, username, date_pub FROM posts INNER JOIN users ON posts.author_id=users.id;
            """
        )
    posts = cursor.fetchall()
    return posts


def save_post(title, description):

    cursor.execute(
        """
        INSERT INTO posts (title, description, author_id, date_pub)
        VALUES (%s, %s, 1, %s);
        """,
        (title, description, date_pub),
    )
    connection.commit()


def get_post(id):
    cursor.execute(
        """
        SELECT * FROM posts
        
        """,
    )
    post = cursor.fetchone()
    return post


def del_post(id):
    cursor.execute(
        """
        DELETE FROM posts WHERE id= (%s);
        """,
        (id,),
    )
    connection.commit()


def change_post(id, title_n, description_n):
    cursor.execute(
        """
    UPDATE posts
    SET title = (%s), description = (%s)
    WHERE id = (%s)
    """,
        (title_n, description_n, id),
    )
    connection.commit()


# cursor.close()
# connection.close()
