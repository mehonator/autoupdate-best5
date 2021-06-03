import pyautogui
import time
import subprocess
import psutil
import os
import smtplib
from email.mime.multipart import MIMEMultipart
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
import datetime

TIME_AFTER_START = 10
TIME_BETWEEN_MOVE = 3
TIME_BETWEEN_FAILLE = 5
PATH_PIC = ""


class EmailBot:
    def __init__(self):
        self.addr_from = "botAutoReport@yandex.ru"
        self.password = "updqvyohhlevessz"
        self.addr_to = "mehonator@yandex.ru"

    def send_email(self, subject_tex='Тема сообщения', text="текс сообщения", path_pic=""):
        try:
            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = self.addr_from
            msg['To'] = self.addr_to
            msg['Subject'] = subject_tex

            body = text
            # Добавляем в сообщение текст
            msg.attach(MIMEText(body, 'plain'))
            # Имя файла в абсолютном или относительном формате
            filepath = path_pic
            # Только имя файла
            filename = os.path.basename(filepath)

            # Если файл существует
            if os.path.isfile(filepath) and path_pic != "":
                # Определяем тип файла на основе его расширения
                ctype, encoding = mimetypes.guess_type(filepath)
                # Если тип файла не определяется
                if ctype is None or encoding is not None:
                    # Будем использовать общий тип
                    ctype = 'application/octet-stream'
                # Получаем тип и подтип
                maintype, subtype = ctype.split('/', 1)
                # Если текстовый файл
                if maintype == 'text':
                    # Открываем файл для чтения
                    with open(filepath) as fp:
                        # Используем тип MIMEText
                        file = MIMEText(fp.read(), _subtype=subtype)
                        # После использования файл обязательно нужно закрыть
                        fp.close()

                elif maintype == 'image':
                    # Если изображение
                    with open(filepath, 'rb') as fp:
                        file = MIMEImage(fp.read(), _subtype=subtype)
                        fp.close()

                elif maintype == 'audio':
                    # Если аудио
                    with open(filepath, 'rb') as fp:
                        file = MIMEAudio(fp.read(), _subtype=subtype)
                        fp.close()
                else:
                    # Неизвестный тип файла
                    with open(filepath, 'rb') as fp:
                        # Используем общий MIME-тип
                        file = MIMEBase(maintype, subtype)
                        # Добавляем содержимое общего типа (полезную нагрузку)
                        file.set_payload(fp.read())
                        fp.close()

                    # Содержимое должно кодироваться как Base64
                    encoders.encode_base64(file)

            # Добавляем заголовки
            file.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(file)

            # Создаем объект SMTP
            server = smtplib.SMTP("smtp.yandex.ru", 587)

            # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
            # server.set_debuglevel(True)

            # Начинаем шифрованный обмен по TLS
            server.starttls()

            # Получаем доступ
            server.login(self.addr_from, self.password)

            # Отправляем сообщение
            server.send_message(msg)

            # Выходим
            server.quit()
        except TypeError:
            print("ошибка отправки на почту")

    def send_email_screen(self, subject_text='Ошибка', text="текс сообщения"):
        now = datetime.datetime.now()
        name_rep_pic = f"{now.year}_{now.month}_{now.day}__{now.hour}_{now.minute}_{now.second}_{now.microsecond}.png"
        pyautogui.screenshot(name_rep_pic)
        self.send_email(subject_tex=subject_text, text=text, path_pic=name_rep_pic)
        os.remove(name_rep_pic)

    def send_error_msg(self, subject_text="Ошибка", msg="ошибка"):
        self.send_email(subject_tex=subject_text, text=msg)


class Clicker:
    def __init__(self, number_try=5):
        self.number_try = number_try

    def find_and_click(self, name_pic, chek_pic='', box_search=[0, 0, 1920, 1080]) -> bool:
        time.sleep(TIME_BETWEEN_MOVE)
        try:
            if chek_pic != '':
                box_search = pyautogui.locateOnScreen(PATH_PIC + chek_pic, region=box_search)

            x, y = pyautogui.locateCenterOnScreen((PATH_PIC + name_pic), region=box_search)
            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
            pyautogui.click()

            print(x, y)
            print(box_search)
            print(f"клик по{name_pic}")
            return True
        except:
            return False

    def find_click_sev_try(self, name_pic, chek_pic='', box_search=[0, 0, 1920, 1080],
                           time_between_faille=TIME_BETWEEN_FAILLE, number_try=None):
        counter_er = 0
        number_try = self.number_try if number_try else number_try
        for i in range(self.number_try):
            if self.find_and_click(name_pic, chek_pic, box_search=box_search):
                break

            print(f"попытка найти {i + 1} из {self.number_try} провалилась")
            counter_er += 1

            for k in range(time_between_faille):
                time.sleep(1)
                print(f"Ожидание {k} из {time_between_faille}")

            if counter_er == number_try:
                raise BaseException(f"Не найдено изображение {name_pic} в {chek_pic}")


class ClickerBEST5:
    def _enter_best5(self):
        self.find_click_sev_try("01вход_ок.png", chek_pic="00вход.png", number_try=15)
        self.find_click_sev_try("03вход_аптека_сиемма.png", chek_pic="02вход_выбор_пред.png")
        # без проверки тк проверили в прошлый раз
        self.find_click_sev_try("03вход_аптека_сиемма_ок.png")

    def _enter_main_menu(self):
        # нет чек пикчи, тк октружение сильно меняется
        # ловим исключение, тк кнопка мб нажата
        try:
            self.find_click_sev_try("04главное меню_ненаж.png")
        except TypeError:
            self.find_click_sev_try("04главное меню_наж.png")

    def _enter_officina_menu(self):
        self.find_click_sev_try("05отрас_реш.png", chek_pic="05отрас_реш.png")
        self.find_click_sev_try("06отрас_реш_апт2.png", chek_pic="06отрас_реш_апт.png")

    def _enter_electronii_prihod(self):
        # нет чек пикчи, тк октружение сильно меняется
        self.find_click_sev_try("07электронный приход.png")
        self.find_click_sev_try("08выполнить.png", chek_pic="08внимание_восстановление.png")

    def _start_indexation(self):
        # так как процесс длительный чекаем реже, но дольше
        self.find_click_sev_try("9индексациязав_ок.png", chek_pic="9индексациязав.png", number_try=30,
                                time_between_faille=120)

    def _choose_download_update(self):
        self.find_click_sev_try("10выбор загрузок галка.png", chek_pic="10выбор загрузок.png")

    def _accept_results(self):
        # так как процесс длительный чекаем реже, но дольше
        self.find_click_sev_try("11резульаты обнпеч_ок_ок.png", chek_pic="11резульаты обнпеч_ок.png",
                                number_try=30,
                                time_between_faille=120)

    def morning_start_best_and_update_base(self):
        self._enter_best5()
        self._enter_main_menu()
        self._enter_officina_menu()
        self._enter_electronii_prihod()
        self._start_indexation()
        self._choose_download_update()
        self._accept_results()


class Runner:
    def __init__(self, path_setting, messge_sender):
        self.path_setting = path_setting
        self.name_and_path_program = self._get_path_program()
        self.message_sender = messge_sender

    def _find_process_best5(self, name_process) -> bool:
        for proc in psutil.process_iter():
            name = proc.name()
            if name == name_process:
                return True
        return False

    def _find_process_best5_sev_try(self, name_proc, time_between_faille=TIME_BETWEEN_FAILLE) -> bool:
        number_try = 5
        for i in range(number_try):
            if self._find_process_best5(name_proc):
                return True
            else:
                print("попытка найти процесс", i + 1, "из", number_try, "провалилась")
                time.sleep(time_between_faille)
        return False

    def _get_path_program(self) -> str:
        print("Пытаюсь получить путь БЕСТ5 из файла настройки")
        try:
            file_handler = open(self.path_setting)
            name_and_path = file_handler.read()

            if name_and_path[0:3] == "п»ї":
                print("Найдена метка BOM в файле настроке, читаю без неё")
                name_and_path = name_and_path[3:]
            print(f"путь к BEST5 {name_and_path}")

        except IOError:
            error = "Ошибка ввода/вывода файла"
            self.message_sender.send_error_msg(subject_text=error, msg="нет файла настройки")
            print(error)
            input("можете закрыть это окно")

        finally:
            file_handler.close()
        return name_and_path

    def _is_run_program(self) -> bool:
        return self._find_process_best5_sev_try(os.path.basename(self.name_and_path_program))

    def _start_program(self):
        try:
            subprocess.Popen([self.name_and_path_program])
        except BaseException:
            text_msg = """не получилось запустить БЕСТ5
            проверьте корректности пути и кодировку
            требуемая кодировка - UTF8
            возможно, требуются права админа
            либо мешает UAC
            """
            print(text_msg)
            self.message_sender.send_email_screen(subject_text="Ошибка", text=text_msg)

    def run_program(self):
        if not self._is_run_program():
            self._start_program()


def main():
    try:
        email_bot = EmailBot()
        runner = Runner("pathOfBest5.txt", email_bot)
        runner.run_program()

        print("ждём ", TIME_AFTER_START, " секунд")
        time.sleep(TIME_AFTER_START)

        pyautogui.moveTo(50, 50, duration=TIME_BETWEEN_MOVE, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(1050, 50, duration=TIME_BETWEEN_MOVE, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(50, 50, duration=TIME_BETWEEN_MOVE, tween=pyautogui.easeInOutQuad)

        clicker_best5 = ClickerBEST5()
        try:
            clicker_best5.morning_start_best_and_update_base()
            print("Готово! Можно закрыть это окно")
            email_bot.send_email_screen(subject_text="успешный запуск!")
        except BaseException as error:
            print(f"Ошбика распознавания {error}")
            email_bot.send_email_screen(subject_text="Ошбика распознавания")
            input("Можно закрыть данное окно")

    except BaseException:
        error_msg = "что-то пошло не так"
        email_bot.send_error_msg(subject_text="Ошибка", msg=error_msg)
        email_bot.send_email_screen(subject_text=error_msg)
        input("Можно закрыть это окно")


if __name__ == "__main__":
    main()
