import hashlib
from db_connection import get_connection


def hash_password(password):
    """Password ko SHA-256 hash mein convert karta hai."""
    return hashlib.sha256(password.encode()).hexdigest()


def username_exists(username):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


def signup_user(username, password):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_pw)
        )
        conn.commit()
        return True, "✅ Account successfully created! Ab login kar sakte ho."
    except Exception as e:
        return False, f"❌ Signup failed: {e}"
    finally:
        cursor.close()
        conn.close()


def login_user(username, password):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return False, "❌ Username does not exist."

    hashed_pw = hash_password(password)
    if user["password_hash"] != hashed_pw:
        return False, "❌ Incorrect password."

    return True, "✅ Login successful!"


def update_user(old_username, new_username=None, new_password=None):
    """
    UPDATE operation.
    Username aur/ya password update karta hai.
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()

        if new_username:
            cursor.execute(
                "UPDATE users SET username = %s WHERE username = %s",
                (new_username, old_username)
            )

        if new_password:
            hashed_pw = hash_password(new_password)
            # agar username bhi update hua hai to naya username use karo
            target_username = new_username if new_username else old_username
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (hashed_pw, target_username)
            )

        conn.commit()
        return True, "✅ Account successfully updated!"
    except Exception as e:
        return False, f"❌ Update failed: {e}"
    finally:
        cursor.close()
        conn.close()


def delete_user(username):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        return True, "✅ Account successfully deleted."
    except Exception as e:
        return False, f"❌ Delete failed: {e}"
    finally:
        cursor.close()
        conn.close()
