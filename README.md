# PetsShop - Django oraz Bootstrap

Wszystkie zdjęcia, ceny oraz opisy są ze strony https://apetete.pl

Aby wysłać mail przejdz do pliku petShop/petShop/settings.py w linii 37 i 38 wstaw swoje dane do poczty z której chcesz wysłać mail :)

## Klonowanie projektu

Aby sknolowa projekt na swoim komputerze należy wykonać następujące kroki:

1. Otwórz terminal na swoim komputerze i przejdz do lokalizacji w której chcesz zapisać projekt
2. Użyj komendy ```git clone https://github.com/uzdanska/pets-shop.git```
3. Następnie przejdz do katalogu wpisując: ```cd pets-shop```


## Konfiguracja

Należy zainstalować wszystkie pakety z pliku 'requirements.txt' używając komendy:
```pip install -r requirements.txt```


## Uruchomienie aplikacji

Aby uruchomić aplikację przejść do lokalizacji gdzie znajduje się plik 'manage.py' i użyć komendy:
```python manage.py runserver```

## Testowanie

W projekcie znajduja się również testy modeli aby je uruchomić należy użyć komendy:

```python manage.py test```

## Podsumowanie 

W designie aplikacji znajdują się każda funkcjonalność oprócz rejestracji użytkownika, która została wykonana z poziomu admina.

Dane do zalogowania klienta:
  
  * Klient:
    * login: customer
    * hasło: 1234
  * Sprzedawca: 
    * login: seller1
    * hasło: 1234

