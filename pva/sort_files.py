# from concurrent.futures import ThreadPoolExecutor
import re
from pathlib import Path
import shutil
# import multiprocessing
from threading import Thread

# max_relevant_threads = multiprocessing.cpu_count()


def normalize(name: str) -> str:
    """Normalize string (filename)."""
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't',
                   'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu', 'ya', 'je', 'i', 'ji', 'g')

    trans = {}

    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.upper()

    return re.sub(r'\W', '_', name.translate(trans))


def normalize_file(file: Path) -> str:
    """Normalize filename."""
    title, extension = Path(file).name, Path(file).suffix
    return normalize(re.sub(extension, '', title)) + extension


def moving_files(file: Path, folders: Path) -> None:
    """Move file to certain folder."""
    TYPES = {
        'imeges': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'video': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'], 
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
        }
    cut_out = False
    for key, values in TYPES.items():
        for val in values:
            if re.search(val, file.suffix, re.IGNORECASE):
                Path(folders / key).mkdir(exist_ok=True, parents=True)
                file.replace(folders / Path(key) / normalize_file(file))
                cut_out = True
    if not cut_out:
        Path(folders / 'other').mkdir(exist_ok=True, parents=True)
        file.replace(folders / 'other' / normalize_file(file))
           

def overrun_folder(folder: Path, folders: Path) -> None:
    """Overrun junk folders."""
    for file_system_object in folder.iterdir():
        if file_system_object.is_dir():
            thread = Thread(target=overrun_folder, args=(file_system_object, folders))
            thread.start()
            # overrun_folder(file_system_object, folders)
            try:
                file_system_object.rmdir()
            except OSError:
                print(f'The directory "{file_system_object}" is not empty')
        else:
            moving_files(file_system_object, folders)


def unpack_in_thread(archive: Path, folders: Path) -> None:
    """Unpack one file-archive."""
    title, extension = Path(archive).name, Path(archive).suffix
    new_way = Path(folders / 'archives' / re.sub(extension, '', title))
    Path(new_way).mkdir(exist_ok=True, parents=True)
    shutil.unpack_archive(archive, new_way, format=None)


def unpack(folders: Path) -> None:
    """Unpack all archives."""
    try:
        if folders / 'archives':
            for archive in (folders / 'archives').iterdir():
                # unpack_in_thread(archive, folders)
                thread = Thread(target=unpack_in_thread, args=(archive, folders))
                thread.start()

    except FileNotFoundError:
        print('There are no archives in the folder')


def sort_trash(path_to_folder: str) -> str:
    """Sort all in junk."""
    folders = Path(path_to_folder)

    try:
        overrun_folder(folders, folders)

    except FileNotFoundError:
        raise FileNotFoundError(f'I can\'t find folder - {folders}')

    unpack(folders)

    return f'I sorted folder - {folders}'
