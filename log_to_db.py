from webapp.db import DB

def log_to_db(msg):
    """Log to database."""

    db = DB()

    sql = "INSERT INTO log (entry) VALUES (%s)"
    db.execute(sql, msg)
    db.commit()

    db.cursor.close()
    db.disconnect()
