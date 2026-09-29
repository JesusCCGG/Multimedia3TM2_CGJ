!pip install mutagen
cambio de la data:
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from mutagen.mp3 import MP3
# Path to your MP3 file
file_path ="/content/content/SegundoMP3.mp3"
# Load the MP3 file
audio = MP3(file_path, ID3=ID3)
# Modify metadata (e.g., Title, Artist, Album)
audio.tags.add(TIT2(encoding=3, text="Vaije a la luna")) # Title
audio.tags.add(TPE1(encoding=3, text="Juanito alimaña")) # Artist
audio.tags.add(TALB(encoding=3, text="Las poderosas")) # Album
# Save changes
audio.save()
print("Metadata updated successfully!")
obtener metadata:
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
# Path to your MP3 file
file_path = "/content/content/SegundoMP3.mp3"
# Load the MP3 file
audio = MP3(file_path, ID3=ID3)
# Loop through all tags and print them
for tag in audio.tags:
 print(f"{tag}: {audio.tags[tag]}")
obtener caratula:
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
# Path to your MP3 file
file_path = "/content/content/SegundoMP3.mp3"
# Load the MP3 file
audio = MP3(file_path, ID3=ID3)
# Find and extract the album art (APIC frame)
for tag in audio.tags.values():
 if isinstance(tag, APIC):
 # Write the image data to a file
 with open("album_art.jpg", "wb") as img_file:
 img_file.write(tag.data)
 print("Album art extracted successfully!")
 break
lectura metadata:
!pip install mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB
# Path to your MP3 file
file_path = "/content/content/SegundoMP3.mp3"
# Load the MP3 file
audio = MP3(file_path, ID3=ID3)
# Extract duration (in seconds)
duration = audio.info.length
# Extract ID3 tags (metadata)
tags = audio.tags
# Extract metadata if available
title = tags.get('TIT2', 'Unknown Title').text[0] # Song title
artist = tags.get('TPE1', 'Unknown Artist').text[0] # Artist name
album = tags.get('TALB', 'Unknown Album').text[0] # Album name
# Print metadata
print(f"Title: {title}")
print(f"Artist: {artist}")
print(f"Album: {album}")
print(f"Duration: {duration:.2f} seconds")
cambio de caratula:
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TYER, TRCK, COMM, APIC
import os
path_mp3 = "/content/content/SegundoMP3.mp3"
path_imagen = "/content/content/Img2.jpeg" # Imagen nueva
if os.path.exists(path_mp3):
 try:
 audio = ID3(path_mp3)
 except:
 audio = ID3()
 # Aplicar imagen
 if os.path.exists(path_imagen):
 with open(path_imagen, 'rb') as img_file:
 audio.delall('APIC') # Borrar anteriores
 audio.add(APIC(
 encoding=3,
 mime='image/jpeg',
 type=3,
 desc='Cover',
 data=img_file.read()
 ))
 print("Imagen añadida correctamente.")
 audio.save(path_mp3)
 print("Metadatos actualizados con éxito!")
else:
 print("No encontré el archivo MP3 en la carpeta 'mp3/'.")