# ============== Import statements ==============
from tkinter import * 
from tkinter import messagebox 
import customtkinter as ctk 
from fonts import TITLE_FONT, BODY_FONT, BUTTON_FONT
from custom_theme import *
import json 
from datetime import datetime

root = ctk.CTk(fg_color=BACKGROUND)

current_theme = THEMES["Ember"]

root.title("Notes App")
root.after(100, lambda: root.state("zoomed"))

# Header
headerFrame = ctk.CTkFrame(root, fg_color=BACKGROUND)
headerFrame.pack(fill="x", padx=20, pady=20)

headerLabelTitle = ctk.CTkLabel(headerFrame, text="Brain Dump 📝", font=TITLE_FONT, text_color=current_theme["primary"])
headerLabelTitle.pack(pady=20)

# Textbox
inputFrame = ctk.CTkFrame(root,fg_color=BACKGROUND)
inputFrame.pack(fill="x", padx=20, pady=20)

textbox = ctk.CTkTextbox(inputFrame,
        height=200,
        font=BODY_FONT,
        fg_color=CARD,
        text_color=TEXT_SECONDARY,
        border_width=2,
        border_color=CARD
        )
textbox.pack(fill="x")

# Textbox Buttons
buttonsFrame = ctk.CTkFrame(root, fg_color=BACKGROUND)
buttonsFrame.pack(fill="x", padx=20, pady=20)

# Creating an empty list for notes
notes = []

editing_index = None

# Function to create a card with index 
def create_card(note, index):
    # Calculating row and col
    NUM_COLUMNS = 4
    row = index // NUM_COLUMNS
    column = index % NUM_COLUMNS

    # Creating a card
    card = ctk.CTkFrame(cardsContainer, fg_color=CARD)
    card.grid(row=row, column=column, padx=10, pady=10, sticky="nw")
    card.grid_columnconfigure(0, weight=1)

    noteText = ctk.CTkLabel(
                card,
                text=note["text"],
                text_color=TEXT, 
                font=BODY_FONT, 
                wraplength=300,
                justify="left",
                anchor="w"
                )
    noteText.grid(row=0, column=0,  sticky="w", padx=15,pady=(15, 10))

    dateCreatedLabel = ctk.CTkLabel(
                card,
                text=f"Created: {note["created"]}",
                text_color=TEXT_SECONDARY, 
                font=("Segoe UI", 16), 
                wraplength=300,
                justify="left",
                anchor="w"
                )
    dateCreatedLabel.grid(row=1, column=0, sticky="w", padx=15)

    editedLabel = ctk.CTkLabel(
                card,
                text=f"Edited: {note["edited"]}",
                text_color=TEXT_SECONDARY, 
                font=("Segoe UI", 16), 
                wraplength=300,
                justify="left",
                anchor="w"
                )
    editedLabel.grid(row=2, column=0, sticky="w", padx=15)

    editDelButtonFrame = ctk.CTkFrame(card, fg_color=CARD)
    editDelButtonFrame.grid(row=3, column=0, sticky="w",padx=10,pady=(0, 10))

    editBtn = ctk.CTkButton(
                editDelButtonFrame,
                text="Edit",
                fg_color=CASEBUTTONS,
                hover_color=CASEBUTTONSHOVER,
                height=42,
                width=42,
                cursor="hand2",
                font=BUTTON_FONT,
                anchor="w",
                command=lambda: edit_note(index)
                )
    editBtn.pack(side="left", padx=(0,15), pady=10)

    deleteBtn = ctk.CTkButton(
                editDelButtonFrame,
                text="Delete",
                fg_color=ERROR,
                hover_color=ERROR,
                height=42,
                width=42,
                cursor="hand2",
                font=BUTTON_FONT,
                anchor="w",
                command=lambda:delete_note(index)
                )
    deleteBtn.pack(side="left", pady=10)

# Function to handle notes - either add a new note or save changes to edited note
def handle_note():
    if editing_index == None:
        add_note()
    else:
        save_changes()

# Function to add note 
def add_note():
    note = textbox.get("1.0", "end-1c").strip()
    if note == "":
        return 
    created = datetime.now().strftime("%d %b %Y, %I:%M %p")
    new_note = {
        "text": note, 
        "edited": None, 
        "pinned": False,
        "created": created
    }

    notes.append(new_note)

    create_card(new_note, len(notes)-1)
    textbox.delete("1.0", "end")
    save_notes()

# Function to save notes in notes.json file
def save_notes():
    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4)

# Function to load notes when application is opened
def load_notes():
    global notes 
    try:
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []
        save_notes()

    for index, note in enumerate(notes):
        create_card(note, index)

# Function to delete note
def delete_note(index):
    answer = messagebox.askyesno("Delete Note","Are you sure you want to delete this note?") # returns true or false

    if not answer: # means cancel note deletion
        return 

    notes.pop(index)
    save_notes()
    refresh_notes()

# Function to refresh cards 
def refresh_notes():
    for widget in cardsContainer.winfo_children():
        widget.destroy()

    for index, note in enumerate(notes):
        create_card(note, index)

# Function to edit a note
def edit_note(index): 
    global editing_index
    editing_index = index 
    textbox.delete("1.0", "end")
    textbox.insert("1.0", notes[index]["text"])
    addNoteBtn.configure(text="Save Changes")

def save_changes():
    global editing_index
    notes[editing_index]["text"] = textbox.get("1.0", "end-1c").strip()
    notes[editing_index]["edited"] =  datetime.now().strftime("%d %b %Y, %I:%M %p") 
    save_notes()
    refresh_notes()
    textbox.delete("1.0", "end")
    editing_index = None
    addNoteBtn.configure(text="Add Note")

# Add note button
addNoteBtn = ctk.CTkButton(
            buttonsFrame,
            cursor="hand2",
            fg_color=current_theme["primary"],
            hover_color=current_theme["hover"],
            text="Add Note",
            height=44,
            corner_radius=4,
            font=BODY_FONT,
            text_color=TEXT,
            command=handle_note 
            )
addNoteBtn.pack(padx=(0, 25), pady=10, side="left")

# Function to change the case of textbox text
def change_case(case_type):
    text = textbox.get("1.0", "end-1c")
    if case_type == "Uppercase":
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text.upper())

    elif case_type == "Lowercase":
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text.lower())

    elif case_type == "Titlecase":
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text.title())

# Uppercase button
upperCaseBtn = ctk.CTkButton(
            buttonsFrame,
            cursor="hand2",
            fg_color=CASEBUTTONS,
            hover_color=CASEBUTTONSHOVER,
            text="Uppercase",
            height=44, 
            corner_radius=4, 
            font=BODY_FONT, 
            text_color=TEXT,
            command= lambda: change_case("Uppercase")
            )
upperCaseBtn.pack(padx=(0, 25), pady=10, side="left")

# Lowercase button 
lowerCaseBtn = ctk.CTkButton(
            buttonsFrame,
            cursor="hand2",
            fg_color=CASEBUTTONS,
            hover_color=CASEBUTTONSHOVER,
            text="Lowercase",
            height=44, 
            corner_radius=4, 
            font=BODY_FONT, 
            text_color=TEXT,
            command= lambda: change_case("Lowercase")
            )
lowerCaseBtn.pack(padx=(0, 25), pady=10, side="left")

# Titlecase button 
titleCaseBtn = ctk.CTkButton(
            buttonsFrame, 
            cursor="hand2",
            fg_color=CASEBUTTONS,
            hover_color=CASEBUTTONSHOVER,
            text="Titlecase",
            height=44, 
            corner_radius=4, 
            font=BODY_FONT, 
            text_color=TEXT,
            command= lambda: change_case("Titlecase")
            )
titleCaseBtn.pack(padx=(0, 25), pady=10, side="left")

# Function to clear the textbox text
def clearText():
    textbox.delete(0.0, 'end')

# Clear button
clearBtn = ctk.CTkButton(
            buttonsFrame,
            cursor="hand2",
            fg_color=ERROR,
            hover_color=ERROR,
            text="Clear",
            height=44,
            corner_radius=4,
            font=BODY_FONT,
            text_color=TEXT,
            command=clearText
            )
clearBtn.pack(padx=(0, 25), pady=10, side="left")

# Function to apply theme
def apply_theme():
    addNoteBtn.configure(fg_color=current_theme["primary"],hover_color=current_theme["hover"])
    headerLabelTitle.configure(text_color=current_theme["primary"])

# Function to change theme 
def change_theme(choice): 
    global current_theme
    current_theme = THEMES[choice]
    apply_theme()

# Theme choices dropdown
themeComboBox = ctk.CTkComboBox(
            buttonsFrame, 
            values=list(THEMES.keys()),

            fg_color=CARD,
            border_color=CARD,
            button_color=CARD,

            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD,
            dropdown_font=BODY_FONT,

            text_color=TEXT,
            dropdown_text_color=TEXT,
            width=150,
            height=44,

            font=BODY_FONT,
            command=change_theme
            )
themeComboBox.set("Ember")
themeComboBox.pack(side="right", padx=20)

# Notes section
sframe = ctk.CTkScrollableFrame(root, fg_color=BACKGROUND)
sframe.pack(pady=30, padx=10,  fill="both", expand=True,)

cardsContainer = ctk.CTkFrame(sframe, fg_color=BACKGROUND)
cardsContainer.pack(fill="x", anchor="w")

load_notes()


root.mainloop()
