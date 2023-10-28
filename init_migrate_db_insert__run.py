import os
import shutil
from time import sleep

if os.path.exists("migrations"):
    shutil.rmtree("migrations")
if os.path.exists("app/database.sqlite"):
    os.remove("app/database.sqlite")
    
    
os.system("source venv/bin/activate")
sleep(1)
os.system("flask db init")
sleep(1)
os.system("flask db migrate")
sleep(1)
os.system("flask db upgrade")
sleep(1)
os.system("python insert_demo_data.py")
sleep(1)
os.system("python main.py")
