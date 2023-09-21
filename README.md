# The methods

![](/icons/icon.png)

The methods are a project created for the subject of numerical analysis, based on books such as
- Matemáticas para Ingeniería. Métodos numéricos con Python (2017)
- Análisis numérico / Richard L. Burden, J. Douglas Faires


## Use

Download .exe and execute [link](https://jhairparis.com/)

or

With **Python 3.8.7** run each command in your terminal from windows

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

## Build

```bash
pyinstaller.exe --onefile --windowed --icon=icons/icon.ico --name='The methods' main.py

```

![](icons/license.png)
