# postać słownikowa (klucz, wartość)

import dbm

if __name__ == "__main__":

    filepath = "./mydbm"
    with dbm.open(filepath, flag="c", mode=0o666) as mapping:
        print(dbm.whichdb(filepath))
        print(mapping)
