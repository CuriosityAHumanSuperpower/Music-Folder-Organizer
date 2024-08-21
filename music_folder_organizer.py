import csv
import shutil
import click
import logging
from datetime import datetime
from typing import Optional, Dict, List
from mutagen.easyid3 import EasyID3
from pathlib import Path
from tqdm import tqdm
import re

# Define the music file extensions
MUSIC_EXTENSIONS = ('.mp3', '.flac', '.wav', '.m4a')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return None
    return wrapper

def sanitize_folder_name(name: str) -> str:
    """Sanitize folder name by removing forbidden characters using regex."""
    return re.sub(r'[<>:"/\\|?*]', '', name)

@print_errors
def get_music_info(file_path: Path) -> Optional[Dict[str, str]]:
    """Extract music metadata from a file."""
    audio = EasyID3(file_path)
    return {
        'name': audio.get('title', ['Unknown'])[0],
        'artists': audio.get('artist', ['Unknown'])[0],
        'main_artist': audio.get('albumartist', ['Unknown'])[0],
        'year': audio.get('date', ['Unknown'])[0],
        'album': audio.get('album', ['Unknown'])[0]
    }

@print_errors
def move_music_file(file_path: Path, info: Dict[str, str], base_folder: Path) -> Optional[Path]:
    """Move music file to a new directory structure based on metadata."""
    main_artist = info['main_artist'] if info['main_artist'] else 'Unknown'
    first_letter = main_artist[0].upper() if main_artist != 'Unknown' else 'Unknown'
    album = info['album'] if info['album'] else 'Unknown'
    
    album = sanitize_folder_name (album)
    new_folder = base_folder / first_letter / main_artist / album
    new_folder.mkdir(parents=True, exist_ok=True)
    
    new_path = new_folder / file_path.name
    shutil.move(str(file_path), str(new_path))
    return new_path

@print_errors
def delete_empty_folders(folder_path: Path) -> None:
    """Delete empty folders in the given directory."""
    for dir in folder_path.rglob('*'):
        if dir.is_dir() and not any(dir.iterdir()):
            dir.rmdir()
            logging.info(f"Deleted empty folder: {dir}")

@print_errors
def process_batch(files: List[Path], writer: csv.writer, base_folder: Path) -> None:
    """Process a batch of files."""
    for file_path in files:
        info = get_music_info(file_path)
        if info:
            new_path = move_music_file(file_path, info, base_folder)
            writer.writerow([info['name'], info['artists'], info['main_artist'], info['year'], info['album'], new_path])

@print_errors
def process_music_folder(folder_path: Path, output_csv: Path, base_folder: Path, delete_empty: bool, batch_size: int = 100) -> None:
    """Process music files in the given folder and organize them."""
    with output_csv.open(mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Artists', 'Main Artist', 'Year', 'Album', 'New Path'])

        batch, batch_count = [], 0
        files = list(folder_path.rglob('*'))
        for file_path in tqdm(files, desc="Processing files"):
            if file_path.suffix in MUSIC_EXTENSIONS:
                batch.append(file_path)
                batch_count += 1
                if batch_count >= batch_size:
                    process_batch(batch, writer, base_folder)
                    batch, batch_count = [], 0

        # Process any remaining files in the last batch
        if batch:
            process_batch(batch, writer, base_folder)

    if delete_empty:
        delete_empty_folders(folder_path)

@click.command()
@click.option('--folder_path', type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path), default=Path('.'), help='Path to the folder containing music files.')
@click.option('--base_folder', type=click.Path(file_okay=False, dir_okay=True, path_type=Path), default=Path('.'), help='Base folder for organizing music files.')
@click.option('--output_csv', type=click.Path(dir_okay=False, path_type=Path), default=Path(f'musics_{datetime.now().strftime("%Y%m%d")}.csv'), help='Output CSV file name.')
@click.option('--delete_empty', is_flag=True, help='Delete empty folders after processing.')
@click.option('--batch_size', type=int, default=100, help='Number of files to process in each batch.')
def main(folder_path: Path, base_folder: Path, output_csv: Path, delete_empty: bool, batch_size: int):
    """Main function to process and organize music files."""
    process_music_folder(folder_path, output_csv, base_folder, delete_empty, batch_size)

if __name__ == "__main__":
    main()
