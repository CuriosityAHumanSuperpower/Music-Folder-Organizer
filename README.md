```markdown
# Music Folder Organizer

`music_folder_organizer.py` is a Python script designed to organize music files in a specified folder and its subfolders. The script extracts metadata from music files, moves them into a structured directory based on the metadata, and logs the details into a CSV file. It also includes options to delete empty folders after processing.

## Features

- **Metadata Extraction**: Extracts music metadata such as title, artist, main artist, year, and album.
- **File Organization**: Moves music files into a structured directory based on the first letter of the main artist, main artist name, and album name.
- **CSV Logging**: Logs the metadata and new file paths into a CSV file.
- **Batch Processing**: Processes files in batches to manage memory usage efficiently.
- **Progress Bar**: Displays a progress bar to indicate the script's progress.
- **Empty Folder Deletion**: Optionally deletes empty folders after processing.

## Requirements

- Python 3.6+
- `mutagen` library
- `tqdm` library
- `click` library

You can install the required libraries using pip:

```sh
pip install mutagen tqdm click
```

## Usage

```sh
python music_folder_organizer.py --folder_path /path/to/music --base_folder /path/to/organize --delete_empty
```

### Command-Line Arguments

- `--folder_path`: Path to the folder containing music files. Default is the current directory (`.`).
- `--base_folder`: Base folder for organizing music files. Default is the current directory (`.`).
- `--output_csv`: Output CSV file name. Default is `musics_YYYYMMDD.csv` (based on the current date).
- `--delete_empty`: Delete empty folders after processing. This is a flag and does not require a value.
- `--batch_size`: Number of files to process in each batch. Default is 100.

### Example

```sh
python music_folder_organizer.py --folder_path /path/to/music --base_folder /path/to/organize --output_csv organized_music.csv --delete_empty --batch_size 50
```

## Script Overview

### Functions

- **`get_music_info(file_path: Path) -> Optional[Dict[str, str]]`**: Extracts metadata from a music file.
- **`move_music_file(file_path: Path, info: Dict[str, str], base_folder: Path) -> Optional[Path]`**: Moves a music file to a new directory structure based on metadata.
- **`delete_empty_folders(folder_path: Path) -> None`**: Deletes empty folders in the given directory.
- **`process_batch(files: List[Path], writer: csv.writer, base_folder: Path) -> None`**: Processes a batch of files.
- **`process_music_folder(folder_path: Path, output_csv: Path, base_folder: Path, delete_empty: bool, batch_size: int = 100) -> None`**: Processes music files in the given folder and organizes them.

### Error Handling

The script uses a decorator `print_errors` to catch and log errors in the functions.

### Logging

The script uses the `logging` module to log messages, which helps in debugging and tracking the script's progress.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
```
