from PIL import ImageGrab
import time
import hashlib
import pyAesCrypt
import os
import argparse

FILENAME = hashlib.sha1(str(time.time()).encode()).hexdigest() + ".jpg"
ENCRYPTION_PASSWORD = 'Elm34lp9Avm43l2C3n4lkmM1kQwe'

def take_screenshot():
    ImageGrab.grab().save(FILENAME, "JPEG")

def encrypt_file(filename, password):
    with open(filename, "rb") as infile:
        with open(filename[:-4] + ".aes", "wb") as outfile:
            pyAesCrypt.encryptStream(infile, outfile, password, (64 * 1024))

def clean_up(filename):
    os.remove(filename)

def decrypt(filename, password):
    with open(filename, "rb") as infile:
        with open(filename[:-4] + ".jpg", "wb") as outfile:
            try:
                pyAesCrypt.decryptStream(infile, outfile, password, (64 * 1024), os.stat(filename).st_size)
            except ValueError:
                os.remove(filename[:-4] + ".jpg")

def Main():
    parser = argparse.ArgumentParser(description = "command-line args")
    parser.add_argument("-m", "--mode", help="'capture' or 'decrypt' a screenshot")
    parser.add_argument("-f", "--filename", help="name of image file to decrypt")
    args = parser.parse_args()

    if args.mode == "capture":
            take_screenshot()
            encrypt_file(FILENAME, ENCRYPTION_PASSWORD)
            clean_up(FILENAME)
    elif args.mode == "decrypt" and args.filename is not None:
        decrypt(args.filename, ENCRYPTION_PASSWORD)
    else:
        print("Usage: python screenshot.py [mode] [file to decrypt]")

if __name__ == '__main__':
    Main()
