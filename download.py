import lyricsgenius
import re
import os

api_key = ""
with open("api.txt", encoding='utf-8') as file:
    for line in file:
        api_key = line
        break

genius = lyricsgenius.Genius(api_key)


discopolos = ["Bez siebie", "Gdzie prywatki te", "Jesteś szalona", "Małolatki", "Mama ostrzegała",
"Miałaś 18 lat", "Miłość w Zakopanem", "Miód malina", "Niewiara","Ona tańczy dla mnie",
"Przez twe oczy zielone", "Tylko ona jedyna", "Wymarzona", "Blondyneczko", "Gwiazda",
"Miałaś co chciałaś", "Żono moja", "Ruda tańczy jak szalona", "Co ty mi dasz",
"Królowa nocy", "Życie to są chwile", "Inna dziewczyna", "Łobuz", "Ostatni dzień ostatnia noc",
"Filmowa miłość", "Tylko ty", "Straciłaś cnotę", "Czerwone i bure", "Lato w kołobrzegu",
"Ciało do ciała", "Kochana uwierz mi", "Przekorny los", "Gdzie jesteś gdzie", "Pragnienie miłości",
"Kochana wierzę w miłość", "Kasiu Kasieńko", "Nie ma mocnych na Mariolę", "Piękna młoda",
"Niespotykany kolor", "Do białego rana", "O tobie kochana", "O ela ela", "Sexi lala",
"Pokaż jak się kręcisz", "Jagódka"]


metals = ["Apokalipsa trwa", "Autystyczny", "Bez podtekstów", "Bramy żądz", "Ewolucja albo śmierć",
"Figlarz bugi", "Głos z ciemności", "Granica rozsądku", "Herezja doskonała", "Imperium uboju",
"Kiedy umieram", "Kocica", "Koń na białym rycerzu", "Król Olch", "Krzyk kamieni", "Labirynt fauna",
"Legiony śmierci", "Loża szyderców", "Masz mnie wampirze", "Moje ostatnie tchnienie",
"Na dnie wielkiej góry", "Nie tamta już", "Niechaj stanie sie dzień", "Niepowodzenie", 
"Nim stanie się tak", "Noce szatana", "Pani Jeziora", "Pomiędzy niebem a piekłem",
"Śladem krwi", "ŚmierciŚmiech", "Śpisz jak kamień", "Spółka", "Strasznik", "Synowie ognia",
"Szalony ikar", "Wilcza jagoda", "Wspomnienia jak relikwie", "Wyciągam swoją dłoń",
"Zanurzam się", "Zdrajca metalu", "Zerwane więzi", "Zmartwychwstanie", "Ona jest zła", "Legenda",
"Niewesołowski", "Osiem", "Kim"]


def filter_lyrics(lyrics):
    final_lines = []
    lyrics = lyrics.split('\n')
    for line in lyrics:
        if len(line) > 10 and len(line) < 50 and re.match(r'^[^\[\]\<\>\_\:]+$', line):
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
                if len(line) > 10:
                    lines.append(f"{line};{type}")
    print(f"There are {len(lines)} lines with type {type}")
    return lines

download(discopolos, "discopolo")
download(metals, "metal")

all_lines = []
all_lines.append("text;class")
all_lines.extend(merge_lines_from_dir("metal"))
all_lines.extend(merge_lines_from_dir("discopolo"))

with open("dataset.csv", 'w', encoding='utf-8') as the_file:
    for line in all_lines:
        line = line.rstrip('\r\n')
        the_file.write(f"{line}\n")