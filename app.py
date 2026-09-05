from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import re


# =========================================
# APPLICATION
# =========================================

app = Flask(__name__)

CORS(app)


# =========================================
# DATABASE PATH
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "portfolio.db"
)


# =========================================
# DATABASE CONNECTION
# =========================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================
# INITIALIZE DATABASE
# =========================================

def init_db():

    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )


    connection = get_db()

    cursor = connection.cursor()


    # PROJECTS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT NOT NULL,

            link TEXT

        )
    """)


    # CONTACT MESSAGES TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            message TEXT NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)


    connection.commit()

    connection.close()


# =========================================
# HOME API
# =========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "status": "success",

        "message":
            "Anushka Portfolio API is running"

    })


# =========================================
# GET PROJECTS
# =========================================

@app.route(
    "/api/projects",
    methods=["GET"]
)
def get_projects():

    connection = get_db()


    projects = connection.execute(
        """
        SELECT
            id,
            title,
            description,
            link
        FROM projects
        ORDER BY id DESC
        """
    ).fetchall()


    connection.close()


    return jsonify([
        dict(project)
        for project in projects
    ])


# =========================================
# ADD PROJECT
# =========================================

@app.route(
    "/api/projects",
    methods=["POST"]
)
def add_project():

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({
            "error": "Invalid JSON data"
        }), 400


    title = str(
        data.get("title", "")
    ).strip()


    description = str(
        data.get("description", "")
    ).strip()


    link = str(
        data.get("link", "")
    ).strip()


    if not title:

        return jsonify({
            "error":
                "Project title is required"
        }), 400


    if not description:

        return jsonify({
            "error":
                "Project description is required"
        }), 400


    connection = get_db()


    cursor = connection.execute(
        """
        INSERT INTO projects
        (title, description, link)

        VALUES (?, ?, ?)
        """,

        (
            title,
            description,
            link
        )
    )


    connection.commit()


    project_id = cursor.lastrowid


    connection.close()


    return jsonify({

        "message":
            "Project created successfully",

        "id":
            project_id

    }), 201


# =========================================
# CONTACT FORM
# =========================================

@app.route(
    "/api/contact",
    methods=["POST"]
)
def contact():

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({
            "error": "Invalid request"
        }), 400


    name = str(
        data.get("name", "")
    ).strip()


    email = str(
        data.get("email", "")
    ).strip()


    message = str(
        data.get("message", "")
    ).strip()


    # BASIC VALIDATION

    if not name:

        return jsonify({
            "error":
                "Name is required"
        }), 400


    if not email:

        return jsonify({
            "error":
                "Email is required"
        }), 400


    if not message:

        return jsonify({
            "error":
                "Message is required"
        }), 400


    # EMAIL VALIDATION

    email_pattern = (
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )


    if not re.match(
        email_pattern,
        email
    ):

        return jsonify({
            "error":
                "Please enter a valid email"
        }), 400


    # SAVE MESSAGE

    connection = get_db()


    connection.execute(
        """
        INSERT INTO messages
        (name, email, message)

        VALUES (?, ?, ?)
        """,

        (
            name,
            email,
            message
        )
    )


    connection.commit()

    connection.close()


    return jsonify({

        "message":
            "Message received successfully"

    }), 201


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )