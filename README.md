# Termofluidi-App 

Termofluidi App


Deploying:

1. Create env -- pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate
4. pip install pyinstaller
5. pyinstaller app.py
6. cd dist/app
7. ./app

This is how app.spec should look like

    datas=[('fletepagesa_template.docx', '.'), ('client_list.db', '.'), ('invoice_template.docx', '.')],
    hiddenimports=['docxtpl', 'num2words', 'tkcalendar', 'babel.numbers'],

# Era Kastrati