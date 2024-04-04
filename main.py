#Імпортування переліку бібліотек для коректної роботи застосунку
import customtkinter
from PIL import Image
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from googletrans import Translator

#Власний клас що описує характеристики відео і виводить їх  на екран
class Video:
    def __init__(self, file_path):
        self.file_path= file_path
        self.clip = VideoFileClip(file_path)
        self.file_size=os.path.getsize(file_path)
        self.duration = self.clip.duration
        self.fps= self.clip.fps
        self.resolution = self.clip.size
        

    def display_info(self):
        print(f"Шлях: {self.file_path}")
        print(f"Розмір: {self.file_size} байт")
        print(f"Тривалість: {self.duration}")
        print(f"Кількість кадрів: {self.fps} к/сек")
        print(f"Розширення: {self.resolution}")


class App(customtkinter.CTk):
    #Основне вікно
    def __init__(self):
        super().__init__()

        # Функція для відкриття діалогового вікна вибору відео
        def open_file_dialog():
            global video_file_path

            video_file_path = customtkinter.filedialog.askopenfilename(filetypes=[("Відеофайли", "*.mp4 *.avi *.mov")])
            if video_file_path:
                self.video = Video(video_file_path)
                self.info_label.configure(text=f"""1.Інформація про відео:
Шлях: {video_file_path}
Розмір: {self.video.file_size} байт
Тривалість: {self.video.duration} сек
Кількість кадрів: {self.video.fps} к/сек
Розширення: {self.video.resolution}

2. Екстракція аудіо доріжки.
3. Оцифрування мовлення.
4. Переклад тексту.
5. Синтез мовлення.
6. Заміна мовлення.
7. Збереження, шлях:""",
                wraplength=640),
                self.start_button.configure(state="normal", text="Розпочати")
                print("Виконано відкриття відео")
            else:
                print("Вибір файлу скасовано.")


        #Функція для відділення аудіо від відео
        def audio_video_separator():
            video = VideoFileClip(video_file_path)
            audio=video.audio.write_audiofile("output.wav")
            print ("аудіофайл: ", audio)
            print("Виконано відділення аудіо та відео")


        #Функція для розпізнавання мовлення аудіо
        def STT_Engine():
            recognizer = sr.Recognizer()
            global audio_file_path 
            audio_file_path = "output.wav"

            try:
                with sr.AudioFile(audio_file_path) as file:
                    audio_file_path =recognizer.record(file)
                text = recognizer.recognize_google(audio_file_path)
                with open("output.txt", "w") as text_file:
                    text_file.write(text)
                print("Виконано оцифрування аудіо")

            except sr.UnknownValueError:
                print("Розпізнавач мовлення не може розпізнати аудіо")
            except sr.RequestError as e:
                print("Не вдалося отримати результати від служби розпізнавання мовлення Google; {0}".format(e))


        #Функція для перекладу розпізнаного тексту
        def Google_Translator():
            with open('output.txt', 'r+') as file:
                text = file.read().replace('\n', ' ')
                translator = Translator().translate(text, dest='uk')
                file.seek(0)
                file.truncate()
                file.write(translator.text)
                print("Виконано переклад тексту")


        #Функція для озвучування перекладеного тексту
        def TTS_Engine():
            from gtts import gTTS
            
            with open('output.txt', 'r') as file:
                text = file.read()
            
            tts = gTTS(text, lang='uk')
            tts.save("sample.mp3")
            print("Виконано озвучка")


        #функція для заміни старого аудіо на нове
        def SpeechReplace(video_file_path):
            video = VideoFileClip(video_file_path)
            audio = AudioFileClip("sample.mp3")

            new_video = video.set_audio(audio)
            print("Виконано заміна аудіо")
            return new_video


        #функція для збереження нового відео
        def save_file_dialog():
            new_video= SpeechReplace(video_file_path)
            file = customtkinter.filedialog.asksaveasfile(mode='wb', defaultextension=".mp4")
            if file:
                new_video.write_videofile(file.name)
                file.close()
                
                self.info_label.configure(text=f"""1.Інформація про відео:
Шлях: {video_file_path}
Розмір: {self.video.file_size} байт
Тривалість: {self.video.duration} сек
Кількість кадрів: {self.video.fps} к/сек
Розширення: {self.video.resolution}

2. Екстракція аудіо доріжки.
3. Оцифрування мовлення.
4. Переклад тексту.
5. Синтез мовлення.
6. Заміна мовлення.
7. Відео збережено успішно, шлях: {file.name}""",
                wraplength=640)
                
                print("відео збережено успішно!")
            else:
                print("збереження скасовано!")


        #Хендлер для функцій (викликається кнопкою "Розпочати")
        def handle_button_click():
            audio_video_separator()
            STT_Engine()
            Google_Translator()
            TTS_Engine()
            save_file_dialog()

            
        # Іконка для кнопки налаштувань
        self.settings_img = customtkinter.CTkImage(
            Image.open("settings.png"), size=(32, 32)
        )
        
        # іконка для кнопки "оглянути"
        self.oFD_button_img = customtkinter.CTkImage(
            Image.open("ofd_button.png"), size=(68, 60)
        )
        
        # іконка для кнопки "назад"
        self.back_button_img = customtkinter.CTkImage(
            Image.open("back_button.png"), size=(64, 64)
        )

        # іконка для кнопки "Зберегти"
        self.save_button_img = customtkinter.CTkImage(
            Image.open("save_button.png"), size=(52, 52)
        )

        # Великий логотип "Інформація про додаток"
        self.logotype = customtkinter.CTkImage(
            Image.open("logo.jpg"), size=(256, 256)
        )

        # Основне вікно
        self.title("VoiceUA")
        self.iconbitmap("logo.ico")
        self.geometry(f"{750}x{700}")
        self.maxsize(750, 700)
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")

        # Рамки
        self.info_frame = customtkinter.CTkFrame(
            self, width=700, height=515, corner_radius=30, fg_color="#212132"
        )
        self.info_frame.pack(padx=(25, 25), pady=25)

        self.action_frame = customtkinter.CTkFrame(
            self,
            width=700,
            height=110,
            corner_radius=30,
            fg_color="#212132",
        )
        self.action_frame.pack(padx=25)
        
        self.info_label = customtkinter.CTkLabel(
            self.info_frame,
            text=f"""1. Інформація про відео:
2. Екстракція аудіо доріжки.
3. Оцифрування мовлення.
4. Переклад тексту.
5. Синтез мовлення.
6. Заміна мовлення.
7. Збереження, шлях:""",
            text_color="#949494",
            font=("Roboto", 24, "bold"),
            anchor="nw",
            justify="left",
        )
        self.info_label.place(x=50, y=25)

        # Кнопки
        self.settings_button = customtkinter.CTkButton(
            self.action_frame,
            text="",
            fg_color="#D7D7D7",
            hover_color="#B4B4B4",
            width=0,
            height=80,
            corner_radius=30,
            image=self.settings_img,
            command=self.settings_button,
        )
        self.settings_button.grid(row=0, column=0, padx=(25, 0), pady=16)

        self.openFileDialog_button = customtkinter.CTkButton(
            self.action_frame,
            text="Оглянути ",
            text_color="#004D85",
            font=("Inter", 24, "bold", "italic"),
            fg_color="#FFCB65",
            hover_color="#CD8903",
            width=237,
            height=80,
            corner_radius=30,
            image=self.oFD_button_img,
            compound="right",
            command=open_file_dialog
        )
        self.openFileDialog_button.grid(row=0, column=2, padx=(25, 0), pady=16)

        self.start_button = customtkinter.CTkButton(
            self.action_frame,
            text="Оберіть відео",
            text_color="#004D85",
            font=("Inter", 24, "bold", "italic"),
            fg_color="#75AC4A",
            hover_color="#53BB02",
            width=237,
            height=80,
            corner_radius=30,
            anchor="center",  
            state="disabled",
            text_color_disabled="#004D85",
            command=handle_button_click
        )
        self.start_button.grid(row=0, column=3, padx=25, pady=16)

    #Вікно налаштувань
    def settings_button(self):
        self.settings_window = customtkinter.CTkToplevel()
        self.settings_window.title("Налаштування")
        # self.settings_window.iconbitmap("settings.png")
        self.settings_window.geometry(f"{750}x{700}")
        self.settings_window.maxsize(750, 700)
        self.withdraw()

        # Рамка для налаштувань
        self.setting_frame = customtkinter.CTkFrame(
            self.settings_window,
            height=540,
            width=700,
            corner_radius=30,
            fg_color="#212132",
        )
        self.setting_frame.pack(padx=(25, 25), pady=25)

        # Назва вікна "Налаштування"
        self.settings_label = customtkinter.CTkLabel(
            self.setting_frame,
            text="Налаштування",
            text_color="#E4E4E4",
            font=("Roboto", 26, "bold"),
            anchor="nw",
            justify="left",
        )
        self.settings_label.place(x=70, y=25)

        # Чекбокс "Зберегти тимчасові файли?"
        self.temp_checkbox = customtkinter.CTkCheckBox(
            self.setting_frame,
            text="Зберегти тимчасові файли?",
            text_color="#E4E4E4",
            font=("Roboto", 20, "bold"),
        )
        self.temp_checkbox.place(x=50, y=100)

        # Чекбокс "Зберегти переозвучене аудіо?"
        self.save_audio_checkbox = customtkinter.CTkCheckBox(
            self.setting_frame,
            text="Зберегти переозвучене аудіо?",
            text_color="#E4E4E4",
            font=("Roboto", 20, "bold"),
        )
        self.save_audio_checkbox.place(x=50, y=140)

        #Інформація про додаток з логотипом
        self.appinfo_label = customtkinter.CTkLabel(
            self.setting_frame,
            text="""  Інформація про додаток
  Він створений щоб побороти 
  мовні бар'єри, в цілях освіти 
  та  саморозвитку.
  Dev & UI/UX: Стецюра Олександр
  ВСП "ВіФК НУХТ" група 4ОК2
  ♥♥♥vcnuft.vn.ua♥♥♥""",
            text_color="#E4E4E4",
            font=("Roboto", 21, "bold"),
            image=self.logotype,
            anchor="nw",
            justify="left",
            compound="left",
            wraplength=370
        )
        self.appinfo_label.place(x=45, y=220)

        # Кнопка назад в головне вікно
        self.back_button = customtkinter.CTkButton(
            self.settings_window,
            text="Назад ",
            text_color="#004D85",
            font=("Inter", 24, "bold", "italic"),
            anchor="center",
            fg_color="#FFCB65",
            hover_color="#CD8903",
            height=80,
            width=237,
            corner_radius=30,
            image=self.back_button_img,
            compound="right",
            command=lambda: [self.settings_window.withdraw(), self.deiconify()],
        )
        self.back_button.pack(side="left", padx=50, pady=10)

        # Кнопка "Зберегти" налаштування
        self.save_button = customtkinter.CTkButton(
            self.settings_window,
            text="Зберегти",
            text_color="#004D85",
            font=("Inter", 24, "bold", "italic"),
            anchor="center",
            fg_color="#FFCB65",
            hover_color="#CD8903",
            height=80,
            width=237,
            corner_radius=30,
            image=self.save_button_img,
            compound="right",
        )
        self.save_button.pack(side="right", padx=50, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()