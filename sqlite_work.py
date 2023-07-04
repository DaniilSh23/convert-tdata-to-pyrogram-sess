

def sqlite_data_transfer(tl_sess_path, pyro_sess_path):
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
    api_id = 2040   # надо доставать отдельно
    test_mode = 0   # всегда 0
    is_bot = 0  # всегда 0
    tl_date, tl_id = cursor1.execute('SELECT date, id FROM entities').fetchall()[-1]

    # Записываем значение в БД №2
    cursor2.execute('INSERT INTO version (number) VALUES (?)', (tl_version,))
    cursor2.execute('INSERT INTO sessions (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?)', (tl_dc_id, api_id, test_mode, tl_auth_key, tl_date, tl_id, is_bot))
    conn2.commit()

    # Закрываем соединения с базами данных
    cursor1.close()
    conn1.close()
    cursor2.close()
    conn2.close()
