from .default import Default
from .modules.modmanager.bf2cc import Bf2cc
import re
import xml.etree.ElementTree as ET

class Ban():
    def __init__(self, client, method: str = None, address: str = None, period: str = None, cdkeyhash: str = None, datetime: str = None, nick: str = None, profileid: int = None, by: str = None, reason: str = None):
        self.__client = client
        self.method = method
        self.address = address
        self.period = period
        self.cdkeyhash = cdkeyhash
        self.datetime = datetime
        self.nick = nick
        self.profileid = profileid
        self.by = by
        self.reason = reason

    def __repr__(self):
        if self.method == "Address": return "Ban(address=%s, period=%s)" % (self.address, self.period)
        elif self.method == "Key": return "Ban(key=%s, period=%s)" % (self.cdkeyhash, self.period)
        else: return "Ban(key=%s, address=%s, period=%s, type=%s)" % (self.cdkeyhash, self.address, self.period, self.method)

    def unban(self):
        if self.method == "Address": return self.__client.rcon_invoke(f"bm removeBan {self.address}")
        elif self.method == "Key": return self.__client.rcon_invoke(f"bm removeBan {self.cdkeyhash}")
        else: return False

class BanManager:

    def __init__(self, client):
        self.__client = client

    def __load(self) -> list[Ban]:
        bl = self.__client.rcon_invoke("bm listBans")
        root = ET.fromstring(bl)
        bans = []

        fields = ['datetime', 'nick', 'method', 'period', 'address',
                  'cdkeyhash', 'profileid', 'by', 'reason']

        for ban_elem in root.findall('ban'):
            data = {}
            for field in fields:
                elem = ban_elem.find(field)
                data[field] = elem.text if elem is not None and elem.text else ''
            bans.append(Ban(self.__client, **data))

        return bans

    @property
    def list(self): return self.__load()

class ModManager(Default):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.banmanager = BanManager(self)
        self.bf2cc = Bf2cc(self)

    def start(self):
        super().start()
        if self.rcon_invoke("bf2cc check") == "rcon: unknown command: 'bf2cc'":
            raise Exception("Modmanager is not installed on the server")

    def list_modules(self):
        modules = {}
        pattern = r"^(.*?)\s+v(\d+\.\d+)\s+\(\s+(.*?)\s+\)$"
        lines = self.rcon_invoke("mm listModules")
        for line in lines.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                modules[match.group(1)] = {
                    "version": match.group(2),
                    "status": match.group(3)
                }

        return modules

    def config(self):
        pattern = r'(?P<section>\w+)\.(?P<option>\w+)\s+(?:(?P<value_int>\d+)|\"(?P<value_str>[^\"]+)\")'
        sections = {}

        data = self.rcon_invoke("mm printRunningConfig")
        for line in data.split("\n"):
            line = line.strip()

            if line.startswith("#"):
                continue

            match = re.match(pattern, line)

            if not match:
                continue

            section = match.group('section')
            option = match.group('option')
            value = match.group('value_int') or match.group('value_str')

            if value.isdigit(): value = int(value)

            sections[section] = sections.get(section, {})

            if option.startswith("add") or option == "loadModule":
                sections[section][option] = sections[section].get(option, [])
                sections[section][option].append(value)
            else:
                sections[section][option] = sections[section].get(option, value)

        return sections

    def reload_module(self, module:str):
        return self.rcon_invoke("mm reloadModule %s" % module)

    def start_module(self, module:str):
        return self.rcon_invoke("mm startModule %s" % module)

    def shutdown_module(self, module:str):
        return self.rcon_invoke("mm shutdownModule %s" % module)

    def load_module(self, module:str):
        return self.rcon_invoke("mm loadModule %s" % module)

    def save_config(self):
        return self.rcon_invoke("mm saveConfig")

    def set_param(self, module:str, option:str, value:str):
        return self.rcon_invoke("mm setParam %s %s %s" % (module, option, value))