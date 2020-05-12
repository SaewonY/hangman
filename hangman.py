import random
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image 


def visualize_hangman(turns=10, width=100, height=200, reset=False, victory=False):
      
    image_path = f'hangman_{turns}_chances.png'

    if reset:
        image_path = f'hangman.png'
    
    if victory:
        image_path = f'victory.png'

    # opens the image 
    img = Image.open(image_path) 
    img = img.resize((width, height), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 

    # create a label 
    panel = Label(window, image=img) 
    panel.image = img 
    panel.grid(row=12, column=1) 


# window size config
def window_config(window, width_ratio=1.5, height_ratio=2.3):
    window.title("HANGMAN")
    window.update_idletasks()
    width = window.winfo_width() * width_ratio
    height = window.winfo_height() * height_ratio
    window.geometry('{}x{}+200+200'.format(int(width), int(height)))
    window.resizable(True, True)


def main():

    l1 = Label(window, text="")
    l1.grid(row=0, column=0, columnspan = 3)
    
    l2 = Label(window, text="시작 버튼을 누르세요.")
    l2.grid(row=1, column=0, columnspan = 3)
    
    l3 = Label(window, text="")
    l3.grid(row=2, column=0, columnspan = 3)
    
    l4 = Label(window, text="")
    l4.grid(row=3, column=0, columnspan = 3)
    
    l5 = Label(window, text="")
    l5.grid(row=4, column=0, columnspan = 3)
    
    e1 = Entry(window, width=40, state = DISABLED) 
    e1.grid(row=5, column=0, columnspan = 3)
    
    l6 = Label(window, text="")
    l6.grid(row=7, column=0, columnspan = 3)
    
    l7 = Label(window, text="alphabet used for prediction")
    l7.grid(row=8, column=0, columnspan=3)
    
    l8 = Label(window, text="")
    l8.grid(row=9, column=0, columnspan=3)
    
    l9 = Label(window, text="")
    l9.grid(row=10, column=0, columnspan=3)
    
    l10 = Label(window, text="")
    l10.grid(row=11, column=0, columnspan=3)
    
    ############################################################

    # 주로 사용하는 버튼 3개 초기화
    button_list = ['start/init', 'erase', 'predict']
    b1 = Button(window, text=button_list[0], height=2, width=7)
    b1.grid(row=6, column=0)
    
    b2 = Button(window, text=button_list[1], height=2, width=7, state=DISABLED) 
    
    b2.grid(row=6, column=1)
    b3 = Button(window, text=button_list[2], height=2, width=7, state=DISABLED) 
    b3.grid(row=6, column=2)

    
    ############################################################

    infile = open("words.txt" , "r", encoding='utf-8')
    lines = infile.readlines()

    def click1():
        global turns, word, total_try, guesses

        turns = 10
        total_try = 0
        guesses = set()
        
        word = random.choice(lines).rstrip()
        l2['text'] = f"predict word. {len(word)} strings"
        e1["state"] = NORMAL
        b2["state"] = NORMAL
        b3["state"] = NORMAL
        l3['text'] = ''.join(['_'+' ' for c in word])[:-1]
        l4['text'] = ""
        l9['text'] = ""
        
        click2()
        visualize_hangman(turns, reset=True)
        
    
    def click2():
        e1.delete(0, END)

    def process():

        global turns, total_try

        guess = e1.get()
        total_try += 1

        if len(guess) != 1:
            l1['text'] = ""
            l2['text'] = "fill in 1 string"
            click2()
            return

        l1['text'] = ""
        l2['text'] = ""
        l3['text'] = ""
        l4['text'] = ""
        
        failed = 0
        correct = 0
        
        if guess in guesses:
            l2['text'] = "input string beforehand"
            l3['text'] = "input again"
            for char in word:
                if char in guesses:
                    l4['text'] += " " + char
                else:
                    l4['text'] += " " + "_"
            click2()
            return

        guesses.add(guess)

        for char in word:
            if char in guesses:
                l4['text'] += " " + char
                correct += 1
            else:
                l4['text'] += " " + "_"
                failed += 1
        
        if failed == 0:
            l2['text'] = "===== User Victory ====="
            l3['text'] = f'Total tried {total_try} times!'
            b2["state"] = DISABLED
            b3["state"] = DISABLED
            e1["state"] = DISABLED
            visualize_hangman(victory=True)
            click2()
            return

        if correct > 0:
            l2['text'] = f"string correct!"
            l3['text'] = f'still has {turns} turns left!'
            click2()

        if guess not in word:
            turns -= 1
            visualize_hangman(turns)
            if turns == 0:
                l2['text'] = f"User failed ... Answer {word}"
                l3['text'] = "You are dead."
                l4['text'] = ""
                e1.delete(0, END)
                b2["state"] = DISABLED
                b3["state"] = DISABLED
                e1["state"] = DISABLED
            else:
                l2['text'] = f'Wrong {turns} turns left!'
                l3['text'] = f'Your wrong string input is {guess}'
            click2()
        
        l9['text'] = ""
        for char in guesses:
            l9['text'] += f"{char} " 

    b1['command'] = click1 
    b2['command'] = click2 
    b3['command'] = process 
    window.mainloop()
    infile.close()


if __name__ == '__main__':
    window = Tk()
    window_config(window)
    main()