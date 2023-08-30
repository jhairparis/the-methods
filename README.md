# The methods

![](/icons/icon.png)

Please use **Python 3.8.7**
To start run each command in your terminal from windows

```bash
python -m venv env

cd env/Scripts

activate.bat //In CMD or
Activate.ps1 //In Powershel

cd ..
cd ..


pip install -r requirements.txt

```

To close project

```bash
deactivate
```

To **build**:

```bash
pyinstaller.exe --onefile --windowed --icon=icons/icon.ico --name='The methods' main.py

```
