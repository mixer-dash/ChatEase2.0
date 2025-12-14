import database as db
from CTkMessagebox import CTkMessagebox
import uuid  # For generating unique chat_ids

class Controller:
    def __init__(self, view, database=None):
        self.view = view
        self.db = database if database is not None else db
        self.current_user = None
        self.user_id = None
        self.user_role = None
        self.chats = []  # Initialize chats
        self.active_chat = None
        

    # Tickets API
    def controller_submit_ticket(self, name: str, issue: str, description: str):
        try:
            return db.Submitting_ticket.ticket(name, issue, description)
        except Exception as e:
            print("Ticket submission failed:", e)
            return None



    def controller_ticket_getter(self):
        try:
            return db.firstname_getter()
        except Exception as e:
            print("Firstname retrieval failed:", e)
            return None


    def load_tickets(self):
        try:
            return db.load_tickets()
        except Exception as e:
            print("Loading tickets failed:", e)
            return []



    def submit_action(self):
        username = self.view.username.get().strip()
        password = self.view.password.get().strip()
        

        if not username or not password:
            CTkMessagebox(title="Error", message="Please fill out all fields!", icon="cancel")
            return False
        
        login_success, role = db.login_user(username, password)

        if login_success:
            CTkMessagebox(title="Success", message="Login Successful!", icon="check")

            self.current_user = username
            self.user_role = role

            if role == "user":
                self.load_all_chats(username)

            return True
        else:
            return self.view.display_message("Incorrect username/password", "red")


    def get_firstname(self):
        firstname = self.view.username.get().strip()
        return db.firstname_getter(firstname) 

    def controller_ticket_remove(self, name):
        try:
            return db.remove_ticket(name)
        except Exception as e:
            print("Ticket removal failed:", e)
            return None




    def register_user(self):
        username = self.view.createUsername.get().strip()
        password = self.view.createPassword.get().strip()
        firstName = self.view.firstName.get().strip()
        lastName = self.view.lastName.get().strip()

        if not username or not password or not firstName or not lastName:
            self.view.display_message("Please fill out all fields!", "red")
            return

        if db.register_user(username, password, firstName, lastName):
            CTkMessagebox(title="Success", message="Account created successfully!", icon="check")
        else:
           CTkMessagebox(title="Failed", message="Username already exist!", icon="warning")

    


    def change_password(self, username, new_password):
        if not username or not new_password:
            return False
        else:
            return db.change_password(username, new_password) 
    

    def message(self, username, msg):
        if self.active_chat is None:
            # Handle the case where there's no active chat (e.g., start a new one)
            print("No active chat. Starting a new one...")
            chat_id = self.start_new_chat(username) # This will create a new chat and update self.chats
        else:
            chat_id = self.chats[self.active_chat]["chat_id"]

        self.save_user_message(username, msg, chat_id) # Pass chat_id

        bot_reply = db.get_answer(msg)

        self.save_bot_message(username, bot_reply, chat_id) # Pass chat_id

        return bot_reply
    



    def save_user_message(self, username, message, chat_id):
        return db.save_chat_message(username, message, "user", chat_id)

    def save_bot_message(self, username, message, chat_id):
        return db.save_chat_message(username, message,"bot", chat_id)

#Ito ay para sa get_chat_history
    def load_chat_history(self, username, chat_id):
        """Load chat history from DB and populate self.chats for the active chat."""
        if self.active_chat is None:
            return
        
        history = db.get_chat_history(username, chat_id)
        # Map DB rows to (sender, text) format for UI: (role, message)
        self.chats[self.active_chat]["messages"] = [(row[1], row[0]) for row in history]

    # New: Load all chats for a user on login 
    def load_all_chats(self, username):
        chat_ids = self.db.get_user_chat_ids(username)
        self.chats = []  # Reset
        for chat_id in chat_ids:
            history = self.db.get_chat_history(username, chat_id)
            messages = [(row[1], row[0]) for row in history]
            # Infer title from first user message, or default
            title = ""
            for role, msg in messages:
                if role == "user":
                    title = msg[:50]
                    break
            if not title:
                title = f"Chat {len(self.chats) + 1}"
            self.chats.append({"title": title, "messages": messages, "chat_id": chat_id})
        # Set active_chat to the first one if any exist
        self.active_chat = 0 if self.chats else None
        if self.view is not None and hasattr(self.view, 'update_recent_chats'):
            self.view.update_recent_chats()

        else:
            print("View is not set or does not have update_recent_chats method")


    def start_new_chat(self, username):
        """Starts a new chat and assigns a new chat_id."""
        chat_id = str(uuid.uuid4())  # Generate a unique chat_id
        
        self.chats.append({"title": "New Chat", "messages": [], "chat_id": chat_id})
        self.active_chat = len(self.chats) - 1
        if self.view is not None and hasattr(self.view, 'update_recent_chats'):
            self.view.update_recent_chats()
        else:
            print("View is not set or does not have update_recent_chats method.")

        return chat_id
    
    
    def add_answer_submit(self, view):
        question = view.question_entry.get().strip()
        answer = view.desc_box.get("0.0", "end").strip()
        keywords = view.keywords.get().strip()

        if answer == "Enter the Answer here...":
            answer = ""

        if not question or not answer or not keywords:
            CTkMessagebox(title="Error", message="Please fill all fields.", icon="cancel")
            return
        
        confirm = CTkMessagebox(
            title="Confirm Save",
            message=f"Save this question to database?\n\n\"{question}\"",
            icon="question",
            option_1="Cancel",
            option_2="Save"
        )
        if confirm.get() == "Save":
            try:
                # Save to the database using the model
                db.add_answer(question, answer, keywords)
                CTkMessagebox(title="Saved!", message="Answer stored successfully.", icon="check")
                view.add_window.destroy()
            except Exception as e:
                # Handle database errors gracefully
                CTkMessagebox(title="Error", message=f"Failed to save answer: {str(e)}", icon="cancel")


    def update_answer_submit(self, view):
        question = view.update_question_entry.get().strip()
        new_answer = view.update_desc_box.get("0.0", "end").strip()

        if new_answer == "Enter the Answer here...":
            new_answer = ""

        if not question or not new_answer:
            CTkMessagebox(title="Error", message="Please fill all fields.", icon="cancel")
            return

        confirm = CTkMessagebox(
            title="Confirm Update",
            message=f"Update this question in database?\n\n\"{question}\"",
            icon="question",
            option_1="Cancel",
            option_2="Update"
        )
        if confirm.get() == "Update":
            try:
                db.update_answer(question, new_answer)
                CTkMessagebox(title="Updated!", message="Answer updated successfully.", icon="check")
                view.update_window.destroy()
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Failed to update answer: {str(e)}", icon="cancel")

    def delete_answer_submit(self, view, questions):
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message="Are you sure you want to delete this answer?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )
        if confirm.get() == "Delete":
            try:
                db.delete_answer(questions)
                CTkMessagebox(title="Deleted!", message="Answer deleted successfully.", icon="check")
                view.delete_window.destroy()
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Failed to delete answer: {str(e)}", icon="cancel")
