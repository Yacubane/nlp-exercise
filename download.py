import lyricsgenius
import re
import os

api_key = ""
with open("api.txt", encoding='utf-8') as file:
    for line in file:
        api_key = line
        break

genius = lyricsgenius.Genius(api_key)


discopolos = ["Przez twe oczy zielone", "Miłość w Zakopanem", "Żono moja", "Nasza jest noc",
"Kochana wierzę w miłość", "Prawdziwa miłość to ty", "Królowa jednej nocy", "Jesteś szalona",
"Wolność moja jedyna", "Miałaś 18 lat", "Dlaczego ty mi w głowie zawróciłaś",
"Lubisz to lubisz", "Chce się żyć", "Wymarzona", "Miód malina", "Dziewczyna z sąsiedniej ulicy",
"Tylko ona jedyna", "Tańczę z nim do rana", "Niespotykany kolor oczy", "Weselny klimat",
"Ona tańczy dla mnie", "Zabrałaś serce moje", "Zakochany klaun", "Pokaż jak się kręcisz",
 "Bez siebie", "Ona buja sie kozacko", "Rozpieszczona dama", "Dam jej biały welon i obrączki dwie",
 "Majteczki w kropeczki", "Małolatki", "Moja dama", "Ogród pełen róż", "Zwariowana noc", "Mama ostrzegała",
 "Ona by tak chciała", "Skradnę cię", "Więc kochaj", "Gdzie prywatki te", "Cyganeczka Zosia",
 "Niewiara", "Kasiu, Kasieńko"]


metals = ["Szalony ikar", "Kiedy umieram", "Wyciągam swoją dłoń", "Noce szatana", "Pani Panna", "Król Olch",
"Dziewczyna z kebabem", "Pani Jeziora", "Kocica", "Bramy żądz", "Spółka", "Bez podtekstów", 
"Ewolucja albo śmierć", "Koń na białym rycerzu", "Kto jest winien?", "Niepowodzenie", "Nim stanie się tak",
"Nie tamta już", "Wilcza jagoda", "Wspomnienia jak relikwie", "Figlarz bugi", "Zdrajca metalu", "Zanurzam się",
"Niechaj stanie sie dzień", "Śladem krwi", "Na dnie wielkiej góry", "Imperium uboju", "Niewolność", 
"Labirynt fauna", "Strasznik", "Pomiędzy niebem a piekłem", "Masz mnie wampirze", "Głos z ciemności", "Śpisz jak kamień",
"Autystyczny", "Loża szyderców", "Krzyk kamieni", "Apokalipsa trwa", "Moje ostatnie tchnienie", "Herezja doskonała",
"Legiony śmierci", "ŚmierciŚmiech", "Granica rozsądku", "Zerwane więzi", "Synowie ognia"]


def filter_lyrics(lyrics):
    final_lines = []
    lyrics = lyrics.split('\n')
    for line in lyrics:
        if len(line) > 15 and len(line) < 50 and re.match(r'^[^\[\]\<\>\_\:]+$', line):
            final_lines.append(line)
    return final_lines

def download(array, folder):
    for music_name in array:
        filepath = f"{folder}/{music_name}.txt"
        if not os.path.isfile(filepath):
            song = genius.search_song(music_name)
            if song:
                filtered_lyrics = filter_lyrics(song.lyrics)
                with open(filepath, 'a', encoding='utf-8') as the_file:
                    for line in filtered_lyrics:
                        the_file.write(f'{line}\n')
            else:
                print(f"Cannot find {music_name}")

def merge_lines_from_dir(type):
    lines = []
    for filename in os.listdir(f"{type}/"):
        with open(f"{type}/{filename}", encoding='utf-8') as file:
            for line in file:
                line = line.rstrip('\r\n').replace(';', '')
                if len(line) > 5:
                    lines.append(f"{line};{type}")
    return lines

# download(discopolos, "discopolo")
# download(metals, "metal")

all_lines = []
all_lines.append("text;class")
all_lines.extend(merge_lines_from_dir("metal"))
all_lines.extend(merge_lines_from_dir("discopolo"))

with open("dataset.csv", 'w', encoding='utf-8') as the_file:
    for line in all_lines:
        line = line.rstrip('\r\n')
        the_file.write(f"{line}\n")