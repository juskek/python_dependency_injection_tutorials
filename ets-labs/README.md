## 1. Setting up local development env

### 1.1. Virtual Environment
Make sure virtual environment is created
1. Create virtual environment in root directory: `python3 -m venv .venv_ets-labs-depinj`

2. Activate virtual environment:

    // On Windows Command Shell, run:
    `.venv_ets-labs-depinj\Scripts\activate.bat`

    // On Windows Power Shell, run:
    `.venv_ets-labs-depinj\Scripts\activate.ps1`

    // On Unix or MacOS, run:
    `source .venv_ets-labs-depinj/bin/activate`

3. Update pip to install packages: `pip install --upgrade pip`
4. Install required packages: `pip install -r requirements.txt`
5. After dev, you should update requirements.txt:
   - `pip freeze > requirements.txt`
   - WARNING: this prevents any additional packages from being installed in venv, only run this command after finishing dev
   - To start installing packages in venv again, delete .venv folder and restart process 

### 1.2. Running .py files
1. While in venv, run `export PYTHONPATH='.'`
   - Helps to fix: `ModuleNotFoundError: No module named 'lib'`
   - If not, check that scripts and folders do not have the same name
2. Run `python3 path/to/file`