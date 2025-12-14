import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from CTkMessagebox import CTkMessagebox
from controller import Controller
import uuid, re, random, string
from email.mime.text import MIMEText
import smtplib


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Login_Signup(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = Controller(view=self) # Instantiate controller and pass self as view
        self.title("ChatEase")
        self.geometry('1100x700')
        self.minsize(1100, 680)
        self.maxsize(1100, 680)
        self.login_frame()

    def login_frame(self):
        main_frame = ctk.CTkFrame(self, width=1100, height=700, fg_color="#0D1B2A")
        main_frame.pack()
        try:
            self.bg_img = Image.open("seconds.png")
            self.bg = ctk.CTkImage(light_image=self.bg_img, size=(1110, 700))
            self.bg_label = ctk.CTkLabel(main_frame, image=self.bg, text="")
            self.bg_label.place(relx =0, rely=0)
        except FileNotFoundError:
            print("Background image not found. Skipping.")

        try:
            self.bg_img = Image.open("main.png")
            self.bg = ctk.CTkImage(light_image=self.bg_img, size=(550, 550))
            self.bg_label = ctk.CTkLabel(main_frame, image=self.bg, text="")
            self.bg_label.place(x=430, y= 100)
        except FileNotFoundError:
            print("Background image not found. Skipping.")


        #Login frame
        self.frame = ctk.CTkFrame(self, 
                                  width=400, 
                                  height=500, 
                                  corner_radius=1, 
                                  fg_color="#13283d")
        self.frame.place(x=120, y=100)

        self.bubble_frame = ctk.CTkFrame(self.frame, width=400, height=100, fg_color="transparent")
        self.bubble_frame.place(x=170, y=6)

        self.another_bubble_frame = ctk.CTkFrame(self.frame, width=400, height=100, fg_color="transparent")
        self.another_bubble_frame.place(x=170, y=70)

        # --- Labels inside bubbles ---
        typing_font = ctk.CTkFont(family="Segoe UI", size=45, weight="bold", slant="italic")
        self.typing_label = ctk.CTkLabel(
            self.bubble_frame,
            text="",
            font=typing_font,
            wraplength=350,
            justify="center",
            text_color="#00BFA5"
        )
        self.typing_label.pack(padx=15, pady=15)

        another_typing_font = ctk.CTkFont(family="Segoe UI", size=15, weight="bold", slant="italic")
        self.another_label = ctk.CTkLabel(
            self.another_bubble_frame,  # <-- place in another bubble
            text="",
            font=another_typing_font,
            wraplength=350,
            justify="center",
            text_color="#00BFA5"
        )
        self.another_label.pack(padx=15, pady=15)

        # --- Typing Text Setup ---
        self.message = "ChatEase"
        self.another_message = "Your Personal\nHelpdesk Companion"
        self.current_index = 0
        self.another_index = 0

        self.type_text()


        self.gif = Image.open("logo.gif")
        self.frames = [ImageTk.PhotoImage(frame.copy(), master=self) for frame in ImageSequence.Iterator(self.gif)]

        self.label = ctk.CTkLabel(self.frame, text="")
        self.label.place(x=10, y= 10)

        self.index = 0
        self.animate()
    
        self.text1 = "What is ChatEase?"
        self.out1 = ""
        self.idx1 = 0
        self.y1 = 200

        img = Image.open("chat_bubble.png")
        self.ctk_img1 = ctk.CTkImage(light_image=img, size=(250, 60))
        label1_font = ctk.CTkFont(family="Times New Romans", size= 15, slant="italic")
        self.label1 = ctk.CTkLabel(self, width=150, height=50, fg_color="#0D1B2A", text="", font=label1_font, corner_radius=4, text_color="#00BFA5", image=self.ctk_img1, compound="center")
        self.label1.place(x= 730, y=self.y1)

        self.animate_up_1()
        self.type_1()
        

        # ---------------------- LABEL 2 (HIDDEN FIRST) ----------------------
        self.text2 = "A simple computer-based\n application designed\n to help people "
        self.out2 = ""
        self.idx2 = 0
        self.y2 = 250

        img2 = Image.open("chat_bubble.png")
        self.ctk_img2 = ctk.CTkImage(light_image=img2, size=(220, 140))
        label2_font = ctk.CTkFont(family="Times New Romans", size= 13, slant="italic")
        self.label2 = ctk.CTkLabel(self, text="", font=label2_font, width= 170, height= 110, fg_color= "#0D1B2A", corner_radius=5, text_color="#00BFA5", image=self.ctk_img2, compound="center")
        # DON'T PLACE YET — wait until Label 1 finishes

        # ---------------------- LABEL 3 (HIDDEN FIRST) ----------------------
        self.text3 = "This App \ndoesn't need\n Internet."
        self.out3 = ""
        self.idx3 = 0
        self.y3 = 500
        
        img3 = Image.open("chat_bubble.png")
        self.ctk_img3 = ctk.CTkImage(light_image=img3, size=(220, 120))
        label3_font = ctk.CTkFont(family="Times New Romans", size= 13, slant="italic")
        self.label3 = ctk.CTkLabel(self, width= 150, height= 70, fg_color="#0D1B2A", text="", font=label3_font,text_color="#00BFA5", image=self.ctk_img3, compound="center")



        #SignUP
        self.sign_up_font_style = ctk.CTkFont(family="Times New Roman", size=15, slant="italic")
        self.sign_up_label = ctk.CTkLabel(self.frame, text="Doesn't have an Account?", text_color="white", font=self.sign_up_font_style)
        self.sign_up_label.place(x=58, y=180)

        sign_up_underline_font = ctk.CTkFont(underline=True)
        sign_up_btn = ctk.CTkButton(self.frame, 
                                    text="Sign Up",
                                    width=49, 
                                    height=40,
                                    border_width=0,
                                    fg_color="transparent",
                                    hover_color="#13283d", 
                                    font=sign_up_underline_font, 
                                    command=self.open_signup_window)
        sign_up_btn.place(x=230, y=175.4)

        # LOGIN USERNAME
        self.username = ctk.CTkEntry(self.frame,
                                      width=250, 
                                      height=35, 
                                      fg_color="transparent", 
                                      corner_radius=10, 
                                      text_color="white",
                                      placeholder_text="sample@gmail.com")
        self.username.place(x=80, y=250)

        # LOGIN PASSWORD
        self.password = ctk.CTkEntry(self.frame, 
                                     width=250, 
                                     height=35, 
                                     corner_radius=10, 
                                     fg_color="transparent", 
                                     text_color="white", 
                                     show="•")
        self.password.place(x=80, y=330)
        
        #LOGIN
        submitButton = ctk.CTkButton(self.frame,
                                      text="Log In", 
                                      width=200, 
                                      height=40, 
                                      corner_radius=20, 
                                      border_width=0,
                                     bg_color="transparent",
                                       fg_color="#0E66B3", 
                                       hover_color="#00BFA5",
                                     command=self.try_login)  # Fixed: Call instance method
        submitButton.place(x=100, y=400)

        underline_font = ctk.CTkFont(underline=True)
        
        #Forgot Password
        forgotPassword = ctk.CTkButton(self.frame, 
                                       text="Forgot Password?", 
                                       width=200,
                                        height=40,
                                        border_width=0,
                                       fg_color="transparent", 
                                       hover_color="#13283d", 
                                       font=underline_font,
                                       command=lambda: ForgotPasswordUI())
        forgotPassword.place(x=163, y=440)
        self.icons()

        #Show Password
        self.show_pass_checkbox = ctk.CTkCheckBox(self.frame, text="Show Password", command=self.toggle_password)
        self.show_pass_checkbox.place(x= 90, y= 370)
    




    def try_login(self):
        success = self.controller.submit_action()

        
        if success is True:
            self.open_dashboard()


    def open_dashboard(self):
        # Close the login/signup window
        self.withdraw()

        # Create the dashboard window
        if self.controller.user_role == 'admin':
            dashboard = Admin_Dashboard()
            dashboard.set_controller(self.controller)
            self.controller.view = dashboard
        else:
            dashboard = Dashboard(master=self)
            dashboard.set_controller(self.controller)
            self.controller.view = dashboard

            if self.controller.chats:
                dashboard.chats = self.controller.chats
                dashboard.active_chat = self.controller.active_chat
                dashboard.update_recent_chats()
                if dashboard.active_chat is not None:
                    dashboard.load_chat_messages()

        return dashboard

        
        



    def toggle_password(self):
        if self.show_pass_checkbox.get() == 1:       # Checked → show password
            self.password.configure(show="")
        else:                                   # Unchecked → hide password
            self.password.configure(show="•")

    def open_signup_window(self):
        SignUpUI()
    
    def icons(self):
        try:
            # EMAIL ICON
            self.email_icon = ctk.CTkImage(light_image=Image.open("email.png"), size=(20, 20))
            self.email_icon_label = ctk.CTkLabel(self.frame, image=self.email_icon, text="")
            self.email_icon_label.place(x=80, y=219)

            font_style = ctk.CTkFont(family="Arial", size=13, slant="italic")
            username_label = ctk.CTkLabel(self.frame, text="Username", text_color="White", font=font_style)
            username_label.place(x=105, y=220)

            # PASSWORD ICON
            password_icon_img = Image.open("lock.png")
            self.password_icon = ctk.CTkImage(light_image=password_icon_img, size=(23, 23))
            self.password_icon_label = ctk.CTkLabel(self.frame, image=self.password_icon, text="")
            self.password_icon_label.place(x=80, y=300)

            password_label = ctk.CTkLabel(self.frame, text="Password", text_color="white", font=font_style)
            password_label.place(x=105, y=300)
        except FileNotFoundError:
            print("Icon images not found. Skipping.")

    def display_message(self, message, color):
        # Simple method to display messages (e.g., in a label or popup)
        msg_label = ctk.CTkLabel(self.frame, text=message, text_color=color, font=("Arial", 12))
        msg_label.place(x=80, y=450)  # Adjust position as needed
        self.after(3000, msg_label.destroy)  # Auto-remove after 3 seconds

    def animate_up_1(self):
        self.y1 -= 2
        self.label1.place(y=self.y1)

        if self.y1 > 50:
            self.after(10, self.animate_up_1)
        else:
            self.start_label2()  # 👉 Start Label 2 when Label 1 reaches final position

    def type_1(self):
        if self.idx1 < len(self.text1):
            self.out1 += self.text1[self.idx1]
            self.label1.configure(text=self.out1)
            self.idx1 += 1
            self.after(60, self.type_1)

    # ---------------------- LABEL 2 ----------------------
    def start_label2(self):
        """Show Label 2 and start its animation"""
        self.label2.place(x= 850, y=self.y2)
        self.animate_up_2()
        self.type_2()

    def animate_up_2(self):
        self.y2 -= 2
        self.label2.place(y=self.y2)

        if self.y2 > 150:
            self.after(10, self.animate_up_2)
        else:
            self.start_label3()  # 👉 Start Label 3 when Label 2 reaches final position

    def type_2(self):
        if self.idx2 < len(self.text2):
            self.out2 += self.text2[self.idx2]
            self.label2.configure(text=self.out2)
            self.idx2 += 1
            self.after(60, self.type_2)

    # ---------------------- LABEL 3 ----------------------
    def start_label3(self):
        """Show Label 3 and start its animation"""
        self.label3.place(x= 880, y=self.y3)
        self.animate_up_3()
        self.type_3()

    def animate_up_3(self):
        self.y3 -= 2
        self.label3.place(y=self.y3)

        if self.y3 > 330:
            self.after(10, self.animate_up_3)

    def type_3(self):
        if self.idx3 < len(self.text3):
            self.out3 += self.text3[self.idx3]
            self.label3.configure(text=self.out3)
            self.idx3 += 1
            self.after(60, self.type_3)
    
    def animate(self):
        frame = self.frames[self.index]
        self.label.configure(image=frame)

        self.index = (self.index + 1) % len(self.frames)
        self.after(30, self.animate)  # Change speed here

    
    def type_text(self):
        updated = False

        if self.current_index < len(self.message):
            self.typing_label.configure(
                text=self.typing_label.cget("text") + self.message[self.current_index]
            )
            self.current_index += 1
            updated = True

        elif self.another_index < len(self.another_message):  # use elif so it types sequentially
            self.another_label.configure(
                text=self.another_label.cget("text") + self.another_message[self.another_index]
            )
            self.another_index += 1
            updated = True

        if updated:
            self.after(100, self.type_text)





from PIL import Image, ImageTk

class Dashboard(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("ChatEase")
        self.geometry("1200x650")
        
        self.minsize(1200, 650)
        self.maxsize(1200, 650)
        self._fg_color = "#0D1B2A"

        # Chat session storage
        self.chats = []
        self.active_chat = None
        self.bg_greeting = None
        self.bg_preview = None
        self.enter_icon = None
        self.chat_icon = None
        self.ticket_icon = None
        self.logout_icon = None
        self.user_icon = None
        self.ai_icon = None
        self.ai_icon_MAIN = None


        self.load_images()
        self.main_frame()
        self.buttons()
        self.controller = None

        

    
    def set_controller(self, controller):
        self.controller = controller
    # ------------------------------------------------------
    # MAIN FRAME
    # ------------------------------------------------------
    def load_images(self):
        try:
            self.bg = ctk.CTkImage(light_image=Image.open("greeting.png"), size=(300, 400))
            self.bg_preview = ctk.CTkImage(light_image=Image.open("chat_preview.png"), size=(400, 300))
            self.enter_icon = ctk.CTkImage(light_image=Image.open("Enter.png"), size=(20, 20))
            self.chat_icon = ctk.CTkImage(light_image=Image.open("new_chat.png"), size=(30, 30))
            self.ticket_icon = ctk.CTkImage(light_image=Image.open("ticket.png"), size=(30, 30))
            self.logout_icon = ctk.CTkImage(light_image=Image.open("logout.png"), size=(30, 30))
            self.user_icon = ctk.CTkImage(light_image=Image.open("users_icon.png"), size=(40, 40))
            self.ai_icon = ctk.CTkImage(light_image=Image.open("ai_icons.png"), size=(40, 40))
            self.ai_icon_MAIN = ctk.CTkImage(light_image=Image.open("ai_icon_MAIN.png"), size=(30, 30))
        except Exception as e:
            print("Error loading images:", e)


    def main_frame(self):
        main_frame = ctk.CTkFrame(self, width=1200, height=700, fg_color="#0D1B2A")
        main_frame.pack()

        # Main chat frame
        self.mainframe = ctk.CTkFrame(self, width=820, height=620, fg_color="#13283d", corner_radius=20)
        self.mainframe.place(x=360, y=10)

        try:
            # Background image
            bg_img = Image.open("greeting.png")
            self.bg = ctk.CTkImage(light_image=bg_img, size=(300, 400))
            self.bg_label = ctk.CTkLabel(self.mainframe, image=self.bg, text="")
            self.bg_label.place(x=20, y=50)

        except (FileNotFoundError, Exception) as e:
            print(f"Image loading failed: {e}. Skipping.")
        # Text under image
        words_font = ctk.CTkFont(family="Arial", size=15, slant="italic")
        words = ctk.CTkLabel(self.mainframe, width=150, height=50,
                            text="Select New Chat to Initiate Conversation",
                            font=words_font, text_color="#00BFA5")
        words.place(x=490, y=460)


        try: 
            bg_img = Image.open("chat_preview.png")
            self.bg_preview = ctk.CTkImage(light_image=bg_img, size=(400, 300))
            self.bg_label = ctk.CTkLabel(self.mainframe, image=self.bg_preview, text="")
            self.bg_label.place(x=400, y=170)
        except FileNotFoundError:
            print("Chat preview image not found. Skipping.")

        #Total Response
        response_frame = ctk.CTkFrame(self.mainframe, width=250, height=170, fg_color= "#0D1B2A" )
        response_frame.place(x = 90, y =435)

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
        self.bubble_frame.place(x=330, y=80)

        self.another_bubble_frame = ctk.CTkFrame(self.mainframe, width=400, height=100, fg_color="transparent")
        self.another_bubble_frame.place(x=330, y=150)

        # Labels inside bubbles
        typing_font = ctk.CTkFont(family="Segoe UI", size=45, weight="bold")
        self.typing_label = ctk.CTkLabel(self.bubble_frame, text="", font=typing_font,
                                        wraplength=350, justify="center", text_color="#00BFA5")
        self.typing_label.pack(padx=15, pady=15)

        another_typing_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold", slant="italic")
        self.another_label = ctk.CTkLabel(self.another_bubble_frame, text="", font=another_typing_font,
                                        wraplength=350, justify="center", text_color="#00BFA5")
        self.another_label.pack(padx=15, pady=15)

        # Typing messages
        self.message = "Hi, I'm ChatEase"
        self.another_message = "Your Personal Helpdesk Companion"
        self.current_index = 0
        self.another_index = 0

        self.type_text()

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=320, height=630, fg_color="#13283d", corner_radius=10)
        self.sidebar_frame.place(x=10, y=10)

        self.side_scrollbar = ctk.CTkScrollableFrame(self.sidebar_frame, width=320, height=780, fg_color="transparent", orientation="vertical")
        self.side_scrollbar.place(x=0, y=250)

        self.recent_chats = ctk.CTkLabel(self.sidebar_frame, text="Recent Chats",
                                        font=("Arial", 22, "bold"), text_color="white")
        self.recent_chats.place(x=35, y=50)

    def type_text(self):
        updated = False

        if self.current_index < len(self.message):
            self.typing_label.configure(
                text=self.typing_label.cget("text") + self.message[self.current_index]
            )
            self.current_index += 1
            updated = True

        elif self.another_index < len(self.another_message):  # use elif so it types sequentially
            self.another_label.configure(
                text=self.another_label.cget("text") + self.another_message[self.another_index]
            )
            self.another_index += 1
            updated = True

        if updated:
            self.after(100, self.type_text)
    # ------------------------------------------------------
    # ENTRY BOX
    # ------------------------------------------------------
    def entry_box(self):
    # Entry
        self.input_entry = ctk.CTkEntry(
            self.mainframe, width=450, height=50,
            corner_radius=100,
            text_color="white",
            fg_color="transparent",
            placeholder_text="Ask Anything?"
        )
        self.input_entry.place(x=200, y=550)

        try:
            # Enter Button MUST be recreated here
            logo_icon = Image.open("ai_icon_MAIN.png")
            self.logo_icon = ctk.CTkImage(light_image=logo_icon, size=(30, 30))  
            enter_icon_img = Image.open("Enter.png")         
            self.enter_icon = ctk.CTkImage(light_image=enter_icon_img, size=(20, 20))

            self.input_button = ctk.CTkButton(
                self.mainframe, width=40, height=40,
                text="", fg_color="transparent", hover_color="#009688",
                cursor="hand2", image=self.enter_icon, corner_radius=30,
                command=self.add_message
            )
            self.input_button.place(x=573, y=555)
        except FileNotFoundError:
            print("Enter icon not found. Skipping button image.")
            # Fallback: Create button without image
            self.input_button = ctk.CTkButton(
                self.mainframe, width=40, height=40,
                text=">", fg_color="transparent", hover_color="#009688",
                cursor="hand2", corner_radius=30,
                command=self.add_message
            )
            self.input_button.place(x=573, y=555)

    # ------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------
    def logout(self):
        # Close current dashboard window
        self.master.deiconify()
        self.destroy()
        # Reopen login/signup window
        login_window = Login_Signup()
        login_window.controller = self.controller
        self.controller.view = login_window

    def pending_ticket(self, name, issue, description):
        call = self.controller.controller_submit_ticket(name, issue, description)
        return call

    def buttons(self):
        self.new_chat_font = ctk.CTkFont(family="Arial", size=18)
        try:
            chat_icon_img = Image.open("new_chat.png")
            self.chat_icon = ctk.CTkImage(light_image=chat_icon_img, size=(40, 40))
            self.new_chat_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40, 
                text="New Chat", fg_color="transparent",
                hover_color="#182f4d", text_color="white",
                cursor="hand2", font=self.new_chat_font,
                image= self.chat_icon, anchor="w",
                command=self.new_chat
            )
            self.new_chat_button.place(x=20, y=100)

        except FileNotFoundError:
            print("New chat icon not found. Skipping button image.")
            # Fallback: Create button without image
            self.new_chat_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40, 
                text="New Chat", fg_color="transparent",
                hover_color="#182f4d", text_color="white",
                cursor="hand2", font=self.new_chat_font,
                anchor="w", command=self.new_chat
            )
            self.new_chat_button.place(x=20, y=100)

        try:
            # Ticket button
            ticket_icon_img = Image.open("ticket.png")
            self.ticket_icon = ctk.CTkImage(light_image=ticket_icon_img, size=(40, 40))
            ticket_font = ctk.CTkFont(family="Arial", size=18)
            self.ticket_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40,
                text="Ticket", fg_color="transparent",
                hover_color="#182f4d", cursor="hand2", anchor="w",
                image=self.ticket_icon, corner_radius=10,
                font=ticket_font,
                command=self.open_ticket_window
                )
            self.ticket_button.place(x=15, y=150)

        except FileNotFoundError:
            print("Ticket icon not found. Skipping button image.")
            # Fallback: Create button without image
            ticket_font = ctk.CTkFont(family="Arial", size=18)
            self.ticket_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40,
                text="Ticket", fg_color="transparent",
                hover_color="#182f4d", cursor="hand2", anchor="w",
                corner_radius=10, font=ticket_font, command=self.open_ticket_window
            )
            self.ticket_button.place(x=15, y=150)

        try:
            # Logout button
            logout_icon_img = Image.open("logout.png")
            self.logout_icon = ctk.CTkImage(light_image=logout_icon_img, size=(40, 40))
        
            logout_font = ctk.CTkFont(family="Arial", size=18)
            self.logout_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40,
                text="Logout", fg_color="transparent",
                hover_color="#182f4d", cursor="hand2", anchor="w",
                image=self.logout_icon, corner_radius=10,
                font=logout_font,
                command=self.logout,
            )
            self.logout_button.place(x=15, y=200)

        except FileNotFoundError:
            print("Logout icon not found. Skipping button image.")
            # Fallback: Create button without image
            logout_font = ctk.CTkFont(family="Arial", size=18)
            self.logout_button = ctk.CTkButton(
                self.sidebar_frame, width=200, height=40,
                text="Logout", fg_color="transparent",
                hover_color="#182f4d", cursor="hand2", anchor="w",
                corner_radius=10, font=logout_font,
                command=self.logout
            )
            self.logout_button.place(x=15, y=200)

    # ------------------------------------------------------
    # CHAT LOGIC
    # ------------------------------------------------------
    def new_chat(self): #The typing area

        self.main_scrollbar = ctk.CTkScrollableFrame(
                self.mainframe,
                width=820,
                height=680,
                fg_color="#13283d",
                orientation="vertical")
        self.main_scrollbar.place(x=0, y=0)

        if self.controller:
            self.controller.start_new_chat(self.controller.current_user)
            self.active_chat = self.controller.active_chat

        self.entry_box()
        # Clear input box
        self.input_entry.delete(0, "end")

        # Clear existing chat bubbles only
        for widget in self.main_scrollbar.winfo_children():
            widget.destroy()


    def add_message(self, event=None):
        msg = self.input_entry.get()
        if not msg or self.active_chat is None:
            return
        

        self.chats[self.active_chat]["messages"].append(("user", msg))
        ai_response = self.controller.message(self.controller.current_user, msg)
        self.chats[self.active_chat]["messages"].append(("bot", ai_response))

        if self.chats[self.active_chat]["title"] == "":
            self.chats[self.active_chat]["title"] = msg[:50]

        self.load_chat_messages()
        self.update_recent_chats()
        self.input_entry.delete(0, "end")


            
    def chat_click(self, index):
        self.active_chat = index
        if self.controller:
            chat_id = self.chats[index]["chat_id"]
            self.controller.active_chat = index
            self.controller.load_chat_history(self.controller.current_user, chat_id)
            self.chats[index]["messages"] = self.controller.chats[index]["messages"]
        self.load_chat_messages()


    def load_chat_messages(self):
        if not hasattr(self, "main_scrollbar"):
            self.main_scrollbar = ctk.CTkScrollableFrame(self.mainframe, width=820, height=680, fg_color="#13283d")
            self.main_scrollbar.place(x=0, y=0)
        for widget in self.main_scrollbar.winfo_children():
            widget.destroy()

        if self.active_chat is None:
            return

        # Load user and AI icons
        user_icon_img = Image.open("user_icon.png").resize((40, 40))
        user_icon = ctk.CTkImage(light_image=user_icon_img, size=(40, 40))

        ai_icon_img = Image.open("ai_icon_MAIN.png").resize((40, 40))
        ai_icon = ctk.CTkImage(light_image=ai_icon_img, size=(40, 40))

        for sender, msg in self.chats[self.active_chat]["messages"]:
            # Horizontal frame to hold icon + bubble
            frame = ctk.CTkFrame(self.main_scrollbar, fg_color="transparent")
            frame.pack(fill="x", pady=5, padx=50)

            bubble_font = ctk.CTkFont(family="Segoe UI", size=15)

            if sender == "user":
                # Right-aligned frame for user
                icon_label = ctk.CTkLabel(frame, image=user_icon, text="")
                icon_label.pack(side="right", padx=(10, 0))

                bubble = ctk.CTkLabel(
                    frame, text=msg, fg_color="#0D6EFD",
                    text_color="white", corner_radius=10,
                    anchor="center", justify="center", font=bubble_font,
                    wraplength=300, padx=15, pady=10
                )
                bubble.pack(side="right", padx=(0, 10))
            else:
                # Left-aligned frame for AI
                icon_label = ctk.CTkLabel(frame, image=self.ai_icon, text="")
                icon_label.pack(side="left", padx=(0, 10), pady=(10, 145))

                #frame ito
                bubble = ctk.CTkLabel(
                    frame, text=msg, fg_color="#1B263B",
                    text_color="white", corner_radius=10,
                    anchor="center", justify="center", font=bubble_font,
                    wraplength=300, padx=15, pady=10
                )
                bubble.pack(side="left", padx=(10, 0), pady=(10, 145))



    def update_recent_chats(self):
        self.label_font = ctk.CTkFont(family="Arial", size=15)
        for widget in self.side_scrollbar.winfo_children():
            widget.destroy()

        for i, chat in enumerate(self.chats):
            title = chat["title"] if chat["title"] else f"Chat {i+1}"
            label = ctk.CTkLabel(
                self.side_scrollbar, text=title, width=300, height=65,
                anchor="w", text_color="white", fg_color="#182f4d",
                cursor="hand2", font=self.label_font, corner_radius=10
            )
            label.pack(padx=5, pady=5)
            label.bind("<Button-1>", lambda e, idx=i: self.chat_click(idx))




    def open_ticket_window(self):
        # Create a popup window
        self.ticket_window = ctk.CTkToplevel(self)
        self.ticket_window.title("Submit a Ticket")
        self.ticket_window.geometry("400x450")
        self.ticket_window.resizable(False, False)
        self.ticket_window.grab_set()  # Focus on popup

        # Title
        title_font = ctk.CTkFont(family="Arial", size=22, weight="bold")
        title_label = ctk.CTkLabel(self.ticket_window, text="Submit a Ticket", font=title_font)
        title_label.pack(pady=15)

        # Name Field
        self.name_entry = ctk.CTkEntry(self.ticket_window, placeholder_text="Your Name", width=300)
        self.name_entry.pack(pady=10)


        # Issue Type
        self.issue_type = ctk.CTkOptionMenu(self.ticket_window, values=["Bug", "Account Issue", "Feature Request", "Other"])
        self.issue_type.pack(pady=10)

        # Description box
        self.desc_box = ctk.CTkTextbox(self.ticket_window, width=300, height=120)
        self.desc_box.insert("0.0", "Describe your issue here...")
        self.desc_box.pack(pady=10)

        submit_btn = ctk.CTkButton(self.ticket_window, text="Submit Ticket", command=self.submit_ticket)
        submit_btn.place(x= 120, y= 350)


        # Submit button
    def submit_ticket(self):
        name = self.name_entry.get()
        issue = self.issue_type.get()
        description = self.desc_box.get("0.0", "end").strip()

        if not name or not description:
            CTkMessagebox(title="Error", message="Please fill in all fields.", icon="cancel")
            return
        else:
            self.pending_ticket(name, issue, description)
            CTkMessagebox(
                title="Ticket Submitted",
                message="Your ticket has been successfully submitted!",
                icon="check"
            )
            self.ticket_window.destroy()



class ForgotPasswordUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Forgot Password")
        self.geometry('450x500')
        self.minsize(400, 500)

        self.generated_code = None
        
        self.fp_frame()
        self.fp_inputs()
        self.fp_button()
        self.mainloop()
        self.controller = None

    def fp_frame(self):
        self.frame = ctk.CTkFrame(self, width=390, height=490, corner_radius=1, fg_color="#0D1B2A")
        self.frame.pack(fill="both", expand=True)

        fp_label = ctk.CTkLabel(self.frame, text="Forgot\n Password", font=("Space Age", 40, "bold", "italic"), text_color="#00BFA5")
        fp_label.place(x= 60, y= 20)

    def fp_inputs(self):
        font_style = ctk.CTkFont(family="Arial", size=13, slant="italic")

        # Username / Email Entry
        self.username = ctk.CTkEntry(self.frame, width=200, height=40, fg_color="transparent", text_color="white")
        self.username.place(x=120, y=160)
        username_label = ctk.CTkLabel(self.frame, text="Email (Gmail)", text_color="white", font=font_style)
        username_label.place(x=125, y=130)

        # Verification Code Entry
        self.code_entry = ctk.CTkEntry(self.frame, width=200, height=40, fg_color="transparent", text_color="white")
        self.code_entry.place(x=120, y=230)
        code_label = ctk.CTkLabel(self.frame, text="Verification Code", text_color="white", font=font_style)
        code_label.place(x=125, y=200)

        # Send Code Button
        sendCodeButton = ctk.CTkButton(
            self.frame, text="Send Verification Code",
            width=200, height=30,
            fg_color="#13283d", hover_color="#00BFA5",
            command=self.generate_and_send_code
        )
        sendCodeButton.place(x=120, y=280)

        # New Password
        self.new_password = ctk.CTkEntry(self.frame, width=200, height=40, fg_color="transparent", text_color="white", show="*")
        self.new_password.place(x=120, y=340)
        new_password_label = ctk.CTkLabel(self.frame, text="New Password", text_color="white", font=font_style)
        new_password_label.place(x=125, y=310)

    def fp_button(self):
        # Show/Hide Password
        self.show_new_pass_checkbox = ctk.CTkCheckBox(
            self.frame, text="Show Password", command=self.toggle_new_password
        )
        self.show_new_pass_checkbox.place(x=120, y=390)

        # Submit Button
        submitButton = ctk.CTkButton(
            self.frame,
            text="Update Password",
            width=200,
            height=40,
            fg_color="#13283d",
            hover_color="#00BFA5",
            command=self.fp_submit_action
        )
        submitButton.place(x=120, y=420)
        
    def set_controller(self, controller):
        self.controller = controller
    def call_username(self):
        if not self.controller or not self.controller.current_user:
            return "User"
        first = self.controller.get_firstname(self.controller.current_user)
        return first if first else "User"

    def toggle_new_password(self):
        if self.show_new_pass_checkbox.get() == 1:
            self.new_password.configure(show="")
        else:
            self.new_password.configure(show="*")


    def generate_and_send_code(self):
        """Generate a 6-digit code and send it to user Gmail."""
        email = self.username.get().strip()

        if not email or "@gmail.com" not in email:
            CTkMessagebox(title="Invalid Email", message="Please enter a valid Gmail address.", icon="warning")
            return

        # Create verification code
        self.generated_code = str(random.randint(100000, 999999))

        # Email setup (YOU MUST EDIT THIS PART)
        sender_email = "lawrencerosario237@gmail.com"
        sender_password = "krcm zcnk jzus okke"  # Use App Password

        body = (f"Your verification code is: {self.generated_code}\nA sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.\n\nThis is a system-generated email. Please do not reply.\n\nThanks,\nThe ChatEase System\n\n")
        message = MIMEText(body, "plain")

        message["Subject"] = "[ChatEase] Verification Code!"
        message["From"] = sender_email
        message["To"] = email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            server.quit()

            CTkMessagebox(title="Code Sent", message="Verification code sent to Gmail.", icon="check")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to send email.\n{e}", icon="cancel")

    def calculate_strength(self, password):
        strength = 0
        if len(password) >= 12:
            strength += 2
        elif len(password) >= 8:
            strength += 1
        if re.search(r"[A-Z]", password):
            strength += 1
        if re.search(r"[a-z]", password):
            strength += 1
        if re.search(r"[0-9]", password):
            strength += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1
        return strength

    def fp_submit_action(self):
        username = self.username.get().strip()
        new_password = self.new_password.get().strip()

        # Check strong password
        strength = self.calculate_strength(new_password)
        if strength < 5:  # Require Strong or Excellent password
            CTkMessagebox(
                title="Weak Password",
                message="New password is not strong enough! Use uppercase, lowercase, numbers, symbols, and at least 8 characters.",
                icon="warning"
            )
            return  

        # If password is strong, proceed to update (replace with your controller logic)
        success = Controller.change_password(username, new_password)  # Replace this with: self.controller.change_password(username, old_password, new_password)
        if success:
            CTkMessagebox(title="Success", message="Password updated successfully!", icon="check")
        else:
            CTkMessagebox(title="Error", message="Update Failed! Check credentials.", icon="cancel")



class SignUpUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = Controller(view=self)
        self.title("Sign Up")
        self.geometry('400x600')
        self.minsize(400, 600)
        self.fp_frame()
        self.create_inputs()
        self.create_password_widgets()
        self.create_buttons()
        self.mainloop()

    def fp_frame(self):
        self.frame = ctk.CTkFrame(self, width=390, height=590, corner_radius=1, fg_color="#0D1B2A")
        self.frame.pack(fill="both", expand=True)

    def create_inputs(self):
        create_account_label = ctk.CTkLabel(self.frame, text="Create Account", fg_color="transparent", font= ("Space Age", 30, "bold"))
        create_account_label.place(x= 20, y = 50)
        font_style = ctk.CTkFont(family="Arial", size=13, slant="italic")
        
        # First Name
        self.firstName = ctk.CTkEntry(self.frame, width=140, height=35, fg_color="transparent", corner_radius=10, text_color="white")
        self.firstName.place(x=44, y=160)
        Firstname_label = ctk.CTkLabel(self.frame, text="Firstname", text_color="white", font=font_style)
        Firstname_label.place(x=55, y=130)

        # Last Name
        self.lastName = ctk.CTkEntry(self.frame, width=140, height=35, corner_radius=10, fg_color="transparent", text_color="white")
        self.lastName.place(x=214, y=160)
        Lastname_label = ctk.CTkLabel(self.frame, text="Lastname", text_color="white", font=font_style)
        Lastname_label.place(x=220, y=130)

        # Username
        self.createUsername = ctk.CTkEntry(self.frame, width=240, height=35, corner_radius=10, fg_color="transparent", text_color="white")
        self.createUsername.place(x=74, y=230)
        username_label = ctk.CTkLabel(self.frame, text="Username", text_color="white", font=font_style)
        username_label.place(x=85, y=200)

        # Password
        self.createPassword = ctk.CTkEntry(self.frame, width=240, height=35, corner_radius=10, fg_color="transparent", text_color="white", show="*")
        self.createPassword.place(x=74, y=300)
        password_label = ctk.CTkLabel(self.frame, text="Password", text_color="white", font=font_style)
        password_label.place(x=85, y=270)

    def create_password_widgets(self):
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame, width=240)
        self.progress_bar.place(x=74, y=380)

        # Result label
        self.result_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=12), text_color="white")
        self.result_label.place(x=74, y=390)

        # Suggestion label
        self.suggestion_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=10), text_color="white")
        self.suggestion_label.place(x=74, y=410)

        # Show/hide password
        self.show_pass_checkbox = ctk.CTkCheckBox(self.frame, text="Show Password", command=self.toggle_password)
        self.show_pass_checkbox.place(x=74, y=350)

        # Bind password strength check
        self.createPassword.bind("<KeyRelease>", lambda e: self.check_password())

    def toggle_password(self):
        if self.show_pass_checkbox.get() == 1:
            self.createPassword.configure(show="")
        else:
            self.createPassword.configure(show="*")

    def suggest_password(self, password):
        suggestions = []

        if not re.search(r"[A-Z]", password):
            suggestions.append(random.choice(string.ascii_uppercase))
        if not re.search(r"[a-z]", password):
            suggestions.append(random.choice(string.ascii_lowercase))
        if not re.search(r"[0-9]", password):
            suggestions.append(random.choice(string.digits))
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            suggestions.append(random.choice("!@#$%^&*()"))

        while len(password) + len(suggestions) < 8:
            suggestions.append(random.choice(string.ascii_letters + string.digits + "!@#$%^&*()"))

        return password + ''.join(suggestions)

    def calculate_strength(self, password):
        strength = 0
        if len(password) >= 12:
            strength += 2
        elif len(password) >= 8:
            strength += 1
        if re.search(r"[A-Z]", password):
            strength += 1
        if re.search(r"[a-z]", password):
            strength += 1
        if re.search(r"[0-9]", password):
            strength += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1
        return strength

    def check_password(self):
        password = self.createPassword.get()
        strength = self.calculate_strength(password)

        # Update progress bar
        self.progress_bar.set(strength / 6)

        # Update labels
        if strength <= 2:
            self.result_label.configure(text="Weak Password", text_color="red")
            self.suggestion_label.configure(text=f"Suggestion: {self.suggest_password(password)}")
        elif strength <= 4:
            self.result_label.configure(text="Moderate Password", text_color="orange")
            self.suggestion_label.configure(text="Add numbers or symbols for stronger protection.")
        elif strength == 5:
            self.result_label.configure(text="Strong Password 👍", text_color="green")
            self.suggestion_label.configure(text="")
        else:
            self.result_label.configure(text="Excellent Password 🔥", text_color="cyan")
            self.suggestion_label.configure(text="")

        # Enable/disable create account button
        if strength >= 5:  # Strong or Excellent
            self.create_button.configure(state="normal")
        else:
            self.create_button.configure(state="disabled")

    def create_buttons(self):
        self.create_button = ctk.CTkButton(
            self.frame,
            text="Create Account",
            width=200,
            height=40,
            corner_radius=20,
            border_width=0,
            bg_color="transparent",
            fg_color="#0E66B3",
            hover_color="#071647",
            command=self.controller.register_user
        )
        self.create_button.place(x=100, y=450)
        self.create_button.configure(state="disabled")  # Disabled initially


import os
from PIL import Image
from customtkinter import CTkImage

class Admin_Dashboard(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("ChatEase")
        self.geometry("1200x650")
        
        self.minsize(1200, 650)
        self.maxsize(1200, 650)
        

        # Chat session storage
        self.active_chat = None
        self.bg_greeting = None
        self.popup_frame = None  # placeholder
     

        self.load_images()
        self.main_frame()
        self.buttons()

        self.controller = Controller(self)

        

    
    def set_controller(self, controller):
        self.controller = controller
    # ------------------------------------------------------
    # MAIN FRAME
    # ------------------------------------------------------
    def load_images(self):
        self.bg = None  # Initialize to None as a fallback
        if os.path.exists("background_ADMIN.png"):
            try:
                bg_img = Image.open("background_ADMIN.png")
                self.bg = CTkImage(light_image=bg_img, size=(750, 500))
            except Exception as e:
                print("Error loading images:", e)
                self.bg = None
        else:
            print("Image file 'background_ADMIN.png' not found. Skipping background image.")


    def main_frame(self):
        main_frame = ctk.CTkFrame(self, width=1200, height=650, fg_color="#0D1B2A")
        main_frame.pack()

        # Main chat frame
        self.mainframe = ctk.CTkFrame(self, width=820, height=620, fg_color="#13283d", corner_radius=2)
        self.mainframe.place(x=360, y=10)

        if self.bg is not None:
            try:
                self.bg_label = ctk.CTkLabel(self.mainframe, image=self.bg, text="")
                self.bg_label.place(x=230, y=50)
            except Exception as e:
                print(f"Failed to display background image: {e}. Skipping.")
        else:
            print("No background image available. Proceeding without it.")


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

        self.bubble_target_y = 160     
        self.another_target_y = 240     


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
            font=logout_font,
            command=self.logout
        )
        self.logout_button.place(x=15, y=200)


        about_us_font = ctk.CTkFont(family="Arial", size=15, weight="bold")
        self.about_us = ctk.CTkButton(self.mainframe, width=100, height=50, text="About Us", command=self.open_popup, fg_color="transparent", font=about_us_font, hover_color="#00BFA5")
        self.about_us.place(x = 600, y = 30)

        admin_notification_font = ctk.CTkFont(family="Arial", size=15, weight="bold")
        self.about_us = ctk.CTkButton(self.mainframe, width=100, height=50, text="Notification",command=self.notification_popup, fg_color="transparent", font=admin_notification_font, hover_color="#00BFA5")
        self.about_us.place(x = 500, y = 30)


    def logout(self):
        # Close current dashboard window
        self.master.deiconify()
        self.destroy()
        # Reopen login/signup window
        login_window = Login_Signup()
        login_window.controller = self.controller

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
            font=("Space Age", 30, "bold"),
            text_color="#00BFA5"

        ).place(x=55, y= 20)

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
                 "information anytime and anywhere even without\n" 
                 "an internet connection, because all data is stored\n" 
                 "locally in our Database.",
                 
            justify="center", font=("Times New Roman", 15)
        ).place(x= 15, y= 70)

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
        tickets = self.controller.controller_ticket_getter()  # returns [(user, msg, date), ...]

        if not tickets:
            ctk.CTkLabel(
                self.popup_scrollable,
                text="No tickets found.",
                font=("Arial", 14)
            ).pack(pady=10)
        else:
            # Display each ticket as a clickable button
            for name, issue, pending_question in tickets:
                ticket_btn = ctk.CTkButton(
                    self.popup_scrollable,
                    text=f"{name}: {pending_question[:30]}...",  # show first 30 chars
                    width=280,
                    height=60,
                    fg_color="#1B1B1B",
                    hover_color="#00BFA5",
                    corner_radius=2,
                    anchor="w",
                    command=lambda u=name, m=issue, d=pending_question: self.open_ticket_frame(u, m, d)
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


    def open_ticket_frame(self, name, issue, pending_question):
        # Destroy previous frame if exists
        if getattr(self, "ticket_detail_frame", None):
            self.ticket_detail_frame.destroy()

        # Create a new frame
        self.ticket_detail_frame = ctk.CTkFrame(self, width=330, height=240, fg_color="#0D1B2A", corner_radius=2)
        self.ticket_detail_frame.place(x=380, y=100)

        # Add ticket details
        ctk.CTkLabel(self.ticket_detail_frame, text=f"From: {name}", font=("Arial", 18, "bold")).place(x= 10, y= 10)
        ctk.CTkLabel(self.ticket_detail_frame, text=f"Issue: {issue}", font=("Arial", 12, "italic")).place(x = 10, y= 30)
        ctk.CTkLabel(self.ticket_detail_frame, text=f"Message:\n{pending_question}", wraplength=250, justify = "left", font=("Arial", 13, "bold")).place(x = 10, y= 100)

        ctk.CTkButton(
            self.ticket_detail_frame,
            text="Remove",
            command=lambda: self.controller.controller_ticket_remove(name),
            hover_color="#00BFA5", 
            height= 30,
            font=("Arial", 15, "bold")
            ).place(x= 90, y =190)


        # Close button inside the frame
        ctk.CTkButton(
            self.ticket_detail_frame,
            text="Close",
            command=self.ticket_detail_frame.destroy,
            hover_color="#00BFA5", 
            height= 30,
            font=("Arial", 12),
            width= 60,
            corner_radius=10
        ).place(x= 250, y =10)




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

        self.desc_box = ctk.CTkTextbox(self.add_window, width=300, height=80, border_color="gray", border_width=1, fg_color="#13283d")
        self.desc_box.insert("0.0", "Enter the Answer here...")
        self.desc_box.place(x=50, y=150)

        self.keywords = ctk.CTkEntry(self.add_window, placeholder_text="Enter a keywords?", width=300, height=60, fg_color="#13283d")
        self.keywords.place(x=50, y=250)

        submit_btn = ctk.CTkButton(self.add_window, text="Save to Database", command=lambda: self.controller.add_answer_submit(self), width=150, hover_color="#00BFA5", fg_color="#0D1B2A")
        submit_btn.place(x=125, y=370)




    
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

        update_submit_btn = ctk.CTkButton(self.update_window, text="Update", command=lambda:self.controller.update_answer_submit(self), width=150, hover_color="#00BFA5", fg_color="#0D1B2A")
        update_submit_btn.place(x=125, y=370)






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
        delete_submit_btn = ctk.CTkButton(self.delete_window, text="Delete", command=lambda: self.controller.delete_answer_submit(self, self.delete_answer_entry.get()),
                                        width=100, height=50, hover_color="#00BFA5", fg_color="#0D1B2A")
        delete_submit_btn.place(x=140, y=370)




# ------------------------------------------------------
# RUN APP
# ------------------------------------------------------