import os
import getpass

# 사용자 이름 (username) 가져오기
username = getpass.getuser()

# 전체 이름 (fullname) 가져오기
import ctypes


def get_full_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value


fullname = get_full_name()

print(f"사용자 이름 (Username): {username}")
print(f"전체 이름 (Fullname): {fullname}")
