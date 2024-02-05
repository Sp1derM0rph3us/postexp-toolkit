#!/usr/bin/python3
# Simple Linux hash cracker python script
# Made by: Sp1d3rM0rph3us
import sys, crypt, re


"""
Processo:
1 - Abrir a wordlist
2 - Abrir a lista de hashes
3 - Identificar o salt
4 - Salvar a hash alvo
5 - Utilizando a wordlist, salt e a crypt() gerar hashes até que uma seja idêntica a hash alvo.
"""

### OPEN THE WORDLIST

def open_passlist(passlist):
    wordlist = []
    try:
        with open(passlist, "r") as file:
            for line in file:
                wordlist.append(line.strip())

    except FileNotFoundError:
        print(f"[-] File {passlist} not found.")
        return None

    except Exception as e:
        print(f"[-] Failed to open wordlist: {e}")
        return None

    finally:
        return wordlist

### OPEN HASHLIST

def open_hashlist(hashes):
    hashlist = []
    try:
        with open(hashes, "r") as file:
            for line in file:
                hashlist.append(line.strip())

    except FileNotFoundError:
        print(f"[-] File {hashes} not found.")
        return None

    except Exception as e:
        print(f"[-] Failed to open hashes file: {e}")
        return None

    finally:
        return hashlist

### FINDING THE SALT

def get_salt(hashlist):
    salts = []

    try:
        for hash in hashlist:
            parts = hash.split('$')
            if len(parts) == 4:
                salt = f"${parts[1]}${parts[2]}$"
                salts.append(salt)

            elif len(parts) >= 4:
                salt = f"${parts[1]}${parts[2]}${parts[3]}$"
                salts.append(salt)
                
    except Exception as e:
        print(f"[-] Failed to get hashe's salt: {e}")
        return None

    finally:
        return salts

def hash_crack(wordlist, hashlist, salts):
    cracked_hash = []
    passwords = []


    try:
        print(f"[*] BRUTING...")
        for h in hashlist:
            fhash = f"{h}/"
            for salt in salts:
                for word in wordlist:
                    cracking_hash = crypt.crypt(word,salt)

                    if cracking_hash == fhash:
                        cracked_hash.append(h)
                        passwords.append(word)
                        print(f"[+] PASSWORD FOUND: {word}:{h}")

    except Exception as e:
        print(f"[-] Failed to perform brute force attack: {e}")

    finally:
        return cracked_hash, passwords

# ==================================================== #


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 spidercrack.py [hashlist] [wordlist]")
        
    else:

        print("""
        ======//======
        SPIDER-CRACKER
        ======//======
              ||
              ||
              ||
              ||

        Made by: Sp1d3rM0rph3us

        """)

        hashes = sys.argv[1]
        passlist = sys.argv[2]
        
        try:
            hashlist = open_hashlist(hashes)
            wordlist = open_passlist(passlist)

        except Exception as e:
            print(f"[-] Failed to open files: {e}")

        try:
            salts = get_salt(hashlist)
            if salts:
                pass
            else:
                print("Couldn't find salts")

        except Exception as e:
            print(f"[-] Couldn't find hash salts: {e}")

        try:
            cracked_hash, passwords = hash_crack(wordlist, hashlist, salts)
            if cracked_hash and passwords:
                print("[!] CRACKED HASHES:")
                for h in cracked_hash:
                    for p in passwords:
                        print(f"    [+] {h}")
                        print(f"     |----> [+] {p}")

            else:
                print("[-] Brute force performed successfully but no hash could be cracked.")

        except Exception as e:
            print(f"[-] Failed to perform brute force attack: {e}")


if __name__ == "__main__":
    main()
