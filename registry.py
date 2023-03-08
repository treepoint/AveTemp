#!/usr/bin/env python3
#Для работы с регистром windows
from winregistry import WinRegistry
import support
import logger

#USAGE

""" from winregistry import WinRegistry

TEST_REG_PATH = r"HKLM\SOFTWARE\_REMOVE_ME_"


if __name__ == "__main__":
    with WinRegistry() as client:
        client.create_key(TEST_REG_PATH)
        client.write_entry(TEST_REG_PATH, "remove_me", "test")
        test_entry = client.read_entry(TEST_REG_PATH, "remove_me")
        assert test_entry.value == "test"
        client.delete_entry(TEST_REG_PATH, "remove_me") """

@logger.log
def getCurrentThemeIsLight(self):
    path = r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"

    with WinRegistry() as client:
        value = client.read_entry(path, "SystemUsesLightTheme").value

    return support.toBool(value)

if __name__ == "__main__":
    print(getCurrentThemeIsLight())