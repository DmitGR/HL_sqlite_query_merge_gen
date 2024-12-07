# sqlite_query_merge_gen
Query generator for sqlite database merge</br>
Alternate **Hogwarts Mod Merger**, but base on **your game version** and with the ability to edit the merge</br>
Simple Manual Version

## About: This script Help for Hogwarts Legacy modders or mod users generete diffrence between your mod (witch include sqlite db changes) and update your sql db  of your game version.
### Req: Python 3.7, 
Libs: os, sqlite3
## How to USE IT:

## For mod users:
1. Extract your version of the database from the game files using https://github.com/LongerWarrior/FModel/releases/tag/HW_1.0.0.0
Setting fo HL:
_________________
![image](https://github.com/user-attachments/assets/d0b73c03-ac73-456d-b531-00903535aa0c)
_________________
Choose **pakchunkO-WindowsNoEditor.pak** -> **Phoenix/Content/SQLiteDB/PhoenixShipData.sqlite** - It's your db version
_________________
3.  Move this file in main dir and Updated
_________________
4.  Extract db file from HL mod using https://github.com/RiotOreO/unrealpak<br>
Just drop your file in **Unpack.bat**
_________________
5. Move this folder to **main/Mods** dir
_________________
6. Run main.py , It's generate SQL file of differences between the mod and your DB<br>
You can change it<br>
For example, I added a script to delete all lines that have data on the **tutorial**, because it led to crash the game when installing any mods for my version of the game.<br>
You can find it in substrings = ["Tutorial", "Game"]  # Change it if you know for sure that this data crashes the start of the game<br>
_________________
7. Then run update.py to Update your db file in /Updated<br>
It's run all query from SQL query file
_________________
8. Need pack changes in pak file, using https://github.com/RiotOreO/unrealpak<br>
Create a folder tree **./z_MergedMods/Phoenix/Content/SQLiteDB** in unrealpak root foler<br>
Drop **PhoenixShipData.sqlite ** From **./Update** to **./z_MergedMods/Phoenix/Content/SQLiteDB**
_________________
9. Drop **z_MergedMods** folder in **UnrealPak-Without-Compression.bat**
_________________
10. All done drop in HL ~mods Your z_MergedMods


## For modders:
You can genrete **differences_and_updates.sql SQL file** with your mod and source HL DB file ,</br>
Then you got **Clean and correct changes for all versions of the game**</br>
How it's done at https://www.nexusmods.com/hogwartslegacy/mods/1987/</br>
And everyone will be able to do a merge with their versions of the game
