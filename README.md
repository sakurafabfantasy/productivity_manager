Данный бот выполняет три задачи:
✅Управление заметками(80%)
✅Управление задачами(80%)
✅Менеджер изучения новых слов(20%)

ГАЙД ПО УСТАНОВКЕ

1) git clone https://github.com/sakurafabfantasy/productivity_manager
2) cd productivity_manager
3) python3 -m venv venv
4) source venv/bin/activate
5) pip install -r requirements.txt
6) echo "alias note='cd ~/productivity_manager && ./venv/bin/python3 -m cli.main'" >> ~/.bashrc
7) source ~/.bashrcs