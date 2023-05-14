# Serializacja obiektów
# serializacja, marshalling, deserializacja, bazy danych
# jeśli obiekty mają przypisane funkcje (tez obiekty) to JSON już nie przejdzie
# Można w formie stringa zachować
# Jeśli obiekty mają wzajemne referencje do siebie,
# pickle - ogorek pik;
# w pickle obiekt -> ciag bajtow w danym protokole
# pickle jest docelowo binarny
# Pickle jest raczej ograniczony do Pythona
# do pickla możemy wstrzyknąć kod, który może być
# szkodliwy

from labs.lab7.src.app import Duck
import pickle

if __name__ == "__main__":

    english_duck = Duck("Maria", 19, ["bread"])
    polish_duck = Duck("Kwaczka", 19, ["chleb", "groszek"])

    english_duck.set_friend(polish_duck)

    english_duck.set_quack(lambda x: print("quaack"))

    ducks = [english_duck, polish_duck]

    pickled_ducks = pickle.dumps(ducks)

    print(pickled_ducks)

    loaded_ducks = pickle.loads(pickled_ducks)

    print(loaded_ducks)
    loaded_ducks[0].quack()




