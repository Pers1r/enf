# Scenariusze Testowe 

## Moduł: Katalog i Prezentacja Produktów

### ST-01: Wyświetlanie listy produktów
* **Cel:** Weryfikacja poprawnego ładowania siatki produktów w wybranej kategorii.
* **Kroki:** Wejdź w wybraną kategorię. Sprawdź, czy wyświetlają się miniatury, nazwy, kolory i ceny produktów.
* **Oczekiwany wynik:** Siatka produktów ładuje się poprawnie, a kliknięcie w miniaturę przenosi na kartę produktu.

### ST-02: Działanie filtrów i sortowania
* **Cel:** Sprawdzenie, czy filtry poprawnie zawężają wyniki.
* **Kroki:** Otwórz filtry, wybierz zakres cenowy oraz konkretny rozmiar, a następnie zastosuj zmiany.
* **Oczekiwany wynik:** Lista produktów odświeża się bez przeładowania całej strony, pokazując tylko produkty spełniające kryteria.

### ST-03: Wyszukiwarka dynamiczna (na żywo)
* **Cel:** Weryfikacja działania wyszukiwarki.
* **Kroki:** Wpisz fragment nazwy produktu w pole wyszukiwania i poczekaj ułamek sekundy.
* **Oczekiwany wynik:** Wyniki wyszukiwania zawężają się automatycznie na podstawie wpisanego tekstu.

### ST-04: Galeria zdjęć na karcie produktu
* **Cel:** Sprawdzenie podglądu dodatkowych zdjęć.
* **Kroki:** Na karcie produktu kliknij jedno ze zdjęć z dodatkowej galerii.
* **Oczekiwany wynik:** Główne zdjęcie produktu zostaje podmienione na to, które zostało kliknięte.

### ST-05: Weryfikacja stanów magazynowych na karcie produktu
* **Cel:** Zablokowanie możliwości wyboru wyprzedanego rozmiaru.
* **Kroki:** Wejdź na produkt posiadający rozmiary niedostępne w magazynie (stan = 0).
* **Oczekiwany wynik:** Przycisk wyboru takiego rozmiaru jest wyszarzony i nieaktywny, a domyślnie zaznaczony jest pierwszy dostępny rozmiar.

### ST-06: Sekcja produktów powiązanych
* **Cel:** Weryfikacja wyświetlania bloku "You may also like".
* **Kroki:** Zjedź na dół karty produktu.
* **Oczekiwany wynik:** Wyświetlają się inne, klikalne produkty z tej samej kategorii.

---

## Moduł: Koszyk Zakupowy

### ST-07: Dodanie produktu do koszyka
* **Cel:** Sprawdzenie procesu dodawania towaru.
* **Kroki:** Wybierz dostępny rozmiar i kliknij przycisk dodania do koszyka.
* **Oczekiwany wynik:** Licznik w nagłówku się aktualizuje, pojawia się powiadomienie o sukcesie, a koszyk wysuwa się z boku ekranu.

### ST-08: Zabezpieczenie przed brakiem wyboru rozmiaru
* **Cel:** Zablokowanie dodania produktu, gdy nie wybrano atrybutów.
* **Kroki:** (Jeśli dotyczy) odznacz rozmiar i spróbuj dodać do koszyka.
* **Oczekiwany wynik:** System blokuje akcję i wyświetla prośbę o wybranie rozmiaru.

### ST-09: Zmiana ilości w koszyku
* **Cel:** Poprawne przeliczanie wartości koszyka.
* **Kroki:** Otwórz koszyk i użyj przycisków "+" / "-" przy produkcie.
* **Oczekiwany wynik:** Ilość się zmienia, a cena jednostkowa i cena całkowita koszyka aktualizują się automatycznie.

### ST-10: Limit stanu magazynowego w koszyku
* **Cel:** Blokada dodania większej liczby sztuk niż dostępna.
* **Kroki:** W koszyku zwiększaj ilość produktu aż do przekroczenia dostępnego stanu w magazynie.
* **Oczekiwany wynik:** System nie pozwala na dalsze zwiększanie ilości i wyświetla komunikat o braku wystarczającej liczby sztuk.

### ST-11: Usunięcie produktu i pusty koszyk
* **Cel:** Weryfikacja akcji usuwania.
* **Kroki:** W koszyku kliknij przycisk usuwania dla jedynego znajdującego się tam produktu.
* **Oczekiwany wynik:** Produkt znika, licznik w nagłówku wskazuje '0', a w koszyku wyświetla się informacja, że jest pusty.

---

## Moduł: Proces Zakupowy (Checkout)

### ST-12: Blokada pustego checkoutu
* **Cel:** Zapobieganie błędom w zamówieniach.
* **Kroki:** Przy pustym koszyku spróbuj wejść pod adres kasy (checkout).
* **Oczekiwany wynik:** Przekierowanie do strony z komunikatem o pustym koszyku.

### ST-13: Walidacja formularza dostawy
* **Cel:** Weryfikacja pól wymaganych.
* **Kroki:** Będąc w kasie, pomiń jedno z wymaganych pól (np. miasto lub adres) i spróbuj przejść do płatności.
* **Oczekiwany wynik:** Zamówienie nie zostaje przetworzone, a system prosi o uzupełnienie brakujących danych.

### ST-14: Utworzenie zamówienia i przejście do płatności
* **Cel:** Płynne przejście do bramki płatniczej.
* **Kroki:** Wypełnij poprawnie cały formularz dostawy, wybierz metodę płatności i zatwierdź.
* **Oczekiwany wynik:** Zamówienie zapisuje się w systemie, a użytkownik zostaje przekierowany na zewnętrzną stronę operatora płatności.

### ST-15: Powrót z bramki po udanej płatności
* **Cel:** Obsługa statusu pozytywnego.
* **Kroki:** Zakończ proces płatności sukcesem na stronie operatora.
* **Oczekiwany wynik:** Użytkownik wraca do sklepu na stronę z podziękowaniem za zakupy, a jego lokalny koszyk zostaje wyczyszczony.

### ST-16: Anulowanie płatności na bramce
* **Cel:** Obsługa statusu negatywnego/anulowania.
* **Kroki:** Przerwij proces płatności na zewnętrznej stronie operatora (np. przycisk "Wróć do sklepu").
* **Oczekiwany wynik:** Użytkownik wraca do sklepu, koszyk może zostać przywrócony lub zamówienie zyskuje status "Anulowane".

---

## Moduł: Konto Użytkownika

### ST-17: Rejestracja i logowanie
* **Cel:** Podstawowa autoryzacja.
* **Kroki:** Załóż nowe konto, wyloguj się, a następnie zaloguj ponownie.
* **Oczekiwany wynik:** Procesy przebiegają pomyślnie, użytkownik ma dostęp do panelu "ACCOUNT".

### ST-18: Zarządzanie adresem domyślnym
* **Cel:** Weryfikacja edycji danych profilowych.
* **Kroki:** W panelu klienta przejdź do edycji danych, zmień adres wysyłki i zapisz.
* **Oczekiwany wynik:** Dane aktualizują się płynnie, nowy adres staje się domyślnym przy kolejnych zakupach.

### ST-19: Historia zamówień
* **Cel:** Podgląd dokonanych zakupów.
* **Kroki:** Po złożeniu zamówienia przejdź do historii zamówień w panelu użytkownika.
* **Oczekiwany wynik:** Złożone zamówienie widnieje na liście wraz z poprawnym statusem i podsumowaniem kosztów.