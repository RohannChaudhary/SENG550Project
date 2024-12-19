import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from rec_system import df, cosine_sim, get_recommendations  # Import your recommendation function
from difflib import get_close_matches  # For fuzzy matching

# =============================
# Configuration
# =============================
ACCENT_COLOR = "#FF6F61"  # Coral for buttons
BACKGROUND_COLOR = "Black"  # Black rectangle in the center
TEXT_COLOR = "White"  # Text color
FONT_TITLE = ("Helvetica", 24, "bold")  # Title font
FONT_BUTTON = ("Helvetica", 14, "bold")  # Button font
FONT_TEXT = ("Helvetica", 14)  # General text font
FONT_RECOMMENDATIONS = ("Georgia", 14)  # Recommendations font
FONT_SUGGESTION = ("Helvetica", 12, "italic")  # Suggestion font

# =============================
# Functions
# =============================
def show_recommendations():
    title = entry.get()
    if not title.strip():
        messagebox.showwarning("Input Error", "Please enter a title!")
        return

    try:
        recommendations = get_recommendations(title, cosine_sim)
        if isinstance(recommendations, str):  # No recommendations found
            # Find the closest match
            closest_match = get_close_matches(title, df['title'].str.lower(), n=1, cutoff=0.5)
            if closest_match:
                suggestion = closest_match[0].title()
                suggestion_label.config(
                    text=f"Did you mean: {suggestion}?",
                    fg=ACCENT_COLOR,
                    cursor="hand2"
                )
                suggestion_label.bind("<Button-1>", lambda e: autofill_title(suggestion))
            else:
                suggestion_label.config(text="", cursor="")  # Clear suggestion
            result_label.config(text=recommendations, fg=ACCENT_COLOR)
        else:
            suggestion_label.config(text="", cursor="")  # Clear suggestion
            result_label.config(
                text="Top Recommendations:\n\n"
                     + "\n".join(recommendations.values),
                fg=TEXT_COLOR,
                font=FONT_RECOMMENDATIONS
            )
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg=ACCENT_COLOR)

def autofill_title(suggestion):
    """Autofill the input field with the suggested title and search."""
    entry.delete(0, tk.END)
    entry.insert(0, suggestion)
    show_recommendations()

# =============================
# GUI Setup
# =============================
root = tk.Tk()
root.title("Netflix Recommender System")
root.geometry("900x600")

# Load and set the background image
bg_image = Image.open("rec_system/gui_bg.webp")
bg_image = bg_image.resize((900, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Black rectangle as a centerpiece
center_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)

# =============================
# Widgets
# =============================
# Header
header = tk.Label(
    center_frame,
    text="NETFLIX RECOMMENDER",
    font=FONT_TITLE,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    pady=20
)
header.pack()

# Input Box
entry_frame = tk.Frame(center_frame, bg=BACKGROUND_COLOR)
entry_frame.pack(pady=10)

entry = tk.Entry(
    entry_frame,
    font=FONT_TEXT,
    width=40,
    relief="solid",
    highlightthickness=2,
    highlightbackground=ACCENT_COLOR
)
entry.pack(ipady=10)

# Suggestion Section
suggestion_label = tk.Label(
    center_frame,
    text="",
    font=FONT_SUGGESTION,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
   
)
suggestion_label.pack()

# Button
recommend_button = tk.Button(
    center_frame,
    text="Get Recommendations",
    command=show_recommendations,
    font=FONT_BUTTON,
    bg=ACCENT_COLOR,
    fg=ACCENT_COLOR,
    activebackground=ACCENT_COLOR,
    activeforeground=ACCENT_COLOR,
    relief="solid",  # Adds a solid border
    borderwidth=1,   # Thickness of the inner border
    highlightthickness=2,  # Thickness of the outer border
    highlightbackground=ACCENT_COLOR,
    padx=15,
    pady=10
)



recommend_button.pack(pady=20)

# Results Section
result_label = tk.Label(
    center_frame,
    text="",
    font=FONT_RECOMMENDATIONS,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    wraplength=450,
    justify="left",
    pady=5,
)
result_label.pack()

# =============================
# Run Application
# =============================
root.mainloop()
