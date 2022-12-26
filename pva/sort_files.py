import re
from pathlib import Path
import shutil


def normalize(name): # функція нормалізує рядок
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, t in zip(CYRILLIC_SYMBOLS,TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()

    return re.sub(r'\W', '_', name.translate(TRANS))


def normalize_file(file): # функція нормалізує ім'я файлу
    title, extension = Path(file).name, Path(file).suffix
    return normalize(re.sub(extension, '', title)) + extension


def moving_files(file, FOLDERS): # функція переміщює файли до відповідної категорії
    TYPES = {
        'imeges': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'video': ['AVI', 'MP4', 'MOV','MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
        }
    cut_out = False
    for key, values in TYPES.items():
        for val in values:
            if re.search(val, file.suffix, re.IGNORECASE):
                Path(FOLDERS / key).mkdir(exist_ok=True, parents = True)
                file.replace(FOLDERS / Path(key) / normalize_file(file))
                cut_out = True
    if not cut_out:
        Path(FOLDERS / 'other').mkdir(exist_ok=True, parents = True)
        file.replace(FOLDERS / 'other' / normalize_file(file))


def overrun_folder(folder, FOLDERS): # функція розпаковую папки
    for file in folder.iterdir():
        if file.is_dir():
            overrun_folder(file, FOLDERS)
            try:
                file.rmdir()
            except OSError:
                print (f'The directory "{file}" is not empty')
        else:
            moving_files(file, FOLDERS)


def unpack(FOLDERS): # функція розпакує архіви, якщо вони є
    try:
        if FOLDERS / 'archives':
            for archive in (FOLDERS / 'archives').iterdir():
                title, extension = Path(archive).name, Path(archive).suffix
                new_way = Path(FOLDERS / 'archives'/ re.sub(extension, '', title))
                Path(new_way).mkdir(exist_ok=True, parents = True)
                shutil.unpack_archive(archive, new_way, format=None)
    except FileNotFoundError:
        print('There are no archives in the folder')


def sort_trash(path_to_folder):
    FOLDERS = Path(path_to_folder)
    try:
        overrun_folder(FOLDERS, FOLDERS)
    except FileNotFoundError:
        raise FileNotFoundError(f'I can\'t find folder - {FOLDERS}')
    unpack(FOLDERS)
    return f'I sorted folder - {FOLDERS}'
