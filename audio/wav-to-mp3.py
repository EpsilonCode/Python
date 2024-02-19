import subprocess
import os
import musicbrainzngs as mb

def rip_cd_to_wav(output_directory):
    # Rip the CD to WAV files
    subprocess.run(['cdparanoia', '-B', '-d', '/dev/cdromX', f'--output-wav={output_directory}'])

def convert_wav_to_flac(wav_directory, flac_directory):
    # Convert WAV files to FLAC
    for wav_file in os.listdir(wav_directory):
        if wav_file.endswith('.wav'):
            wav_path = os.path.join(wav_directory, wav_file)
            flac_path = os.path.join(flac_directory, wav_file.replace('.wav', '.flac'))
            subprocess.run(['flac', wav_path, '-o', flac_path])

def fetch_metadata(artist_name, album_title):
    # Fetch metadata from MusicBrainz
    mb.set_useragent("music_backup_script", "0.1", "your-contact-info")
    result = mb.search_releases(artist=artist_name, release=album_title, limit=1)
    return result

def rename_files(flac_directory, metadata):
    # Rename FLAC files based on metadata
    for i, track in enumerate(metadata['release-list'][0]['medium-list'][0]['track-list']):
        original_filename = os.path.join(flac_directory, f"track{i+1}.flac")
        new_filename = os.path.join(flac_directory, f"{track['number']} - {track['title']}.flac")
        if os.path.exists(original_filename):
            os.rename(original_filename, new_filename)

def main():
    wav_directory = 'path/to/wav'
    flac_directory = 'path/to/flac'
    
    # Rip and Convert
    rip_cd_to_wav(wav_directory)
    convert_wav_to_flac(wav_directory, flac_directory)

    # Fetch Metadata
    artist_name = input("Enter artist name: ")
    album_title = input("Enter album title: ")
    metadata = fetch_metadata(artist_name, album_title)

    # Rename Files
    if metadata and 'release-list' in metadata and len(metadata['release-list']) > 0:
        rename_files(flac_directory, metadata)
    else:
        print("Metadata not found for the given album.")

if __name__ == "__main__":
    main()
