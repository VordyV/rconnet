from .default import Default
import re

class ModManager(Default):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_drive = True

    def start(self):
        super().start()
        if self.rcon_invoke("bf2cc check") == "rcon: unknown command: 'bf2cc'": self.full_drive = False

    def _has_full_drive(self):
        if not self.full_drive:
            raise Exception("Modmanager is not installed on the server")

    def list_modules(self):
        self._has_full_drive()
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
        self._has_full_drive()
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