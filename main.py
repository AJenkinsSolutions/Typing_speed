from tkinter import *
from tkinter import ttk
from tkmacosx import Button
from wonderwords import RandomSentence, RandomWord
import jellyfish
from timeit import default_timer as timer
from datetime import timedelta

BLUE = '#4169E1'


def main():
    class Window():
        def __init__(self):
            #   Creating main root
            self.root = Tk()
            self.root.title('Root Window')
            self.root.rowconfigure(0, weight=1)
            self.root.columnconfigure(0, weight=1)
            self.root.geometry('700x400+100+100')

            # Useful Vars
            self.seconds = 0
            self.minutes = 0

            #   States
            self.game_on = None
            self.start_game_button_state = 'disabled'
            self.text_box_state = 'disabled'
            #   Button states
            self.easy_mode_button_state = 'active'
            self.medium_mode_button_state = 'active'
            self.hard_mode_button_state = 'active'

            #   Word generation
            self.words = None
            self.sentence = None

            self.user_typed = None
            self.accuracy = None
            self.correctly_typed = None
            self.errors = 0
            self.total_n_characters = 0

            self.r = RandomWord()
            #   Creating our pages and configure

            # ==================================== page 1 ====================================#
            #   Home Frame
            self.frame_home = Frame(self.root, background='white')

            #   Buttons
            self.exit_button = Button(self.frame_home, text='Exit', command=self.Close)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.frame_home, text='Typing Speed test', font=('Helvetica', 24, 'bold'))
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            #   Difficulty options
            self.easy_mode_button = Button(self.frame_home, text='Easy', padx=40,
                                           command=self.easy_mode_button_func, bg='#228B22', fg='white')
            # self.easy_mode_button.configure(bg='#228B22', fg='white')
            self.easy_mode_button.grid(row=1, column=1, padx=20, pady=20)

            self.medium_mode_button = Button(self.frame_home, text='Medium', padx=30,
                                             command=self.medium_mode_button_func, bg='#228B22', fg='white')
            # self.medium_mode_button.configure(bg='#228B22', fg='white')
            self.medium_mode_button.grid(row=2, column=1, padx=20, pady=20)

            self.hard_mode_button = Button(self.frame_home, text='Hard', padx=40,
                                           command=self.hard_mode_button_func, bg='#228B22', fg='white')
            # self.hard_mode_button.configure(bg='#228B22', fg='white')
            self.hard_mode_button.grid(row=3, column=1, padx=20, pady=20)

            #   Start Game button
            self.start_game_button = Button(self.frame_home, text='Start Typing', padx=60,
                                            state=self.start_game_button_state,
                                            command=lambda: self.show_frame(self.frame_main))

            self.start_game_button.grid(row=4, column=1, padx=20, pady=40)

            # ==================================== page 2 ====================================#
            # Main Frame
            self.frame_main = Frame(self.root, background='white')

            #   Main Game Buttons
            self.exit_button = Button(self.frame_main, text='Exit', command=self.Close)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   clock
            self.clock = Label(self.frame_main, text='00:00', padx=20, font=("helvetica", 48), fg='black', bg='grey')
            self.clock.grid(row=0, column=1, padx=150, pady=30)

            #   Word Box
            self.word_box_border = Frame(self.frame_main, width=60, height=20, highlightbackground="blue",
                                         highlightthickness=2)
            self.word_box_border.grid(row=1, column=1, pady=5)

            self.word_box_label = Label(self.word_box_border, text='', bd=0)
            self.word_box_label.pack()

            # Text Box
            self.text_box = Text(self.frame_main, width=60, height=5, bd=1, state=self.text_box_state)
            self.text_box.grid(row=2, column=1, pady=5)

            #   Buttons
            self.start_typing_button = Button(self.frame_main, text='Start', command=self.start_Game, padx=20)
            self.start_typing_button.grid(row=3, column=1, pady=(10, 5))

            self.reset_button = Button(self.frame_main, text='Reset', command=self.reset_Game, padx=20)
            self.reset_button.grid(row=4, column=1, pady=5)

            self.home_button = Button(self.frame_main, text='Home',
                                      command=lambda: self.back_Home(self.frame_home),
                                      padx=24)
            self.home_button.grid(row=5, column=1, pady=5)

            # ===================================== page 3 ====================================#
            self.frame_score_menu = Frame(self.root, background='white')

            #   Score Menu Game Buttons
            self.exit_button = Button(self.frame_score_menu, text='Exit', command=self.Close)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.frame_score_menu, text='Typing Speed test\n Thank you playing',
                                     font=('Helvetica', 24, 'bold'))
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            # Speed Wpm Label
            self.wpm_output_label = Label(self.frame_score_menu, text=f'', borderwidth=1, relief='solid')
            self.wpm_output_label.grid(row=1, column=1, pady=5)

            # Accuracy Label
            self.accuracy_output_label = Label(self.frame_score_menu, text=f'Accuracy\n ##(%)', borderwidth=1,
                                               relief='solid')
            self.accuracy_output_label.grid(row=2, column=1, pady=5)

            # Speed Wpm Label
            self.missed_words_label = Label(self.frame_score_menu, text=f'Missed\n ##', borderwidth=1, relief='solid')
            self.missed_words_label.grid(row=3, column=1, pady=5)

            #   Play again button
            self.home_button = Button(self.frame_score_menu, text='Play Again',
                                      command=lambda: self.back_Home(self.frame_home),
                                      padx=24)
            self.home_button.grid(row=4, column=1, pady=5)

            #   Position Frames
            self.position_frames(self.frame_main, self.frame_home, self.frame_score_menu)
            #   Show Frame on screen
            self.show_frame(self.frame_home)

            #   TKINTER Main loop
            self.root.mainloop()

            #   Easy words

        def generate_sentence(self, lines):
            self.words = []
            for n in range(lines):
                self.words += [self.r.word() for w in range(8)]
                self.words.append('\n')
            self.sentence = ' '.join(self.words)
            print(self.sentence, self.words)

        def easy_mode_button_func(self):
            """
            easy mode pressed
            generate our text
            activate the start game button
            deactivate the other modes
            change the bg color or button
            :return:
            """
            # Generate texts
            if self.sentence is None and self.words is None:
                self.generate_sentence(3)
                self.add_words_to_label()
                #   Change button Appearance
                self.easy_mode_button.config(bg='#006400', fg='white', borderless=0)
                # Clean up other modes states
                self.medium_mode_button_state = 'disabled'
                self.medium_mode_button.config(state=self.medium_mode_button_state)
                self.hard_mode_button_state = 'disabled'
                self.hard_mode_button.config(state=self.hard_mode_button_state)

                #   Activate start button
                self.start_game_button_state = 'active'
                self.start_game_button.config(state=self.start_game_button_state)

            # #clean up so no more text is generated
            # self.easy_mode_button_state = 'disabled'
            # self.easy_mode_button.config(state=self.easy_mode_button_state)

        def medium_mode_button_func(self):
            if self.sentence is None and self.words is None:
                # Generate texts
                self.generate_sentence(5)
                #   Change button Apperance
                self.medium_mode_button.config(bg='#006400', fg='white', borderless=0)
                # modes
                self.easy_mode_button_state = 'disabled'
                self.easy_mode_button.config(state=self.easy_mode_button_state)
                self.hard_mode_button_state = 'disabled'
                self.hard_mode_button.config(state=self.hard_mode_button_state)

                #   Activate start
                self.start_game_button_state = 'active'
                self.start_game_button.config(state=self.start_game_button_state)

        def hard_mode_button_func(self):
            if self.sentence is None and self.words is None:
                # Generate texts
                self.generate_sentence(8)
                #   Change button Apperance
                self.hard_mode_button.config(bg='#006400', fg='white', borderless=0)
                # modes
                self.medium_mode_button_state = 'disabled'
                self.medium_mode_button.config(state=self.medium_mode_button_state)
                self.easy_mode_button_state = 'disabled'
                self.easy_mode_button.config(state=self.easy_mode_button_state)

                #   Activate start
                self.start_game_button_state = 'active'
                self.start_game_button.config(state=self.start_game_button_state)

        def add_words_to_label(self):
            self.word_box_label.config(text=self.sentence)

        def get_users_typed(self):
            raw_typed_words = self.text_box.get(1.0, END).split()
            print(raw_typed_words)

        def return_typed_text(self, event):
            """
            bind return key
            capture uses typed text
            :param frame:
            :return:
            """

            data = self.text_box.get(1.0, END).lower()
            self.raw_typed_words = data.split()
            self.end = timer()

            # Removes line breaks from the list we wanna check
            for i, v in enumerate(self.words):
                if v == '\n':
                    self.words.pop(i)

            # get the length of both list
            len_user_typed = len(self.raw_typed_words)
            # Create new word list to check for errors
            self.words = self.words[:len_user_typed]

            #   Error rate func
            self.error_rate_calculations()

            #   Correctly Typed
            self.calculate_correctly_typed()

            #   Calculate Accuracy
            self.calculate_accuracy()


            #   wpm calculations
            self.typed_execution_calculation()


            # Gross WPM
            self.gross_wpm_calculation()

            # Net words per minute
            self.errors_per_minute_calculation()


            # Net typing speed (gross words per minute/ errors per minute)
            self.net_words_per_minute_calculation()

            # Add  calculations to labels
            self.update_labels()

            self.show_frame(self.frame_score_menu)

        def typed_execution_calculation(self):
            self.results = timedelta(seconds=self.end - self.start).seconds
            self.raw_minutes = self.results / 60
            print(f'it took you: {self.results} seconds')
            self.minutes = round(self.raw_minutes, 2)
            print(f'it took you: {self.minutes} minutes')

        def gross_wpm_calculation(self):
            # all typed entires divided by 5 divded by minutes
            letter_count = 0
            for word in self.raw_typed_words:
                for c in word:
                    letter_count += 1
            print('letter count', letter_count)

            self.gross_words_per_minute = round((letter_count / 5) / self.minutes, 1)
            print(f'your gross words per minute {self.gross_words_per_minute}')

        def errors_per_minute_calculation(self):
            self.errors_per_minute = (self.errors / self.minutes)

        def net_words_per_minute_calculation(self):
            self.net_words_per_minute = round((self.gross_words_per_minute - self.errors_per_minute), 2)
            print(f'Your net words per minute: {self.net_words_per_minute}')

        def error_rate_calculations(self):
            # error rate calculations
            for i in range(len(self.words)):
                self.errors += jellyfish.damerau_levenshtein_distance(self.words[i], self.raw_typed_words[i])
                self.total_n_characters += len(self.words[i])
            # print('total_chars', self.total_n_characters)
            # print('errors', self.errors)

        def calculate_correctly_typed(self):
            self.correctly_typed = self.total_n_characters - self.errors
            print('number of correctly typed', self.correctly_typed)

        def calculate_accuracy(self):
            self.accuracy = round(self.correctly_typed / self.total_n_characters * 100)
            print(f'Accuracy: {self.accuracy}%')

        def update_labels(self):
            self.wpm_output_label.config(text=f'Speed\n{self.net_words_per_minute}(WPM)')
            self.accuracy_output_label.config(text=f'Accuray\n{self.accuracy}%')
            self.missed_words_label.config(text=f'Errors:\n{self.errors}')

        def Close(self):
            """
            Closes the root window
            :return:
            """
            self.root.quit()

        def back_Home(self, frame):
            """
            Raise the home page frame
            reset the game

            """

            self.reset_Game()

            #   start typing reset
            self.start_game_button_state = 'disabled'
            self.start_game_button.config(state=self.start_game_button_state)

            # reset sentecnes and words
            self.sentence = None
            self.words = None


            # Turn all button states back on
            self.easy_mode_button_state = 'active'
            self.medium_mode_button_state = 'active'
            self.hard_mode_button_state = 'active'
            self.easy_mode_button.config(state=self.easy_mode_button_state, bg='#228B22', fg='white')
            self.medium_mode_button.config(state=self.medium_mode_button_state, bg='#228B22', fg='white')
            self.hard_mode_button.config(state=self.hard_mode_button_state, bg='#228B22', fg='white')

            frame.tkraise()



        def start_Game(self):
            """
            1: Start button in frame main
            will focus the users on the text box
            2: Start timer
            :return:
            """
            # Adjust games state
            self.game_on = True
            #   Configure text box
            self.text_box_state = 'normal'
            self.text_box.config(state=self.text_box_state)
            self.text_box.focus_set()
            self.timer()
            self.start = timer()
            self.text_box.bind("<Return>", self.return_typed_text)

        def reset_Game(self):
            """
            Resets timer
            clear the text box
            resets random text
            resets all wpm and accuracy calculations
            resets all current game states
            :return:
            """
            self.game_on = False
            self.reset_timer()
            self.clear_text_box()

        def timer(self):
            if self.game_on:
                #   Increment clock by one
                self.seconds += 1
                #   Configure clock display
                self.clock.config(text='00:' + str(self.seconds))
                #   Clock display
                if 10 > self.seconds > 0:
                    self.clock.config(text='00:0' + str(self.seconds))
                    self.clock.after(1000, self.timer)
                elif self.seconds == 0:
                    self.clock.config(text='Done')
                else:
                    self.clock.after(1000, self.timer)
            else:
                self.reset_timer()

        def reset_timer(self):
            self.seconds = 0
            self.clock.config(text='00:0' + str(self.seconds))

        def clear_text_box(self):
            """
            Clears all text wihtin textbox
            :return:
            """
            self.text_box.delete(1.0, END)

        def position_frames(self, f1, f2, f3):
            for frame in (f1, f2, f3):
                frame.grid(row=0, column=0, sticky='nsew')

        def show_frame(self, frame):
            frame.tkraise()

    # s = RandomSentence()
    # d = s.sentence()
    # print(d)
    # for i in range(4):
    #     print(s.sentence())

    # #   Easy words
    # def generate_sentence(lines):
    #     words = []
    #     for i in range(lines):
    #         words += [r.word(word_min_length=2, word_max_length=5) for i in range(8)]
    #         words.append('\n')
    #     sentence = ' '.join(words)
    #     return sentence, words

    # sentence, raw_words = generate_sentence(3)
    # print(raw_words)
    # print(sentence)

    # checking for line breaks
    # then removing them
    # for i, v in enumerate(raw_words):
    #     if v == '\n':
    #         raw_words.pop(i)
    #     else:
    #         print(v)
    # print(raw_words)
    test = Window()


if __name__ == '__main__':
    main()
