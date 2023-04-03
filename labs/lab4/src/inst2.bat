cd C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\src

set BACKUPS_DIR=C:\Users\julia\alt_backups

python lab4_1.py BACKUPS_DIR

dir "C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\to_archive"

python backup.py "C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\to_archive"

dir "C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\restore_here"

python restore.py "C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\restore_here"

dir "C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\restore_here"
