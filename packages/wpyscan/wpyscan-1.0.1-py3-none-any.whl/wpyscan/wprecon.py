"""
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
ganapati (@G4N4P4T1) wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
----------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import re
import requests
import random

class WPRecon():
    def __init__(self, proxy):
        self.req = requests.Session()
        self.version = None
        self.readme_version = None
        if proxy is not None:
            self.req.proxies = proxy

    def scan(self, url):
        if not url.endswith('/'):
            url = "{}/".format(url)

        results = {'printable_results': [],
                   'plugins': []}

        results['printable_results'] = self.get_printable_results(url)
        results['plugins'] = self.get_plugins(url)
        return results

    def get_printable_results(self, url):
        folders = ["wp-content/uploads/", 
                   "wp-includes/"]
        themes = self.get_theme(url)

        for theme in themes:
            folders.append("wp-content/themes/{}/".format(theme.split("--")[0].strip()))
        
        results = {
            'Robots': self.get_robots(url),
            'Readme': self.get_readme(url),
            'Full path disclosure': self.get_fpd(url, folders),
            'Backup': self.get_backup(url),
            'Version': self.get_version(url),
            'Themes': themes}
        return results

    def get_user_agent(self):
        user_agents = ["Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1"]
        return random.choice(user_agents)

    # Recon methods

    def get_plugins(self, url):
        plugins = []
        headers = {'User-Agent': self.get_user_agent()}
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text, "html.parser")

        # Search pluginss in css
        plugin_paths = soup.findAll("link", {"rel": "stylesheet"})
        for plugin_path in plugin_paths:
            if 'wp-content/plugins/' in plugin_path['href']:
                regex = re.compile("wp-content/plugins/([a-zA-Z0-9-_]+)/",
                                   re.IGNORECASE)
                r = regex.findall(plugin_path['href'])
                for plugin_name in r:
                    plugins.append(plugin_name)

        # Search plugins in javascript
        plugin_paths = soup.findAll("script",
                                    {"type": "text/javascript"})
        for plugin_path in plugin_paths:
            try:
                if 'wp-content/plugins/' in plugin_path['src']:
                    regex = re.compile("wp-content/plugins/([a-zA-Z0-9-_]+)/",
                                       re.IGNORECASE)
                    r = regex.findall(plugin_path['src'])
                    for plugin_name in r:
                        plugins.append(plugin_name)
            except:
                # Silently pass, parsing html is pain in the ass
                pass

        return list(set(plugins))

    def get_robots(self, url):
        robots = []
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "{}{}".format(url, 'robots.txt')
        robots_req = self.req.get(full_url, headers=headers)
        if robots_req.status_code == 200:
            robots_text = robots_req.text.split("\r\n")
            for robot_text in robots_text:
                if (robot_text.lower().startswith('allow') or
                   robot_text.lower().startswith('disallow')):
                    robots.append(robot_text)
        if not robots:
            return None
        else:
            return robots

    def get_readme(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        full_url = "{}{}".format(url, 'readme.html')
        readme_req = self.req.get(full_url, headers=headers)
        result = None
        try:
            if readme_req.status_code == 200:
              soup = BeautifulSoup(readme_req.text, "html.parser")
              version = soup.find("h1").getText().strip()
              self.readme_version = version.replace('Version ', '')
              result = full_url
        except:
            pass
        return result

    def get_fpd(self, url, folders):
        headers = {'User-Agent': self.get_user_agent()}
        fpd = []
        for folder in folders:
            full_url = "{}{}".format(url, folder)
            fpd_req = self.req.get(full_url, headers=headers)
            if fpd_req.status_code == 200:
                if "Index of" in fpd_req.text:
                    fpd.append(full_url)
        return fpd 

    def get_backup(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        backups_find = []
        backups = ["wp-config.php~",
                   "wp-config.php.save",
                   ".wp-config.php.swp",
                   "wp-config.php.swp",
                   "wp-config.php.swo",
                   "wp-config.php_bak",
                   "wp-config.bak",
                   "wp-config.php.bak",
                   "wp-config.save",
                   "wp-config.old",
                   "wp-config.php.old",
                   "wp-config.php.orig",
                   "wp-config.orig",
                   "wp-config.php.original",
                   "wp-config.original",
                   "wp-config.txt"]
        for backup in backups:
            full_url = "{}{}".format(url, backup)
            backup_req = self.req.get(full_url, headers=headers)
            if backup_req.status_code == 200:
                backups_find.append(backup)

        if not backups_find:
            return None
        else:
            return backups_find

    def get_version(self, url):
        if self.version is not None:
            return self.version
        headers = {'User-Agent': self.get_user_agent()}
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text, "html.parser")
        generator = soup.find("meta", {'name': 'generator'})
        if generator is not None:
            try:
                self.version = generator['content'].replace('Wordpress ', '').strip()
            except:
                pass
        else:
            if self.version is None:                
                version_pos = page_req.text.find("wp_blog_version")
                if version_pos != -1:
                    version_pos += 19
                    self.version = page_req.text[version_pos:version_pos+page_req.text[version_pos:].find('";')]
                elif self.readme_version is not None:
                    self.version = self.readme_version
        return self.version

    def get_theme(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        results = []
        page_req = self.req.get(url, headers=headers)
        soup = BeautifulSoup(page_req.text, "html.parser")
        theme_paths = soup.findAll("link", {"rel": "stylesheet",
                                            "type": "text/css"})
        for theme_path in theme_paths:
            if 'wp-content/themes/' in theme_path['href']:
                regex = re.compile("wp-content/themes/([a-zA-Z0-9-_]+)/",
                                   re.IGNORECASE)
                r = regex.findall(theme_path['href'])
                if len(r) > 0:
                    full_url = "{}wp-content/themes/{}/sftp-config.json".format(url, r[0])
                    page_req = self.req.get(full_url, headers=headers)
                    if page_req.status_code == 200:
                        if "password" in page_req.text:
                            results.append("{} -- (sftp config found : {})".format(r[0], full_url))
                        else:
                            results.append(r[0])
                    else:
                        results.append(r[0])
        results = list(set(results))
        return results
