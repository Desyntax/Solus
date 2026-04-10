INSTRUCTIONS FOR USE:
1. Install Python 3.12.1 or newer (https://www.python.org/downloads/)
2. Run `solus.py` in its residing directory. Don't run it from an external directory or it will fail to locate some necessary files
3. If the interface looks strange, then run it on a different command line. Solus uses ANSI escape codes to stylise its text
4. Login details: Username: `desyntax`, password: `password`. You can change these either in `config.txt` or by using the `username`/`password` commands
5. Use the `help` command to view a list of commands

DO NOT run `boom`, `nano`, or `rep` on important system files or directories. Solus will probably return a `PermissionError`, but I wouldn't risk it nonetheless.
With FTP implemented, it is your responsibility to only connect to systems you are authorised to access.

KNOWN ISSUES:
* Still incompatible with Windows
* Directory symbol doesn't update (but in FTP it does)
* `scan` with `;m` attribute does not properly stylise {rainbow} content
* `sign` on very large nodes fails to calculate size

Solus v0.2.0, open-sourced project. All content, including code, falls under public domain.
