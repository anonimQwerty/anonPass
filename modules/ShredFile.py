import os
import random
from .generatepassword import generatepassword

def ShredFile(file: str, cycles = 3):
    # Check if file exists and is not directory
    if not os.path.exists(file) or not os.path.isfile(file):
        return False
    # Shred file
    try:
        # Create random filename
        RandomFileName = generatepassword(1, 6)
        # Rewrite the data of file,
        with open(file, "ba+") as delfile:
            length = delfile.tell()
            for _ in range(cycles):
                delfile.seek(0)
                delfile.write(random._urandom(length))
        # Renames the file for completely remove traces
        os.rename(file, RandomFileName)
        # Finaly deletes the file
        os.unlink(RandomFileName)
    except Exception as error:
        print(error)
        return False
    else:
        return True