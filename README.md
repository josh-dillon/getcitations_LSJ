# getcitations_LSJ
A Python script that generates an index of all citations to a given work in the Liddell–Scott–Jones Greek–English Lexicon (LSJ)
## Instructions
Download the LSJ xml files here: https://github.com/helmadik/LSJLogeion

Update the location of the files in the script (replace "/path/to/LSJ" with your directory in double quotation marks).

Run the script from Terminal:

`$ python3 getcitations_LSJ.py`

The script will prompt you to enter your author number, then the work number.

For instance, if you want an index of all words cited from the _Iliad_, enter 0012 for Homer, press return, and then enter 001. Press return again to launch the script.

Wait for the script to inform you that the words have been extracted.

Your index is contained in a tab-delimited text file called "output.txt" located in the same directory as the script. It should contain your words and their individual locations in the work. Lemmata appear in the order in which they are encountered in a given work (from beginning to end).

Note that all duplicates are automatically removed. This can be useful when a single instance of a word is cited twice in a given entry (e.g. once at the beginning in the section on morphology and later in the entry under a given sense).
## Credits
The incomparable Helma Dik of Logeion, Perseus Tufts
## Errors
Please report LSJ errors here: https://logeion.uchicago.edu/ (click "Report a Problem" at top right-hand corner).
