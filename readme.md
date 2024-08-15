**_Create the basic project directory_**

Initilize Git

```
git init
```

use the following to make a virtual environment:

```
python -m venv venv
```

Why do we need venv in python?

- Dependency Management: Keeps your project’s dependencies isolated from the system-wide Python installation.
- Environment Consistency: Ensures consistent behavior across different development environments.

if this doesnt work it likely means the installed python has been named python3 rather than python. This means we will also have pip3 rather than pip. To resolve this we will make a name alias for both:

```
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

```
echo "alias pip=pip3" >> ~/.zshrc
source ~/.zshrc
```

now try again

once this is made, activate the venv using:

```
source venv/bin/activate
```

in the main project directory make a src folder that will house the main code:
make the first python file main.py

```
Python Project Practice/
│
├── Practice1/
│   ├── venv/
│   └── src/ (or `app`)
│       └── main.py

```

**_Install first dependancy fastAPI:_**

```
pip install fastapi uvicorn
```

to then run the server we can use

```
uvicorn main:app --reload
```

but this isnt needed yet.

**\* Dependancy Management with requirements.txt \***

The requirements.txt file lists all the Python packages your project depends on. This ensures that anyone working on the project can install the exact versions of packages needed.

```
pip freeze > requirements.txt
```

This command captures all currently installed packages in your virtual environment and writes them to requirements.txt.

Therefore each time dependancies are installed during development it is important to run this code again to update the requirements.txt.

Others can install these dependencies by running:

```
pip install -r requirements.txt
```

**_.gitignore_**

- .gitignore: Specifies files and directories that Git should ignore, like venv/, **pycache**/, and other generated files.

Virtual environment directory (venv) (not typically included in version control).
