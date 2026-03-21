INSTRUCTIONS FOR USE:
1. Install Python 3.12.1 or newer (https://www.python.org/downloads/)
2. Run `solus.py` in its residing directory. Don't run it from an external directory or it will fail to locate some necessary files
3. If the interface looks strange, then run it on a different command line. Solus uses ANSI escape codes to stylise its text
4. Login details: Username: `desyntax`, password: `password`. You can change these either in `config.txt` or by using the `username`/`password` commands
5. Use the `help` command to view a list of commands

KNOWN ISSUES:
* `nano` in OVERWRITE mode fails to overwrite the file contents, instead appends
* `scan` with `;m` attribute does not properly stylise {rainbow} content
* `sign` on very large nodes fails to calculate size
* `ls` in certain directories like root (/) does not list all directories (FIXED)
* `login` keyword in `config.txt` doesn't do anything

Solus indev_4, open-sourced project. All content, including code, falls under public domain.
