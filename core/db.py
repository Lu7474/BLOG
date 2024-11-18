import psycopg2
import os
from datetime import datetime
from werkzeug.utils import secure_filename


def get_db_connection():
    return psycopg2.connect(
        dbname="BLOG",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
    )


date_pub = datetime.now()


UPLOAD_FOLDER = "core/static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return file_path
    return None


def get_posts(search=None):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            if search:
                cursor.execute(
                    f"""
                    SELECT posts.id, title, description, username, date_pub, image_path FROM posts INNER JOIN users ON posts.author_id=users.id WHERE title LIKE '%{search}%';
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT posts.id, title, description, username, date_pub, image_path FROM posts INNER JOIN users ON posts.author_id=users.id;
                    """
                )
            posts = cursor.fetchall()
            return posts


def save_post(title, description, image_file=None):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            image_path = None
            if image_file:
                image_path = save_image(image_file)
            cursor.execute(
                """
                INSERT INTO posts (title, description, author_id, date_pub, image_path)
                VALUES (%s, %s, 1, %s, %s);
                """,
                (title, description, date_pub, image_path),
            )
            connection.commit()


def get_post(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM posts WHERE id = %s;
                """,
                (id,),
            )
            post = cursor.fetchone()
            return post


def del_post(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM posts WHERE id= (%s);
                """,
                (id,),
            )
            connection.commit()


def change_post(id, title_n, description_n):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
            UPDATE posts
            SET title = (%s), description = (%s)
            WHERE id = (%s)
            """,
                (title_n, description_n, id),
            )
            connection.commit()
