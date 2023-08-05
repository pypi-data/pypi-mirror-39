Wpyscan
=======

Wordpress pentest tool

Description :
-------------

Scan wordpress for infos:
 - Modules
 - Version
 - Theme
 - Robots.txt
 - Readme.html
 - Full path disclosure
 - Backups files
 - Directory listing in upload directory

Search exploits on exploit-db, wordpressexploit.com and wpvulndb.com according to recon informations (version, modules and theme).

Input arguments :
-----------------
usage: wpyscan.py [-h] -u URL [-r] [-t] [-p PROXY]

Sploit Wordpress for fun

optional arguments:
  - h, --help : show this help message and exit
  - u URL, --url URL : victim url
  - r, --recon : Just recon (no sploits)
  - t, --tor : Use Tor
  - p PROXY, --proxy PROXY : Use proxy (ip:port)
