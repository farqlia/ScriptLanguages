from csv import reader, DictReader
with open(r'C:\Users\julia\PycharmProjects\ScriptLanguages\Uczniowie.txt',
          newline='', encoding='utf-8') as f:

    reader = DictReader(f, delimiter=';')
    for row in reader:
        print(f'''UPDATE uczniowie SET Imie='{row["Imie"]}' WHERE IdU={row["IdU"]};''')