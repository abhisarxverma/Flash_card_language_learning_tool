from tkinter import *
import random
import pandas

language = None
current_card = {}
flip_start =None
to_learn = None


BACKGROUND_COLOR = "#B1DDC6"

class FlashCard(Canvas):
    def __init__(self, master):
        super().__init__(master, width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
        self.front_image = PhotoImage(file='images/card_front.png')
        self.back_image = PhotoImage(file='images/card_back.png')
        self.tick = PhotoImage(file='images/right.png')
        self.cross = PhotoImage(file='images/wrong.png')
        self.image = self.create_image(400, 263, image=self.front_image)
        self.word = self.create_text(400, 253, text='', font=('arial', 70, 'normal'))
        self.title = self.create_text(400, 130, text='', font=('inter', 30, 'italic'))
        self.previous_word= self.create_text(400, 400, text='', font=('arial', 25, 'normal'))
        self.grid(row=0, column=0, columnspan=2)

        self.right_button = Button(image=self.tick, highlightthickness=0, borderwidth=0)
        self.right_button.grid(row=1, column=0)

        self.wrong_button = Button(image=self.cross, highlightthickness=0, borderwidth=0)
        self.wrong_button.grid(row=1, column=1)

def next_card():
    global current_card, flip_start
    window.after_cancel(flip_start)
    current_card = random.choice(to_learn)
    flashcard.itemconfig(flashcard.title, text=language, fill='black')
    flashcard.itemconfig(flashcard.word, text=current_card[language], fill='black')
    flashcard.itemconfig(flashcard.image, image=flashcard.front_image)

    flip_start = window.after(3000, flip_card)

def flip_card():
    flashcard.itemconfig(flashcard.image, image=flashcard.back_image)
    if language == 'English':
        flashcard.itemconfig(flashcard.word, text=current_card['Hindi'], fill='white', font=('arial', 50, 'normal'))
        flashcard.itemconfig(flashcard.title, text='Hindi', fill='white')
    else:
        flashcard.itemconfig(flashcard.word, text=current_card['English'], fill='white')
        flashcard.itemconfig(flashcard.title, text='English', fill='white')
    flashcard.itemconfig(flashcard.previous_word, text = current_card[language], fill='white')

def guessed_right():
    global current_card, to_learn
    to_learn.remove(current_card)
    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv('data/words_to_learn_spanish.csv', index=False)
    

def set_language(lang):
    global language, language1, language2, flip_start, to_learn
    language = lang
    flashcard.delete(language1)
    flashcard.delete(language2)
    flashcard.delete(language3)
    flashcard.delete(language4)
    flashcard.itemconfig(flashcard.title, text='', font=('inter', 30, 'italic'))
    flashcard.right_button.config(command=guessed_right)
    flashcard.wrong_button.config(command=next_card)
    try:
        data = pandas.read_csv(f'words_to_learn_{language}.csv')
    except FileNotFoundError:
        data = pandas.read_csv(f'data/{language}_data.csv')
    finally:
        to_learn = data.to_dict(orient='records')

    flip_start = window.after(3000, flip_card)
    next_card()
    

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

if __name__ == "__main__":
    flashcard = FlashCard(window)

flashcard.itemconfig(flashcard.title, text='Select Language', font=('arial', 45, 'normal'))
language1 = flashcard.create_text(250, 270, text='French', font=('inter', 40, 'bold'), fill=BACKGROUND_COLOR)
flashcard.tag_bind(language1, '<Button-1>', lambda e: set_language('French'))
language2 = flashcard.create_text(530, 270, text='Spanish', font=('inter', 40, 'bold'), fill=BACKGROUND_COLOR)
flashcard.tag_bind(language2, '<Button-1>', lambda e: set_language('Spanish'))
language3 = flashcard.create_text(530, 340, text='Italian', font=('inter', 40, 'bold'), fill=BACKGROUND_COLOR)
flashcard.tag_bind(language3, '<Button-1>', lambda e: set_language('Italian'))
language4 = flashcard.create_text(250, 340, text='English', font=('inter', 40, 'bold'), fill=BACKGROUND_COLOR)
flashcard.tag_bind(language4, '<Button-1>', lambda e: set_language('English'))   
    

window.mainloop()
