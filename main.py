from tkinter import *
from tkinter import messagebox
from tkmacosx import Button
from wonderwords import RandomSentence, RandomWord
import jellyfish
from timeit import default_timer as timer
from datetime import timedelta
import time

BLUE = '#4169E1'


def main():
    class Window():
        def __init__(self):
            #   Creating main root
            self.root = Tk()
            self.root.title('Typing Speed Test')
            self.root.rowconfigure(0, weight=1)
            self.root.columnconfigure(0, weight=1)
            self.root.geometry('750x600+100+100')

            # Useful Vars
            self.seconds = 0
            self.minutes = 0

            #   States
            self.game_on = None

            # game mode 1=classic mode, 0=endless mode
            self.game_mode = None
            self.start_game_button_state = 'disabled'
            self.classic_mode_start_game_button_state = 'disabled'
            self.text_box_state = 'disabled'

            self.TEAL = '#6CC4A1'
            self.GREEN = '#A0D995'
            self.BABY_BLUE = '#4CACBC'

            #   Button states
            self.easy_mode_button_state = 'active'
            self.medium_mode_button_state = 'active'
            self.hard_mode_button_state = 'active'

            # Game buttons
            self.start_typing_button_state = None

            #   Word generation
            self.words = None
            self.sentence = None

            #   Word Calculation
            self.user_typed = None
            self.accuracy = None
            self.correctly_typed = None
            self.errors = 0
            self.total_n_characters = 0

            self.r = RandomWord()
            #   Creating our pages and configure

            # ==================================== Select Game mode frame ====================================#
            self.game_mode_frame = Frame(self.root)

            #                                         Content of frame

            #   Exit Button
            self.exit_button = Button(self.game_mode_frame, text='Exit', command=self.Close, background=self.BABY_BLUE)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.game_mode_frame, text='Select Game Mode', font=('Helvetica', 24, 'bold'), background=self.GREEN, highlightthickness=1, highlightbackground='#F6E3C5')
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            #   Mode Selection buttons

            self.classic_mode_button = Button(self.game_mode_frame, highlightthickness=0, text='Classic Mode',
                                              command=lambda: self.classic_mode_selection(self.classic_mode_frame), background='#6CC4A1',
                                              )
            self.classic_mode_button.grid(row=1, column=1, padx=20, pady=20)

            self.endless_mode = Button(self.game_mode_frame, text='No Time limit Mode',
                                       command=lambda: self.endless_mode_selection(self.frame_home_2), background='#6CC4A1'
                                       )
            self.endless_mode.grid(row=2, column=1, padx=20, pady=20)


            # ==================================== No timelimit game mode frame  ====================================#
            #   Home Frame
            self.frame_home_2 = Frame(self.root)

            #   Buttons
            self.exit_button = Button(self.frame_home_2, text='Exit', command=self.Close, background=self.BABY_BLUE)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.frame_home_2, text='Typing Speed test', font=('Helvetica', 24, 'bold'))
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            #   Difficulty options
            self.easy_mode_button = Button(self.frame_home_2, text='Easy', padx=40,
                                           command=self.easy_mode_button_func, bg=self.TEAL, fg='white')
            # self.easy_mode_button.configure(bg='#228B22', fg='white')
            self.easy_mode_button.grid(row=1, column=1, padx=20, pady=20)

            self.medium_mode_button = Button(self.frame_home_2, text='Medium', padx=40,
                                             command=self.medium_mode_button_func, bg=self.TEAL, fg='white')
            # self.medium_mode_button.configure(bg='#228B22', fg='white')
            self.medium_mode_button.grid(row=2, column=1, padx=20, pady=20)

            self.hard_mode_button = Button(self.frame_home_2, text='Hard', padx=40,
                                           command=self.hard_mode_button_func, bg=self.TEAL, fg='white')
            # self.hard_mode_button.configure(bg='#228B22', fg='white')
            self.hard_mode_button.grid(row=3, column=1, padx=20, pady=20)

            #   Start Game button
            self.start_game_button = Button(self.frame_home_2, text='Start Typing', padx=60,
                                            state=self.start_game_button_state,
                                            command=lambda: self.show_frame(self.frame_main))

            self.start_game_button.grid(row=4, column=1, padx=20, pady=40)

            # ==================================== Classic mode frame ====================================#

            self.classic_mode_frame = Frame(self.root)

            #   Buttons
            self.exit_button = Button(self.classic_mode_frame, text='Exit', command=self.Close, background=self.BABY_BLUE)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.classic_mode_frame, text='Classic mode', font=('Helvetica', 24, 'bold'), background=self.GREEN)
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            # Classic mode time selections
            self.classic_mode_options = [
                '1 minute',
                '2 minute',
                '3 minute'
            ]
            self.time_dic = {
                '1 minute': 60,
                '2 minute': 120,
                '3 minute': 180
            }


            self.clicked = StringVar()
            self.clicked.set(self.classic_mode_options[0])

            self.classic_mode_drop_down = OptionMenu(self.classic_mode_frame, self.clicked,  *self.classic_mode_options, command=self.get_drop_down_selection)
            self.classic_mode_drop_down.grid(row=1, column=1, padx=20, pady=20, )

            #   Start Game button
            self.classic_mode_start_game_button = Button(self.classic_mode_frame, text='Start Typing', padx=60,
                                                         state=self.classic_mode_start_game_button_state,
                                                        command=lambda: self.show_frame(self.frame_main))

            self.classic_mode_start_game_button.grid(row=2, column=1, padx=20, pady=40)

            # ==================================== Classic mode main frame ====================================#






            # ==================================== page 2 ====================================#
            # Main Frame
            self.frame_main = Frame(self.root, background='white')

            #   Main Game Buttons
            self.exit_button = Button(self.frame_main, text='Exit', command=self.Close, background=self.BABY_BLUE)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)


            #======================= Clock Version 2===========================#

            self.countdown_times = {
                '1 minute': '01',
                '2 minute': '02',
                '3 minute': '03',
                '4 minute': '04',
                '5 minute': '05',
            }

            #   Declare Clock v2 vars
            self.hour_string = StringVar()
            self.minute_string = StringVar()
            self.second_string = StringVar()

            #   Set Default values
            self.hour_string.set('00')
            self.minute_string.set('00')
            self.second_string.set('00')

            self.clock_frame = Frame(self.frame_main)
            self.clock_frame.grid(row=1, column=1)

            #   Initialize Clock v2
            self.hour_Textbox = Label(self.clock_frame, width=3, height=1, font=("Calibri", 24, "bold"), fg='black',
                                      bg=self.GREEN, textvariable=self.hour_string)
            self.minute_Textbox = Label(self.clock_frame, width=3, height=1, font=("Calibri", 24, "bold"),
                                        fg='black', bg=self.GREEN, textvariable=self.minute_string)
            self.second_Textbox = Label(self.clock_frame, width=3, height=1, font=("Calibri", 24, "bold"),
                                        fg='black', bg=self.GREEN, textvariable=self.second_string)
            #   Clock V2 display
            self.hour_Textbox.grid(row=0, column=0)
            self.minute_Textbox.grid(row=0, column=1)
            self.second_Textbox.grid(row=0, column=2)



            #   Word Box
            self.word_box_border = Frame(self.frame_main, width=60, height=20, highlightbackground=self.GREEN,
                                         highlightthickness=2)
            self.word_box_border.grid(row=2, column=1, pady=5)

            self.word_box_label = Label(self.word_box_border, text='', bd=0, font=('open sans', 16, 'normal' ))
            self.word_box_label.pack()

            # Text Box
            self.text_box = Text(self.frame_main, width=60, height=5, bd=1, state=self.text_box_state)
            self.text_box.grid(row=3, column=1, pady=5)

            #   Buttons
            self.start_typing_button = Button(self.frame_main, text='Start', command=self.start_Game, padx=20, background=self.TEAL)
            self.start_typing_button.grid(row=4, column=1, pady=(10, 5))

            self.reset_button = Button(self.frame_main, text='Reset', command=self.reset_Game, padx=20, background=self.TEAL)
            self.reset_button.grid(row=5, column=1, pady=5)

            self.home_button = Button(self.frame_main, text='Home',
                                      command=lambda: self.back_Home(self.game_mode_frame),
                                      padx=24, background=self.TEAL)
            self.home_button.grid(row=6, column=1, pady=5)

            # ===================================== page 3 ====================================#
            self.frame_score_menu = Frame(self.root, background='white')

            #   Score Menu Game Buttons
            self.exit_button = Button(self.frame_score_menu, text='Exit', command=self.Close, background=self.BABY_BLUE)
            self.exit_button.grid(row=0, column=0, padx=20, pady=30)

            #   Title label
            self.title_label = Label(self.frame_score_menu, text='Typing Speed test\n Thank you playing',
                                     font=('Helvetica', 24, 'bold'), background=self.GREEN)
            self.title_label.grid(row=0, column=1, padx=120, pady=30)

            # Speed Wpm Label
            self.wpm_output_label = Label(self.frame_score_menu, text=f'', borderwidth=0, relief='solid', background=self.TEAL)
            self.wpm_output_label.grid(row=1, column=1, pady=5)

            # Accuracy Label
            self.accuracy_output_label = Label(self.frame_score_menu, text=f'Accuracy\n ##(%)', borderwidth=0,
                                               relief='solid', background=self.TEAL)
            self.accuracy_output_label.grid(row=2, column=1, pady=5)

            # Speed Wpm Label
            self.missed_words_label = Label(self.frame_score_menu, text=f'Missed\n ##', borderwidth=0, relief='solid', background=self.TEAL)
            self.missed_words_label.grid(row=3, column=1, pady=5)

            #   Play again button
            self.home_button = Button(self.frame_score_menu, text='Play Again',
                                      command=lambda: self.back_Home(self.game_mode_frame),
                                      padx=24, background=self.BABY_BLUE)
            self.home_button.grid(row=4, column=1, pady=5)

            #    =======================   Show frames to screen   =====================================    #

            #   Position Frames
            self.position_frames(self.frame_main, self.game_mode_frame, self.frame_home_2, self.classic_mode_frame, self.frame_score_menu)

            #   Show Frame HOME FRAME
            self.show_frame(self.game_mode_frame)

            #   TKINTER Main loop
            self.root.mainloop()

            #   Easy words

        # ============= Mode selection ==================#
        def classic_mode_selection(self, frame):
            self.game_mode = 0
            print(self.game_mode)
            self.show_frame(frame)

        def endless_mode_selection(self, frame):
            self.game_mode = 1
            print(self.game_mode)
            self.show_frame(frame)

        #   Classic Mode Funcs
        def get_drop_down_selection(self, event):
            '''
            Select a time frame for game to take place within
            sets our texts and words
            activate the start game button

            :param event:
            :return:
            '''
            self.mode_selection = self.clicked.get()
            print(self.mode_selection)
            # time = self.time_dic[self.mode_selection]
            # print(time)

            # Add Words and sentences to label
            if self.sentence is None and self.words is None:

                self.generate_sentence(10)
                self.add_words_to_label()

            #Enable start button that will take us to the main frame
            self.classic_mode_start_game_button_state = 'active'
            self.classic_mode_start_game_button.config(state=self.classic_mode_start_game_button_state)

        # ============= Difficulty Modes buttons  ==================#
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
                self.easy_mode_button.config(bg=self.TEAL, fg='white', borderless=0)
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
                self.add_words_to_label()
                #   Change button Apperance
                self.medium_mode_button.config(bg=self.TEAL, fg='white', borderless=0)
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
                self.add_words_to_label()
                #   Change button Apperance
                self.hard_mode_button.config(bg=self.TEAL, fg='white', borderless=0)
                # modes
                self.medium_mode_button_state = 'disabled'
                self.medium_mode_button.config(state=self.medium_mode_button_state)
                self.easy_mode_button_state = 'disabled'
                self.easy_mode_button.config(state=self.easy_mode_button_state)

                #   Activate start
                self.start_game_button_state = 'active'
                self.start_game_button.config(state=self.start_game_button_state)

        # ============= Words Configuration ========================#
        def add_words_to_label(self):
            self.word_box_label.config(text=self.sentence)

        def get_users_typed(self):
            raw_typed_words = self.text_box.get(1.0, END).split()
            print(raw_typed_words)

        def generate_sentence(self, lines):
            self.words = []
            for n in range(lines):
                self.words += [self.r.word() for w in range(8)]
                self.words.append('\n')
            self.sentence = ' '.join(self.words)
            print(self.sentence, self.words)

        # ============= Typing speed Calculations ==================#
        def typed_execution_calculation(self):
            self.results = timedelta(seconds=self.end - self.start).seconds
            self.raw_minutes = self.results / 60
            print(f'it took you: {self.results} seconds')
            self.minutes = round(self.raw_minutes, 2)
            print(f'it took you: {self.minutes} minutes')

        def classic_typed_execution_calculation(self):
            self.raw_minutes = int(self.time)
            print(f'it took you: {int(self.time) * 60} seconds')
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

        # ============= Navigation buttons ==================#

        def Close(self):
            """
            Closes the root window
            :return:
            """
            self.root.quit()

        def back_Home(self, frame):
            """
            Raise the home page frame mode
            reset the game

            """

            self.reset_Game()

            #   start typing reset
            self.start_game_button_state = 'disabled'
            self.start_game_button.config(state=self.start_game_button_state)

            # reset sentences and words
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

            if self.game_mode == 1:
                print('endless mode')
                self.start_typing_button_state = 'disabled'
                self.start_typing_button.configure(state=self.start_typing_button_state)

                self.get_clock_time()
                self.run_timer_2()
                self.start = timer()
                self.text_box.bind("<Return>", self.return_typed_text)
            else:
                print('classic game mode')
                self.start_typing_button_state = 'disabled'
                self.start_typing_button.configure(state=self.start_typing_button_state)

                self.get_clock_time()
                print('???????debug end of timer ??????')
                self.run_timer()




        def calculate_classic(self):
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
            self.classic_typed_execution_calculation()

            # Gross WPM
            self.gross_wpm_calculation()

            # Net words per minute
            self.errors_per_minute_calculation()

            # Net typing speed (gross words per minute/ errors per minute)
            self.net_words_per_minute_calculation()

            # Add  calculations to labels
            self.update_labels()

            self.show_frame(self.frame_score_menu)

        def calculate(self):
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

        def return_typed_text(self, event):
            """
            bind return key
            capture uses typed text
            :param frame:
            :return:
            """
            # returning text
            self.data = self.text_box.get(1.0, END).lower()
            self.raw_typed_words = self.data.split()

            self.end = timer()
            self.calculate()

            #   calculations

        def classic_mode_return_typed_text(self):
            self.data = self.text_box.get(1.0, END).lower()
            self.raw_typed_words = self.data.split()


        def reset_Game(self):
            """
            Resets timer
            clear the text box
            resets random text
            resets all wpm and accuracy calculations
            resets all current game states
            Reactivate start button
            :return:
            """
            self.game_on = False
            self.reset_timer()
            self.clear_text_box()

            self.start_typing_button_state = 'active'
            self.start_typing_button.configure(state=self.start_typing_button_state, background=self.TEAL)



        #============= timer =================================#
        def get_clock_time(self):
            if self.game_on:
                if self.game_mode == 0:
                    self.time = self.countdown_times[self.mode_selection]
                    print('debug time - minutes', int(self.time))
                    print('debug time - seconds', int(self.time) * 60)

                    # Set our countdown timers to a default value user selected
                    self.minute_string.set(self.time)
                    #   Begin count down process
                try:
                    self.clockTime = int(self.hour_string.get()) * 3600 + int(self.minute_string.get()) * 60 + int(
                        self.second_string.get())
                except:
                    print("Incorrect values")
                print('clock time', self.clockTime)



        def run_timer(self):

            if self.game_on:
                if (self.clockTime > -1):

                    self.clockTime -= 1

                    totalMinutes, totalSeconds = divmod(self.clockTime, 60)

                    totalHours = 0
                    if (totalMinutes > 60):
                        totalHours, totalMinutes = divmod(totalMinutes, 60)

                    #   set value
                    self.hour_string.set("{0:2d}".format(totalHours))
                    self.minute_string.set("{0:2d}".format(totalMinutes))
                    self.second_string.set("{0:2d}".format(totalSeconds))

                    #   configure display
                    self.hour_Textbox.config(textvariable=self.hour_string)
                    self.minute_Textbox.config(textvariable=self.minute_string)
                    self.second_Textbox.config(textvariable=self.second_string)
                    print('debug boxes configured')
                    self.clock_frame.after(1000, self.run_timer)



                    #   Update window interface
                    # self.clock_frame.update()
                    # time.sleep(1)


                    ### Let the user know if the timer has expired
                    if (self.clockTime == 0):
                        # reset the timer default values
                        self.hour_string.set('00')
                        self.minute_string.set('00')
                        self.second_string.set('00')
                        #calcutlatin
                        self.classic_mode_return_typed_text()
                        self.calculate_classic()

        def run_timer_2(self):
            if self.game_on:
                if (self.clockTime > -1):

                    self.clockTime += 1

                    totalMinutes, totalSeconds = divmod(self.clockTime, 60)

                    totalHours = 0
                    if (totalMinutes > 60):
                        totalHours, totalMinutes = divmod(totalMinutes, 60)

                    #   set value
                    self.hour_string.set("{0:2d}".format(totalHours))
                    self.minute_string.set("{0:2d}".format(totalMinutes))
                    self.second_string.set("{0:2d}".format(totalSeconds))

                    #   configure display
                    self.hour_Textbox.config(textvariable=self.hour_string)
                    self.minute_Textbox.config(textvariable=self.minute_string)
                    self.second_Textbox.config(textvariable=self.second_string)
                    # print('debug boxes configured')
                    self.clock_frame.after(1000, self.run_timer_2)



        def classic_game_mode_timer(self):

            self.time = self.countdown_times[self.mode_selection]
            print('time', self.time)
            if self.game_on and self.seconds < self.time:
                print(self.seconds)
                #   Increment clock by one
                self.seconds += 1
                #   Configure clock display
                self.clock.config(text='00:' + str(self.seconds))

                #   Clock display
                if self.seconds > 0 and self.seconds < 10:
                    self.clock.config(text='00:0' + str(self.seconds))
                    self.clock.after(1000, self.classic_game_mode_timer)
                elif self.seconds > 10 and self.seconds < 60:
                    self.clock.config(text='00:' + str(self.seconds))
                    self.clock.after(1000, self.classic_game_mode_timer)
                elif self.seconds > 60:
                    self.clock.config(text='01:0')

                elif self.seconds == 0:
                    self.clock.config(text='Done')
                else:
                    self.clock.after(1000, self.classic_game_mode_timer)
            else:
                print('time reached', self.time)
                self.reset_timer()
                self.classic_mode_return_typed_text()
                self.calculate_classic()



        def reset_timer(self):
            self.seconds = 0
            # reset timer to defualt
            self.hour_string.set('00')
            self.minute_string.set('00')
            self.second_string.set('00')
            # configure timer to default
            self.hour_Textbox.config(textvariable=self.hour_string)
            self.minute_Textbox.config(textvariable=self.minute_string)
            self.second_Textbox.config(textvariable=self.second_string)
            # self.clock.config(text='00:0' + str(self.seconds))

        def clear_text_box(self):
            """
            Clears all text wihtin textbox
            :return:
            """
            self.text_box.delete(1.0, END)

        # ============= Screen configuration ==================#
        def position_frames(self, f1, f2, f3, f4, f5):
            for frame in (f1, f2, f3, f4, f5):
                frame.grid(row=0, column=0, sticky='nsew')

        def show_frame(self, frame):
            frame.tkraise()


    test = Window()


if __name__ == '__main__':
    main()
