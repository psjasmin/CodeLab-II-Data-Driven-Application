# Import Tkinter & Modules
from tkinter import *
from PIL import Image, ImageTk
import requests
import random
from io import BytesIO

main = Tk()
main.title('Mystic Brew')
main.geometry('765x514')
main.resizable(0, 0)


# Function for switching frames
def switch_to_frame(frame):
    frame.tkraise()

# Class for Fetching Potion Data
class PotionDataFetcher:
    def __init__(self, difficulty, name_textbox, effect_textbox, character_textbox, ingredients_textbox, image_label):
        self.difficulty = difficulty
        self.name_textbox = name_textbox
        self.effect_textbox = effect_textbox
        self.character_textbox = character_textbox
        self.ingredients_textbox = ingredients_textbox
        self.image_label = image_label


    # Function for Retrieving Potion Data (w/ regards to course difficulty)
    def get_potion_data(self):
        url = f"https://api.potterdb.com/v1/potions?filter[difficulty_matches]={self.difficulty}"
        response = requests.get(url)
        data = response.json()

        n = random.randint(0, len(data['data']) - 1)

        potion_name = data["data"][n]['attributes']['name']
        self.name_textbox.delete("1.0", END)
        self.name_textbox.tag_configure("center", justify="center")
        self.name_textbox.insert("1.0", potion_name, "center")

        potion_effect = data["data"][n]['attributes']['effect']
        self.effect_textbox.delete("1.0", END)
        self.effect_textbox.insert(END, potion_effect)

        # Checks if Retrieved Data is Valid
        # Displays Required Information
        potion_characteristics = data["data"][n]['attributes']['characteristics']
        if potion_characteristics is None:
            self.character_textbox.delete("1.0", END)
            self.character_textbox.insert(END, "Characteristics Not Found")
        else:
            bullet_points = " \u2022 "
            characteristics_list = potion_characteristics.split(', ')
            self.character_textbox.delete("1.0", END)
            for point in characteristics_list:
                self.character_textbox.insert(END, bullet_points + point + '\n')

        potion_ingredients = data["data"][n]['attributes']['ingredients']
        if potion_ingredients is None:
            self.ingredients_textbox.delete("1.0", END)
            self.ingredients_textbox.insert(END, "Ingredients Not Found")
        else:
            self.ingredients_textbox.delete("1.0", END)
            self.ingredients_textbox.insert(END, potion_ingredients)

        image_url = data['data'][n]['attributes']['image']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((int(175.03), int(160.79)))
            image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=image)
            self.image_label.image = image
        else:
            placeholder_image = Image.open("Images/Backgrounds/Image-Not-Found.png")
            placeholder_image = placeholder_image.resize(
                (int(175.03), int(160.79)))
            placeholder_image = ImageTk.PhotoImage(placeholder_image)
            self.image_label.configure(image=placeholder_image)
            self.image_label.image = placeholder_image


# Function for getting Beginner potions data
def getBeginnerPotions():
    beginner_fetcher = PotionDataFetcher("Beginner", potionName_B, effect_textbox1, character_textbox1, ingredients_textbox1, potion_imageB)
    beginner_fetcher.get_potion_data()


# Function for getting Moderate potions data
def getModeratePotions():
    moderate_fetcher = PotionDataFetcher("Moderate", potionName_M, effect_textbox2, character_textbox2, ingredients_textbox2, potion_imageM)
    moderate_fetcher.get_potion_data()


# Function for getting Advanced potions data
def getAdvancedPotions():
    advanced_fetcher = PotionDataFetcher("Advanced", potionName_A, effect_textbox3, character_textbox3, ingredients_textbox3, potion_imageA)
    advanced_fetcher.get_potion_data()


# --FRAME 1: HOME SCREEN--
HomeFrame = Frame(main, width=765, height=514)
HomeFrame.place(x=0, y=0)

# Home Screen BG Image
image = Image.open("Images/Backgrounds/HomeFrame.png")
resize_image = image.resize((765, 514))
home_bg = ImageTk.PhotoImage(resize_image)
home_bg_label = Label(HomeFrame, image=home_bg).place(x=-2, y=-2)

# Get Started Button
StartButton = Button(HomeFrame, text="Start Brewing", font=("Times New Roman", 15, 'italic'),
                     bg="#C3AD73", fg="#FDF4DF", activeforeground="#FDF4DF", activebackground="#C3AD73",
                     relief="ridge", command=lambda: switch_to_frame(ContentFrame)).place(relx=0.58, rely=0.6, height=42, width=180, anchor=CENTER)


# --FRAME 2: MAIN CONTENT--
ContentFrame = Frame(main, width=765, height=514)
ContentFrame.place(x=0, y=0)

# Header Background Image
header_bgimage = ImageTk.PhotoImage(Image.open("Images/Backgrounds/Header.png"))
header_canvas = Canvas(ContentFrame, width=900, height=800, bd=0, highlightthickness=0)
header_canvas.pack()
header_canvas.create_image(0, 0, anchor=NW, image=header_bgimage)


# Content 1-Course Level Select
def course_level():
    f1 = Frame(ContentFrame, width=765, height=450)
    f1.place(x=0, y=63)

    # Course Level BG Image
    image = Image.open("Images/Backgrounds/CourseContent.png")
    resize_image = image.resize((765, 450))
    home_bg = ImageTk.PhotoImage(resize_image)
    home_bg_label = Label(f1, image=home_bg, bg=ContentFrame.cget(
        "bg"), borderwidth=0, highlightthickness=0)
    home_bg_label.image = home_bg
    home_bg_label.place(x=0, y=0)

    # Beginner Course Button
    beginner = Button(f1, text="Beginner",
                      font=("Times New Roman", 16, 'bold', 'italic'), bg="#C2CAAE", fg="#FDF4DF",
                      activeforeground="#FDF4DF", activebackground="#C2CAAE",
                      relief="ridge", command=lambda: switch_to_frame(BeginnerFrame))
    beginner.place(relx=0.25, rely=0.87, height=42, width=140, anchor=CENTER)

    # Moderate Course Button
    moderate = Button(f1, text="Moderate",
                      font=("Times New Roman", 16, 'bold', 'italic'), bg="#E5C3A7", fg="#FDF4DF",
                      activeforeground="#FDF4DF", activebackground="#E5C3A7",
                      relief="ridge", command=lambda: switch_to_frame(ModerateFrame))
    moderate.place(relx=0.53, rely=0.87, height=42, width=140, anchor=CENTER)

    # Advanced Course Button
    advanced = Button(f1, text="Advanced",
                      font=("Times New Roman", 16, 'bold', 'italic'), bg="#B7B1B1", fg="#FDF4DF",
                      activeforeground="#FDF4DF", activebackground="#B7B1B1",
                      relief="ridge", command=lambda: switch_to_frame(AdvancedFrame))
    advanced.place(relx=0.80, rely=0.87, height=42, width=140, anchor=CENTER)

    toggle_win()


# Content 2-Instructions
def instructions():
    f1.destroy()
    f2 = Frame(ContentFrame, width=765, height=450)
    f2.place(x=0, y=63)

    # Instructions BG Image
    instructions = Image.open("Images/Backgrounds/InstructionsContent.png")
    resize_instructions = instructions.resize((765, 450))
    instructions_bg = ImageTk.PhotoImage(resize_instructions)
    instructions_bg_label = Label(f2, image=instructions_bg, bg=ContentFrame.cget(
        "bg"), borderwidth=0, highlightthickness=0)
    instructions_bg_label.image = instructions_bg
    instructions_bg_label.place(x=0, y=0)

    toggle_win()


# Toggle Menu Bar
def toggle_win():
    global f1

    # Destroy the existing frame if it exists
    if 'f1' in globals():
        f1.destroy()

    f1 = Frame(main, width=170, height=160, bg='#C3CDC2')
    f1.place(x=0, y=0)

    # Menu Options Buttons
    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            menuButtons['background'] = bcolor
            menuButtons['foreground'] = '#3A3B36'

        def on_leavea(e):
            menuButtons['background'] = fcolor
            menuButtons['foreground'] = '#FDF4DF'

        menuButtons = Button(f1, text=text,
                             width=33, height=1, fg='#FDF4DF', border=0, font=('Times New Roman', 11, 'italic'),
                             bg=fcolor, activeforeground='#3A3B36', activebackground=bcolor, command=cmd)

        menuButtons.bind("<Enter>", on_entera)
        menuButtons.bind("<Leave>", on_leavea)

        menuButtons.place(x=x, y=y)

    # Menu Options (position/label/hover/bg/function call-out)
    bttn(-50, 60, 'COURSE LEVELS', '#FDF4DF', '#C3CDC2', course_level)
    bttn(-50, 90, 'INSTRUCTIONS', '#FDF4DF', '#C3CDC2', instructions)
    bttn(-50, 120, 'EXIT', '#FDF4DF', '#C3CDC2', lambda: switch_to_frame(HomeFrame))

    # Delete existing content to change frames
    def dele():
        global f1
        if 'f1' in globals():
            f1.destroy()

    # Menu close icon button
    global menu_close_button
    menu_close_button = ImageTk.PhotoImage(Image.open("Images/Buttons/menu-close.png"))
    Button(f1, image=menu_close_button, border=0, command=dele,
           bg='#C3CDC2', activebackground='#C3CDC2').place(x=20, y=20)

# Menu open icon button
menu_open_button = ImageTk.PhotoImage(Image.open("Images/Buttons/menu-open.png"))
global b2
b2 = Button(ContentFrame, image=menu_open_button, command=toggle_win, border=0,
            bg='#DFD1B9', activebackground='#DFD1B9').place(x=20, y=20, height=30, width=40)

# Initialize the Menu
course_level()


# --FRAME 3: BEGINNER COURSE--
BeginnerFrame = Frame(main, width=765, height=514)
BeginnerFrame.place(x=0, y=0)

# Beginner Course BG Image
beginner_image = Image.open("Images/Backgrounds/BeginnerFrame.png")
resize_beginner = beginner_image.resize((765, 514))
beginner_bg = ImageTk.PhotoImage(resize_beginner)
beginner_bg_label = Label(BeginnerFrame, image=beginner_bg).place(x=-2, y=-2)

# Back Button
back_button_image1 = ImageTk.PhotoImage(Image.open("Images/Buttons/back-button.png"))
back_button1 = Button(BeginnerFrame, image=back_button_image1, border=0,
                      bg='#DFD1B9', activebackground='#DFD1B9', command=lambda: switch_to_frame(ContentFrame))
back_button1.place(x=20, y=25, height=30, width=40)

# Random Generate (Beginner) Button
beginnerGenerate = Button(BeginnerFrame, text="Generate a Potion", font=("Vivaldi", 19, 'bold', 'italic'),
                          bg="#C3CDC2", fg="#FFF8E9", activeforeground="#FFF8E9", activebackground="#C3CDC2",
                          relief="ridge", command=getBeginnerPotions)
beginnerGenerate.place(relx=0.53, rely=0.14, width=220, height=43)

# Potion title text box
potionName_B = Text(BeginnerFrame, width=12, height=2, font=('Times New Roman', 15, 'italic'),
                    bg='#CED2C1', fg='#3F403B', wrap='word', relief=FLAT)
potionName_B.place(relx=0.24, rely=0.26)

# Effect title & text box
effect = Label(BeginnerFrame, text="Effect:", font=('Times New Roman', 11, 'bold', 'italic'),
               bg='#E9E0D0', fg='#4F4C46')
effect.place(relx=0.49, rely=0.38)
effect_textbox1 = Text(BeginnerFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                       bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
effect_textbox1.place(relx=0.495, rely=0.43)

# Characteristics title & text box
characteristics = Label(BeginnerFrame, text="Characteristics:", font=('Times New Roman', 11, 'bold', 'italic'),
                        bg='#E9E0D0', fg='#4F4C46')
characteristics.place(relx=0.49, rely=0.51)
character_textbox1 = Text(BeginnerFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'), 
                          bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
character_textbox1.place(relx=0.495, rely=0.56)

# Ingredients title & text box
ingredients = Label(BeginnerFrame, text="Ingredients:", font=('Times New Roman', 11, 'bold', 'italic'),
                    bg='#E9E0D0', fg='#4F4C46')
ingredients.place(relx=0.49, rely=0.64)
ingredients_textbox1 = Text(BeginnerFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                            bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
ingredients_textbox1.place(relx=0.495, rely=0.69)

# Potion Image
potion_imageB = Label(BeginnerFrame, bg='#E9E0D0')
potion_imageB.place(relx=0.235, rely=0.47)


# --FRAME 4: MODERATE COURSE--
ModerateFrame = Frame(main, width=765, height=514)
ModerateFrame.place(x=0, y=0)

# Moderate Course BG Image
moderate_image = Image.open("Images/Backgrounds/ModerateFrame.png")
resize_moderate = moderate_image.resize((765, 514))
moderate_bg = ImageTk.PhotoImage(resize_moderate)
moderate_bg_label = Label(ModerateFrame, image=moderate_bg).place(x=-2, y=-2)

# Back Button
back_button_image2 = ImageTk.PhotoImage(Image.open("Images/Buttons/back-button.png"))
back_button2 = Button(ModerateFrame, image=back_button_image2, border=0, bg='#DFD1B9',
                      activebackground='#DFD1B9', command=lambda: switch_to_frame(ContentFrame))
back_button2.place(x=20, y=25, height=30, width=40)

# Random Generate (Moderate) Button
moderateGenerate = Button(ModerateFrame, text="Generate a Potion", font=("Vivaldi", 19, 'bold', 'italic'), 
                          bg="#C3CDC2", fg="#FFF8E9", activeforeground="#FFF8E9", activebackground="#C3CDC2",
                          relief="ridge", command=getModeratePotions)
moderateGenerate.place(relx=0.53, rely=0.14, width=220, height=43)

# Potion title text box
potionName_M = Text(ModerateFrame, width=12, height=2, font=('Times New Roman', 15, 'italic'),
                    bg='#CED2C1', fg='#3F403B', wrap='word', relief=FLAT)
potionName_M.place(relx=0.24, rely=0.26)

# Effect title & text box
effect_M = Label(ModerateFrame, text="Effect:", font=('Times New Roman', 11, 'bold', 'italic'),
                 bg='#E9E0D0', fg='#4F4C46')
effect_M.place(relx=0.49, rely=0.38)
effect_textbox2 = Text(ModerateFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                    bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
effect_textbox2.place(relx=0.495, rely=0.43)

# Characteristics title & text box
characteristics_M = Label(ModerateFrame, text="Characteristics:", font=('Times New Roman', 11, 'bold', 'italic'),
                          bg='#E9E0D0', fg='#4F4C46')
characteristics_M.place(relx=0.49, rely=0.51)
character_textbox2 = Text(ModerateFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                          bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
character_textbox2.place(relx=0.495, rely=0.56)

# Ingredients title & text box
ingredients_M = Label(ModerateFrame, text="Ingredients:", font=('Times New Roman', 11, 'bold', 'italic'),
                      bg='#E9E0D0', fg='#4F4C46')
ingredients_M.place(relx=0.49, rely=0.64)
ingredients_textbox2 = Text(ModerateFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                        bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
ingredients_textbox2.place(relx=0.495, rely=0.69)

# Potion Image
potion_imageM = Label(ModerateFrame, bg='#E9E0D0')
potion_imageM.place(relx=0.235, rely=0.47)


# --FRAME 6: ADVANCED COURSE--
AdvancedFrame = Frame(main, width=765, height=514)
AdvancedFrame.place(x=0, y=0)

# Advanced Course BG Image
advanced_image = Image.open("Images/Backgrounds/AdvancedFrame.png")
resize_advanced = advanced_image.resize((765, 514))
advanced_bg = ImageTk.PhotoImage(resize_advanced)
advanced_bg_label = Label(AdvancedFrame, image=advanced_bg).place(x=-2, y=-2)

# Back Button
back_button_image3 = ImageTk.PhotoImage(Image.open("Images/Buttons/back-button.png"))
back_button3 = Button(AdvancedFrame, image=back_button_image3, border=0,
                      bg='#DFD1B9', activebackground='#DFD1B9', command=lambda: switch_to_frame(ContentFrame))
back_button3.place(x=20, y=25, height=30, width=40)

# Random Generate (Moderate) Button
advancedGenerate = Button(AdvancedFrame, text="Generate a Potion", font=("Vivaldi", 19, 'bold', 'italic'),
                          bg="#C3CDC2", fg="#FFF8E9", activeforeground="#FFF8E9", activebackground="#C3CDC2",
                          relief="ridge", command=getAdvancedPotions)
advancedGenerate.place(relx=0.53, rely=0.14, width=220, height=43)

# Potion title text box
potionName_A = Text(AdvancedFrame, width=12, height=2, font=('Times New Roman', 15, 'italic'),
                    bg='#CED2C1', fg='#3F403B', wrap='word', relief=FLAT)
potionName_A.place(relx=0.24, rely=0.26)

# Effect title & text box
effect_A = Label(AdvancedFrame, text="Effect:", font=('Times New Roman', 11, 'bold', 'italic'),
                 bg='#E9E0D0', fg='#4F4C46')
effect_A.place(relx=0.49, rely=0.38)
effect_textbox3 = Text(AdvancedFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                       bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
effect_textbox3.place(relx=0.495, rely=0.43)

# Characteristics title & text box
characteristics_A = Label(AdvancedFrame, text="Characteristics:", font=('Times New Roman', 11, 'bold', 'italic'),
                          bg='#E9E0D0', fg='#4F4C46')
characteristics_A.place(relx=0.49, rely=0.51)
character_textbox3 = Text(AdvancedFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                          bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
character_textbox3.place(relx=0.495, rely=0.56)

# Ingredients title & text box
ingredients_A = Label(AdvancedFrame, text="Ingredients:", font=('Times New Roman', 11, 'bold', 'italic'),
                      bg='#E9E0D0', fg='#4F4C46')
ingredients_A.place(relx=0.49, rely=0.64)
ingredients_textbox3 = Text(AdvancedFrame, width=31, height=2, font=('Times New Roman', 10, 'italic'),
                        bg='#E9E0D0', fg='#4F4C46', wrap='word', relief=FLAT)
ingredients_textbox3.place(relx=0.495, rely=0.69)

# Potion Image
potion_imageA = Label(AdvancedFrame, bg='#E9E0D0')
potion_imageA.place(relx=0.235, rely=0.47)

# Show Initial Frame
switch_to_frame(HomeFrame)

main.mainloop()