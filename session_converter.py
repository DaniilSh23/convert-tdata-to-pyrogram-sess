import asyncio
import datetime
import os
import shutil

from opentele.api import UseCurrentSession
from opentele.td import TDesktop


class SessionConverter:
    """
    Конвертер сессий Telegram.
    В одной папке с файлом этого конвертера должен лежать файл-шаблон сессии pyrogram (blank_pyro.session)
    """
    def __init__(self, source_dir: str, dest_dir: str):
        """
        Конструктор класса, принимает первый путь - папку, в которой лежат архивы с tdata и второй путь - папку,
        куда сложить файлы сессий парами pyrogram и telethon.
        :param source_dir: str - папка, где лежат архивы с tdata
        :param dest_dir: str - папка, куда сложить файлы сессий
        """
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.blank_pyro_session = os.path.join(self.current_dir, 'blank_pyro.session')

    def convert_tdata_to_pyro_and_tl(self):
        """
        Метод для конвертации tdata в файлы сессий telethon и pyrogram
        """
        for tdata_dir in os.listdir(path=self.source_dir):
            # TODO: прописать метод, который будет распаковывать архив с папкой tdata
            # Конвертируем tdata в сессию telethon
            tl_usr_id = asyncio.run(self.convert_tdata_to_tl_sess(tdata_dir_name=tdata_dir))

            # Копируем шаблон файла сессии pyrogram для его наполнения
            tl_session_path = os.path.join(self.current_dir, f'tl_{tdata_dir}.session')
            pyro_session_path = os.path.join(self.current_dir, f'pyro_{tdata_dir}.session')
            shutil.copy(src=os.path.join(self.current_dir, 'blank_pyro.session'), dst=pyro_session_path)

            # Трансфер SQL инфы файлов сессий между собой
            self.sqlite_data_transfer(tl_sess_path=tl_session_path, pyro_sess_path=pyro_session_path, tl_usr_id=tl_usr_id)

            # Проверяем работу сессии pyrogram
            check_pyro_sess_rslt = asyncio.run(self.check_by_pyro(sess_name=f'pyro_{tdata_dir}'))
            if check_pyro_sess_rslt:
                # Перемещаем файлы сессии в отдельную папку
                shutil.move(src=pyro_session_path, dst=self.dest_dir)
                shutil.move(src=tl_session_path, dst=self.dest_dir)
            else:
                # Удаляем созданные файлы сессий
                os.remove(path=pyro_session_path)
                os.remove(path=tl_session_path)

    async def convert_tdata_to_tl_sess(self, tdata_dir_name):
        """
        Функция, которая конвертирует tdata в сесиию telethon
        """
        tdata_folder = os.path.join(self.source_dir, tdata_dir_name, 'tdata')
        tdesk = TDesktop(tdata_folder)

        # Check if we have loaded any accounts
        assert tdesk.isLoaded()

        # flag=UseCurrentSession
        #
        # Convert TDesktop to Telethon using the current session.
        client = await tdesk.ToTelethon(session=f"tl_{tdata_dir_name}.session", flag=UseCurrentSession)

        await client.connect()
        await client.PrintSessions()
        tl_getme_rslt = await client.get_me()
        print(f'Результат конвертации в сессию telethon. Метод get_me: {tl_getme_rslt}')
        return tl_getme_rslt.id

    @staticmethod
    def sqlite_data_transfer(tl_sess_path, pyro_sess_path, tl_usr_id):
        """
        Функция, которая просто делает трансфер нужных данных из нужных мест файла сессии telethon в файл сессии pyrogram
        """
        import sqlite3

        # Подключение к первой базе данных
        conn1 = sqlite3.connect(tl_sess_path)
        cursor1 = conn1.cursor()

        # Подключение ко второй базе данных
        conn2 = sqlite3.connect(pyro_sess_path)
        cursor2 = conn2.cursor()

        # Забираем значение из БД №1
        tl_version = cursor1.execute('SELECT version FROM version').fetchone()[0]
        tl_dc_id, tl_auth_key = cursor1.execute('SELECT dc_id, auth_key FROM sessions').fetchone()
        api_id = 2040  # надо доставать отдельно
        test_mode = 0  # всегда 0
        is_bot = 0  # всегда 0
        # tl_date, tl_id = cursor1.execute('SELECT date, id FROM entities').fetchall()[-1]
        tl_date, tl_id = datetime.datetime.now(), tl_usr_id

        # Записываем значение в БД №2
        cursor2.execute('INSERT INTO version (number) VALUES (?)', (tl_version,))
        cursor2.execute('INSERT INTO sessions (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot) '
                        'VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (tl_dc_id, api_id, test_mode, tl_auth_key, tl_date, tl_id, is_bot))
        conn2.commit()

        # Закрываем соединения с базами данных
        cursor1.close()
        conn1.close()
        cursor2.close()
        conn2.close()

    @staticmethod
    async def check_by_pyro(sess_name):
        """
        Фукнция для проверки работоспособности файла сессии pyrogram
        """
        from pyrogram import Client

        reset_txt_clr = '\033[0m'
        green_txt_clr = '\033[92m'
        red_txt_clr = '\033[91m'
        async with Client(sess_name) as app:
            try:
                getme_rslt = await app.get_me()
            except Exception as err:
                # Принтуем в терминал сообщение о неудаче
                print(f"{red_txt_clr} Не удалось проверить файл сессии Pyrogram {err}{reset_txt_clr}")
                return
            print(getme_rslt)

        # Принтуем в терминал сообщение об успехе
        print(f"{green_txt_clr}Файл сессии Pyrogram проверен и успешно работает{reset_txt_clr}")
        return True
