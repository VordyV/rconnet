import re

class Ban():
    def __init__(self, client, type=None, address=None, period=None, key=None, **kwargs):
        self.__client = client
        self.type = type
        self.address = address
        self.period = period
        self.key = key
        for option, value in kwargs.items():
            setattr(self, option, value)

    def unban(self):
        if self.type == "address": return self.__client.rcon_invoke("exec admin.removeAddressFromBanList %s" % self.address)
        elif self.type == "key": return self.__client.rcon_invoke("exec admin.removeKeyFromBanList %s" % self.key)
        else: return False

class BanManager():
    def __init__(self, client):
        self.__client = client

    def __load(self):
        blAddrs = self.__client.rcon_invoke("exec admin.listBannedAddresses")
        blKeys = self.__client.rcon_invoke("exec admin.listBannedKeys")

        banlist = []

        pattern = re.compile('(\S*?): (\S*?) (\S*)')
        for ban in blAddrs.split("\n"):
            matches = pattern.findall(ban)
            if len(matches) != 0:
                banlist.append(Ban(self.__client, type="address", address=matches[0][1], period=matches[0][2], key=None))

        for ban in blKeys.split("\n"):
            matches = pattern.findall(ban)
            if len(matches) != 0:
                banlist.append(Ban(self.__client, type="key", key=matches[0][1], period=matches[0][2], address=None))

        if len(banlist) < 1: return None
        return banlist

    @property
    def list(self):
        return self.__load()

    def clear(self):
        return self.__client.rcon_invoke("exec admin.clearBanList")