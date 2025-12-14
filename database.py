# Database.py
from sentence_transformers import SentenceTransformer, util
import string, sqlite3, hashlib, random
from contextlib import closing

FAQ_TABLE = "faq"

DB_PATH = "helpdesk.db"


class Submitting_ticket:
    def ticket(name, issue, pending_questions):
        conn = connect_db()
        cur = conn.cursor()
        # Ensure table exists
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                issue TEXT NOT NULL,
                pending_questions TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            "INSERT INTO ticket (name, issue, pending_questions) VALUES (?, ?, ?)",
            (name, issue, pending_questions,)
        )
        conn.commit()
        return cur.lastrowid

# Load model (It is outside the function for speed)
model = SentenceTransformer('all-MiniLM-L6-v2')


def init_db():
    with closing(connect_db()) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                role TEXT NOT NULL,
                chat_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        # Ensure ticket table exists
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                issue TEXT NOT NULL,
                pending_questions TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


def add_answer(questions, answers, keywords):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {FAQ_TABLE} (questions, answers, keywords) VALUES (?, ?, ?)",
            (questions, answers, keywords)
        )
        conn.commit()

def update_answer(question, new_answer):
    try:
        with closing(connect_db()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {FAQ_TABLE} SET answers = ? WHERE questions = ?",
                (new_answer, question)
            )
            conn.commit()
    except Exception as e:
        print("Database update error:", e)
        raise


        

def firstname_getter():
    try:
        with closing(connect_db()) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT name, issue, pending_questions FROM ticket """)
            #conn.commit()
            return cur.fetchall()
    except Exception as e:
        print("Error saving message:", e)
        return []
    
def remove_ticket(name):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM ticket WHERE name = ?", (name,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print("Error deleting ticket:", e)
        return False


def save_chat_message(username: str, message: str, role: str, chat_id: str):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_history (username, message, role, chat_id)
            VALUES (?, ?, ?, ?)
        """, (username, message, role, chat_id))
        conn.commit()
    except Exception as e:
        print("Error saving message:", e)


def load_tickets():
    try:
        with closing(connect_db()) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT name, pending_questions, created_at FROM ticket ORDER BY id DESC"
            )
            data = cur.fetchall()
            return data
    except Exception as e:
        print("Cannot find data:", e)
        return []

def get_chat_history(username: str, chat_id: str):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT message, role, timestamp
            FROM chat_history
            WHERE username = ? AND chat_id = ?
            ORDER BY id ASC
        """, (username, chat_id))
        return cur.fetchall()  # Returns list of (message, role, timestamp)
    except Exception as e:
        print("Error loading history:", e)
        return []
    
    
def get_user_chat_ids(username: str):
    try:
        with closing(connect_db()) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT chat_id
                FROM chat_history
                WHERE username = ?
                ORDER BY (id) ASC  -- Order by oldest message in each chat
            """, (username,))
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error loading chat IDs:", e)
        return []







def format_response(answer):
    """
    Converts raw database answers into a modern conversational reply.
    """
    openers = [
        "Here’s what I found:",
        "Here’s the explanation:",
        "Let me break this down for you:",
        "Sure, here’s the answer:",
        "Got it. Here's the information:",
    ]

    closers = [
        "If you want to explore something else, feel free to ask.",
        "Let me know if you'd like more details.",
        "You can ask me anything else you’re curious about.",
        "If you need help with something else, I’m here.",
    ]

    
    return f"{random.choice(openers)}\n\n{answer}\n\n{random.choice(closers)}"


def get_answer(user_question):

    # Normalize input
    user_question = user_question.lower().translate(
        str.maketrans("", "", string.punctuation)
    )

    # Connect to DB
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT questions, answers, keywords FROM faq")
    rows = cursor.fetchall()

    if not rows:
        return "I cannot confirm this because the FAQ table is empty."

    # Prepare DB text + answer list
    db_texts = []
    answers = []

    for q, a, k in rows:
        if k:
            combined = f"{q} {k}".lower().translate(
                str.maketrans("", "", string.punctuation)
            )
        else:
            combined = q.lower()

        db_texts.append(combined)
        answers.append(a)

    # Encode using the embedding model
    user_embedding = model.encode(user_question, convert_to_tensor=True)
    db_embeddings = model.encode(db_texts, convert_to_tensor=True)

    # Compute similarity scores
    similarities = util.pytorch_cos_sim(user_embedding, db_embeddings)[0]

    best_index = similarities.argmax()
    best_similarity = similarities[best_index].item()

    # Adjust threshold for best accuracy
    if best_similarity > 0.5:
        best_answer = answers[best_index]
        return format_response(best_answer)
    else:
        return "I cannot confirm this because no matching answer was found."
    





def insert_questions():
    data = [

    ]
    

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO faq (questions, answers, keywords)
    VALUES (?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

    print("FAQ data inserted successfully.")


#Login Database
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def connect_db():
    return sqlite3.connect(DB_PATH)

sqlite3.connect(DB_PATH)








def register_user(username: str, password: str, firstName: str, lastName: str) -> bool:
    username = (username or "").strip()
    password = (password or "").strip()
    firstName = (firstName or "").strip()
    lastName = (lastName or "").strip()

    if not username or not password or not firstName or not lastName:
        return False

    hashed_password = hash_password(password)

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", (firstName, lastName, username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False



def login_user(username: str, password: str) -> tuple[bool, str | None, str | None]:
    username = (username or "").strip()
    password = (password or "").strip()

    if not username or not password:
        return False, None

    hashed_password = hash_password(password)

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cur.fetchone()

        if user:
            role = "admin" if username.lower() == "admin" else "user"
            return True, role
        return False, None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, None
    


def change_password(username, new_password):
    hashed_new = hash_password(new_password)

    try:
        with closing(connect_db()) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hashed_new, username)
            )
            conn.commit()

            if cur.rowcount > 0:
                return True
            else:
                return False
    except Exception as e:
        print("Error updating password:", e)
        return False


# Delete answer by question
def delete_answer(question: str) -> bool:
    question = (question or "").strip()
    if not question:
        return False
    try:
        with closing(connect_db()) as conn:
            cur = conn.cursor()
            cur.execute(
                f"DELETE FROM {FAQ_TABLE} WHERE questions = ?",
                (question,)
            )
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print("Database delete error:", e)
        return False








    
