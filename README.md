# *Траектория будущего*

Нужно дополнительно установить:

```bash
sudo apt-get install python3-venv
```

Создание *venv*:

```bash
$ python3 -m venv venv
```

Вход в *venv*:

```bash
$ source venv/bin/activate
```

Для выхода из виртуального окружения *venv* наберите:

```bash
deactivate
```

### *Установите зависимости*

```bash
(venv) ~$ python3 -m pip install --upgrade pip
(venv) ~$ pip3 install -r requirements.txt
```

Запустите проект из консоли:

```bash
(venv) ~$ python3 main.py filename.csv (Название вашего файла)
```

По умолчание проект запускается по адресу <localhost:8000>

