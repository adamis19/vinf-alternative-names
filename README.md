Softvér sa spúšta cez príkazový riadok. Má na výber tri rôzne parametre:

  - python main.py parse - spustenie programu s týmto parametrom začne parsovanie xml súboru a na výstupe budú súbory alternative_names.csv a statistics.txt
  - python main.py index - na tento parameter treba mať v zariadení stiahnutý Elasticsearch. Program zaindexuje vygenerovaný csv súbor z parametru parse na server
  - python main.py search {name} - program s týmto parametrom vyhľadá zo serveru zadaný string v názvoch a alternatívnych menách
