import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from CTkMessagebox import CTkMessagebox

ctk.set_appearance_mode("dark")
class Admin_Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ChatEase")
        self.geometry("1200x650")
        
        self.minsize(1200, 650)
        self.maxsize(1200, 650)
        

        # Chat session storage
        self.active_chat = None
        self.bg_greeting = None

     

        self.load_images()
        self.main_frame()
        self.buttons()
        self.controller = None
        self.popup_frame = None  # placeholder
        

    
    def set_controller(self, controller):
        self.controller = controller
    # ------------------------------------------------------
    # MAIN FRAME
    # ------------------------------------------------------
    def load_images(self):
        try:
            self.bg = ctk.CTkImage(light_image=Image.open("admin_background.png"), size=(300, 400))
        except Exception as e:
            print("Error loading images:", e)


    def main_frame(self):
        main_frame = ctk.CTkFrame(self, width=1200, height=700, fg_color="#0D1B2A")
        main_frame.pack()

        # Main chat frame
        self.mainframe = ctk.CTkFrame(self, width=820, height=620, fg_color="#13283d", corner_radius=2)
        self.mainframe.place(x=360, y=10)

        try:
            # Background image
            bg_img = Image.open("admin_background.png")
            self.bg = ctk.CTkImage(light_image=bg_img, size=(750, 500))
            self.bg_label = ctk.CTkLabel(self.mainframe, image=self.bg, text="")
            self.bg_label.place(x=230, y=50)

        except (FileNotFoundError, Exception) as e:
            print(f"Image loading failed: {e}. Skipping.")
        # Text under image
        words_font = ctk.CTkFont(family="Arial", size=15, slant="italic")
        words = ctk.CTkLabel(self.mainframe, width=150, height=50,
                            text="Select New Chat to Initiate Conversation",
                            font=words_font, text_color="#00BFA5")
        words.place(x=490, y=540)




        #Total Response
        response_frame = ctk.CTkFrame(self.mainframe, width=250, height=170, fg_color= "#0D1B2A" )
        response_frame.place(x = 70, y =360)

        #Words Inside Response
        response_font = ctk.CTkFont(family="Arial", size= 25, weight="bold")
        response_words = ctk.CTkLabel(response_frame, text="Total Response",text_color="#00BFA5", font=response_font)
        response_words.place(x= 20, y= 20)

        over_font = ctk.CTkFont(family="Arial", size= 10, weight="bold")
        over_words = ctk.CTkLabel(response_frame, text="Over",text_color="white", font=over_font)
        over_words.place(x= 20, y= 60)

        number_font = ctk.CTkFont(family="Arial", size= 40, weight="bold", slant="italic")
        number_words = ctk.CTkLabel(response_frame, text="1000+",text_color="#00BFA5", font=number_font)
        number_words.place(x= 20, y= 90)

        # Typing Text
        self.bubble_frame = ctk.CTkFrame(self.mainframe, width=400, height=100, fg_color="transparent")
        self.bubble_frame.place(x=20, y=160)

        self.another_bubble_frame = ctk.CTkFrame(self.mainframe, width=400, height=100, fg_color="transparent")
        self.another_bubble_frame.place(x=25, y=240)

        # Labels inside bubbles
        typing_font = ctk.CTkFont(family="Space Age", size=45, weight="bold")
        self.typing_label = ctk.CTkLabel(self.bubble_frame, text="", font=typing_font,
                                        wraplength=350, justify="center", text_color="#00BFA5")
        self.typing_label.pack(padx=15, pady=15)

        another_typing_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold", slant="italic")
        self.another_label = ctk.CTkLabel(self.another_bubble_frame, text="", font=another_typing_font,
                                        wraplength=350, justify="center", text_color="#00BFA5")
        self.another_label.pack(padx=(20, 0), pady=15)

        # Typing messages
        self.message = "ChatEase"
        self.another_message = "Your Personal Helpdesk Companion"
        self.current_index = 0
        self.another_index = 0

        # Movement settings
        self.bubble_y = 190
        self.another_bubble_y = 290

        self.bubble_target_y = 160      # where first bubble should stop moving
        self.another_target_y = 240     # where second bubble should stop moving


        self.type_text()

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=320, height=630, fg_color="#13283d", corner_radius=10)
        self.sidebar_frame.place(x=10, y=10)

        self.side_scrollbar = ctk.CTkScrollableFrame(self.sidebar_frame, width=320, height=780, fg_color="transparent")
        self.side_scrollbar.place(x=0, y=200)

        self.recent_chats = ctk.CTkLabel(self.sidebar_frame, text="Welcome, Admin!",
                                        font=("Arial", 20, "bold"), text_color="white")
        self.recent_chats.place(x=35, y=40)

    def type_text(self):
        updated = False

        # --- First bubble typing + upward movement ---
        if self.current_index < len(self.message):
            # Typing
            self.typing_label.configure(
                text=self.typing_label.cget("text") + self.message[self.current_index]
            )
            self.current_index += 1
            updated = True

            # Move upward while typing
            if self.bubble_y > self.bubble_target_y:
                self.bubble_y -= 2
                self.bubble_frame.place(x=10, y=self.bubble_y)

        # --- Second bubble typing + upward movement ---
        elif self.another_index < len(self.another_message):
            # Typing
            self.another_label.configure(
                text=self.another_label.cget("text") + self.another_message[self.another_index]
            )
            self.another_index += 1
            updated = True

            # Move upward while typing
            if self.another_bubble_y > self.another_target_y:
                self.another_bubble_y -= 2
                self.another_bubble_frame.place(x=15, y=self.another_bubble_y)

        # --- Reset when both finished ---
        else:
            self.after(1000, self.reset_typing)
            return

        # Continue sequence
        if updated:
            self.after(80, self.type_text)

    
    def reset_typing(self):
        self.typing_label.configure(text="")
        self.another_label.configure(text="")

        self.current_index = 0
        self.another_index = 0

        self.after(300, self.type_text)  # restart typing


    def buttons(self):
        add_answer_font = ctk.CTkFont(family="Arial", size=17)
        self.add_answer_button = ctk.CTkButton(
            self.sidebar_frame, width=200, height=40, 
            text="Add Answer", fg_color="transparent",
            hover_color="#182f4d", text_color="white",
            cursor="hand2", font=add_answer_font,
            anchor="w",
            command=self.add_answer
        )
        self.add_answer_button.place(x=20, y=80)


        update_answer_font = ctk.CTkFont(family="Arial", size=17)
        self.update_answer_button = ctk.CTkButton(
            self.sidebar_frame, width=200, height=40,
            text="Update Answer", fg_color="transparent",
            hover_color="#182f4d", cursor="hand2", anchor="w",
            corner_radius=10,
            font=update_answer_font,
            command=self.update_answer_window
            )
        self.update_answer_button.place(x=15, y=120)



        delete_answer_font = ctk.CTkFont(family="Arial", size=17)
        self.delete_answer_button = ctk.CTkButton(
            self.sidebar_frame, width=200, height=40,
            text="Delete Answer", fg_color="transparent",
            hover_color="#182f4d", cursor="hand2", anchor="w",
            corner_radius=10,
            font=delete_answer_font,
            command=self.delete_answer_window
            )
        self.delete_answer_button.place(x=15, y=160)

        # Logout button 
        logout_font = ctk.CTkFont(family="Arial", size=17)
        self.logout_button = ctk.CTkButton(
            self.sidebar_frame, width=200, height=40,
            text="Logout", fg_color="transparent",
            hover_color="#182f4d", cursor="hand2", anchor="w",
            corner_radius=10,
            font=logout_font
        )
        self.logout_button.place(x=15, y=200)


        about_us_font = ctk.CTkFont(family="Arial", size=15, weight="bold")
        self.about_us = ctk.CTkButton(self.mainframe, width=100, height=50, text="About Us", command=self.open_popup, fg_color="transparent", font=about_us_font, hover_color="#00BFA5")
        self.about_us.place(x = 600, y = 30)

        admin_notification_font = ctk.CTkFont(family="Arial", size=15, weight="bold")
        self.about_us = ctk.CTkButton(self.mainframe, width=100, height=50, text="Notification",command=self.notification_popup, fg_color="transparent", font=admin_notification_font, hover_color="#00BFA5")
        self.about_us.place(x = 500, y = 30)
     #ABOUT US
    def open_popup(self):
        # Prevent multiple popups
        if self.popup_frame is not None:
            return  

        # Create frame
        self.popup_frame = ctk.CTkFrame(self, width=320, height=350, fg_color="#0D1B2A")
        self.popup_frame.place(x= 850, y = 90)

        # Title
        ctk.CTkLabel(
            self.popup_frame,
            text="ChatEase",
            font=("Arial", 30, "bold"),
            text_color="#00BFA5"

        ).place(x=90, y= 20)

        # Message
        ctk.CTkLabel(
            self.popup_frame,
            text="ChatEase is a modern AI chatbot system\n"
                 "built using Python & CustomTkinter.\n " 
                 "It's a simple computer-based application\n" 
                 "designed to help people when they are seeking\n" 
                 "assistance or information.Instead of using systems\n" 
                 "that require data or the internet to access\n" 
                 "information, this system allows users to access\n" 
                 " information anytime and anywhere even without\n" 
                 " an internet connection, because all data is stored\n" 
                 " locally in our Database",
                 
            justify="center", font=("Arial", 13)
        ).place(x= 10, y= 70)

        # Close button
        ctk.CTkButton(
            self.popup_frame,
            text="Close",
            command=self.close_popup,
            hover_color="#00BFA5"
        ).place(x= 90, y= 300)

    def close_popup(self):
        if self.popup_frame:
            self.popup_frame.destroy()
            self.popup_frame = None




    
    def notification_popup(self):
        # Prevent multiple popups
        if getattr(self, "popup_frame", None) is not None:
            return  

        # Create frame
        self.popup_frame = ctk.CTkFrame(self, width=320, height=350, fg_color="#0D1B2A")
        self.popup_frame.place(x=850, y=90)

        self.popup_scrollable = ctk.CTkScrollableFrame(self.popup_frame, width=320, height=350, fg_color="#0D1B2A")
        self.popup_scrollable.place(x=0, y=0)

        # Title
        ctk.CTkLabel(
            self.popup_scrollable,
            text="Tickets",
            font=("Arial", 30, "bold"),
            text_color="#00BFA5"
        ).pack(pady=10)

        # ---------------------------
        # LOAD TICKETS FROM DATABASE
        # ---------------------------
        tickets = self.load_tickets()  # returns [(user, msg, date), ...]

        if not tickets:
            ctk.CTkLabel(
                self.popup_scrollable,
                text="No tickets found.",
                font=("Arial", 14)
            ).pack(pady=10)
        else:
            # Display each ticket as a clickable button
            for user, msg, date in tickets:
                ticket_btn = ctk.CTkButton(
                    self.popup_scrollable,
                    text=f"{user}: {msg[:30]}...",  # show first 30 chars
                    width=280,
                    height=60,
                    fg_color="#1B1B1B",
                    hover_color="#00BFA5",
                    corner_radius=2,
                    anchor="w",
                    command=lambda u=user, m=msg, d=date: self.open_ticket_frame(u, m, d)
                )
                ticket_btn.pack(pady=5, padx=10)

        # Close button
        ctk.CTkButton(
            self.popup_frame,
            text="Close",
            command=self.close_popup,
            hover_color="#00BFA5"
        ).place(x=90, y=300)



    def close_popup(self):
        if self.popup_frame:
            self.popup_frame.destroy()
            self.popup_frame = None


    def open_ticket_frame(self, user, msg, date):
        # Destroy previous frame if exists
        if getattr(self, "ticket_detail_frame", None):
            self.ticket_detail_frame.destroy()

        # Create a new frame
        self.ticket_detail_frame = ctk.CTkFrame(self, width=330, height=240, fg_color="#0D1B2A", corner_radius=2)
        self.ticket_detail_frame.place(x=380, y=100)

        # Add ticket details
        ctk.CTkLabel(self.ticket_detail_frame, text=f"From: {user}", font=("Arial", 18, "bold")).place(x= 10, y= 10)
        ctk.CTkLabel(self.ticket_detail_frame, text=f"Message:\n{msg}", wraplength=250, justify = "left", font=("Arial", 13, "bold")).place(x = 10, y= 100)
        ctk.CTkLabel(self.ticket_detail_frame, text=f"Date: {date}", font=("Arial", 12, "italic")).place(x = 10, y= 30)

        # Close button inside the frame
        ctk.CTkButton(
            self.ticket_detail_frame,
            text="Close",
            command=self.ticket_detail_frame.destroy,
            hover_color="#00BFA5", 
            height= 30,
            corner_radius=10
        ).place(x= 90, y =190)

    def load_tickets(self):
        import sqlite3
        con = sqlite3.connect("tickets.db")
        cur = con.cursor()

        cur.execute("SELECT user_name, message, date FROM tickets ORDER BY id DESC")
        data = cur.fetchall()

        con.close()
        return data


    #Add Answer Window
    def add_answer(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Add Answer in Database")
        self.add_window.geometry("400x450")
        self.add_window.resizable(False, False)
        self.add_window.grab_set()

        self.add_answer_frame = ctk.CTkFrame(self.add_window, width=400, height=450, fg_color="#13283d")
        self.add_answer_frame.place(x=0, y=0)

        add_font = ctk.CTkFont(family="Arial", size=22, weight="bold")
        add_label = ctk.CTkLabel(self.add_window, text=" 📋 Add Answer", font=add_font, text_color="#00BFA5",fg_color="#13283d")
        add_label.place(x=40, y=20)

        self.question_entry = ctk.CTkEntry(self.add_window, placeholder_text="What's the Question?", width=300, height=50, fg_color="#13283d")
        self.question_entry.place(x=50, y=70)

        self.desc_box = ctk.CTkTextbox(self.add_window, width=300, height=200, border_color="gray", border_width=1, fg_color="#13283d")
        self.desc_box.insert("0.0", "Enter the Answer here...")
        self.desc_box.place(x=50, y=150)

        submit_btn = ctk.CTkButton(self.add_window, text="Save to Database", command=self.add_answer_submit, width=150, hover_color="#00BFA5", fg_color="#0D1B2A")
        submit_btn.place(x=125, y=370)


    def add_answer_submit(self):
        question = self.question_entry.get().strip()
        answer = self.desc_box.get("0.0", "end").strip()

        if not question or not answer or answer == "Enter the Answer here...":
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
            CTkMessagebox(title="Saved!", message="Answer stored successfully.", icon="check")
            self.add_window.destroy()


    
    #UPDATE ANSQWER WINDOW
    def update_answer_window(self):
        self.update_window = ctk.CTkToplevel(self)
        self.update_window.title("Update Database")
        self.update_window.geometry("400x450")
        self.update_window.resizable(False, False)
        self.update_window.grab_set()

        self.update_answer_frame = ctk.CTkFrame(self.update_window, width=400, height=450, fg_color="#13283d")
        self.update_answer_frame.place(x=0, y=0)

        update_font = ctk.CTkFont(family="Arial", size=22, weight="bold")
        update_label = ctk.CTkLabel(self.update_window, text=" 📝 Update Answer", font=update_font, text_color="#00BFA5", fg_color="#13283d")
        update_label.place(x=30, y=20)

        self.update_question_entry = ctk.CTkEntry(self.update_window, placeholder_text="Question to update...", width=300, height=50, fg_color="#13283d")
        self.update_question_entry.place(x=50, y=70)

        self.update_desc_box = ctk.CTkTextbox(self.update_window, width=300, height=200, border_color="gray", border_width=1, fg_color="#13283d")
        self.update_desc_box.insert("0.0", "Updated answer here...")
        self.update_desc_box.place(x=50, y=150)

        update_submit_btn = ctk.CTkButton(self.update_window, text="Update", command=self.update_answer_submit, width=150, hover_color="#00BFA5", fg_color="#0D1B2A")
        update_submit_btn.place(x=125, y=370)


    def update_answer_submit(self):
        question = self.update_question_entry.get().strip()
        updated_answer = self.update_desc_box.get("0.0", "end").strip()

        if not question or not updated_answer or updated_answer == "Updated answer here...":
            CTkMessagebox(title="Error", message="Please fill in all fields.", icon="cancel")
            return

        confirm = CTkMessagebox(
            title="Confirm Update",
            message=f"Are you sure you want to update:\n\n\"{question}\"?",
            icon="warning",
            option_1="Cancel",
            option_2="Update"
        )

        if confirm.get() == "Update":
            CTkMessagebox(
                title="Updated!",
                message="The question has been successfully updated.",
                icon="check"
            )
            self.update_window.destroy()





    def delete_answer_window(self):
        # Create a popup window
        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.title("Delete Answer")
        self.delete_window.geometry("400x450")
        self.delete_window.resizable(False, False)
        self.delete_window.grab_set()  # Focus on popup

        self.delete_answer_frame = ctk.CTkFrame(self.delete_window, width=400, height=450, fg_color="#13283d")
        self.delete_answer_frame.place(x=0, y=0)

        # Title
        delete_font = ctk.CTkFont(family="Arial", size=22, weight="bold")
        delete_label = ctk.CTkLabel(self.delete_window, text="📤 Remove From Database", font=delete_font,
                                    fg_color="#13283d", text_color="#00BFA5")
        delete_label.place(x=30, y=20)

        # Entry Field
        self.delete_answer_entry = ctk.CTkEntry(self.delete_window, placeholder_text="Enter question to delete...",
                                                width=300, height=50, fg_color="#13283d")
        self.delete_answer_entry.place(x=50, y=70)

        # Submit Button
        delete_submit_btn = ctk.CTkButton(self.delete_window, text="Delete", command=self.delete_answer_submit,
                                        width=100, height=50, hover_color="#00BFA5", fg_color="#0D1B2A")
        delete_submit_btn.place(x=140, y=370)


    def delete_answer_submit(self):
        delete_text = self.delete_answer_entry.get()

        if not delete_text:
            CTkMessagebox(title="Error", message="Please enter a question.", icon="cancel")
            return

        # ⚠️ Confirmation popup
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message=f"Are you sure you want to delete:\n\n\"{delete_text}\"?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )

        result = confirm.get()

        if result == "Delete":
            # Proceed with deleting
            CTkMessagebox(
                title="Deleted",
                message="Question was successfully deleted.",
                icon="check"
            )
            
            self.delete_window.destroy()

        else:
            # Cancel pressed - do nothing
            CTkMessagebox(title="Cancelled", message="Deletion cancelled.", icon="info")


    
    


app = Admin_Dashboard()
app.mainloop()