#! /data/data/com.termux/files/usr/bin/python3.x
# encoding: utf8
# copyright @val <xnver404@gmail.com>

# information about the developer
__author__ = "val (zevtyardt)"
__version__ = "0.0.2"
__description__ = "Python hash cracker"
__github__ = "https://github.com/zevtyardt"
__email__ = "xnver404[at]gmail[dot]com"

# importing module
from passlib.hash import mysql323, mysql41, lmhash, nthash
from hashlib import *
import time
import re
import argparse
import os
import requests
import sys

# lambda function
tampil = lambda s,info="info": print(f" [{time.strftime('%H:%M:%S')}] [{info.upper()}] {s}")
prog = lambda s,info="info": print(f" [{time.strftime('%H:%M:%S')}] [{info.upper()}] {s} ",end="\r")
elapsed = lambda start_time : print(f" Elapsed time {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}\n")

# hash algorithms
hashlib_hash_algos = list(i for i in algorithms_guaranteed if "shake" not in i)
passlib_hash_algos = { "mysql323":mysql323.hash, "mysql41":mysql41.hash, "lmhash":lmhash.hash, "nthash":nthash.hash }
__all__ = ["md5md5"]+[i for i in algorithms_available if "shake" not in i or i == "blake2s256" or i == "sha3-256"]+[i for i in passlib_hash_algos]

# result data
final = {}

# ------------------ the beginning of all functions ----------------

# hashing string
def hashing():
    print ('') # new line
    for type in __all__:
        sys.stdout.write(type+':'+('\t'*2)) if len(type) <= 6 else sys.stdout.write(type+':\t')
        if type in list(o for o in algorithms_available if "shake" not in o):
            m = new(type)
            m.update(arg.string.encode())
            print(m.hexdigest())
        elif type == 'md5md5':
            obj1 = md5(arg.string.encode()).hexdigest()
            print(md5(obj1.encode()).hexdigest())
        else:
            print(passlib_hash_algos[type](arg.string.encode()))
    print ('') # new line

# verify hash type
class verify:
    def __init__(self,hash_to_verify):
        def build_re(hex_len, prefix=r"", suffix=r"(:.+)?"):
           regex_string = r"^{}[a-f0-9]{{{}}}{}$".format(prefix, hex_len, suffix)
           return re.compile(regex_string, re.IGNORECASE)

        self.hash_to_verify = hash_to_verify
        self.HASH_TYPE_REGEX = {
            build_re(32, prefix="(md5)?"): [ "md5md5", "md5", "md4", "nthash", "lmhash", "mdc2" ],
            build_re(16, prefix="(0x)?", suffix="(L)?"): [ "mysql323" ],
            build_re(64): [ "sha256", "sha3_256", "sm3", "sha512-256" ],
            build_re(128): [ "sha512", "whirlpool", "sha3_512", "blake2b512", "blake2b" ],
            build_re(56, suffix=""): [ "sha224", "sha3_224" ],
            build_re(40): [ "sha1", "ripemd160" ],
            build_re(96, suffix="", prefix="(0x0100)?"): [ "sha384", "sha3_384" ],
            build_re(40, prefix=r"\*", suffix=""):  [ "mysql41" ],
        }

        self.verify_hash_type()

    def verify_hash_type(self):
        """verify the type of hash using regex"""
        for regex, hash_types in self.HASH_TYPE_REGEX.items():
            if regex.match(self.hash_to_verify) or regex.match("*"+self.hash_to_verify):
                final[self.hash_to_verify] = hash_types

# create new wordlist
class create_new_wordlist:
    def __init__(self):
        self.hashes = [i for i in hashes]

    def _create(self):
        """make your own internal word list (success rate of ± 70%)"""
        words = []

        for numhash,hash in enumerate(self.hashes):
            response = requests.get(f"http://www.google.com/search?q={hash}").text
            list_temp = response.replace(".", " ").replace(":", " ").replace("?", "").replace("(", " ").replace(""", " ").replace("""," ").replace("“"," ").replace("”"," ").replace(","," ").replace(";"," ").replace("="," ").replace(">"," ").replace("<"," ").replace("/"," ").replace(")"," ").replace("{"," ").replace("}"," ").replace("&"," ").replace("-"," ").replace("_"," ").replace("%3F"," ").replace("%26"," ").replace("%3D"," ").replace("%2B","+").replace("#"," ").replace("]"," ").replace("["," ").split()
            for numtemp,word in enumerate(list_temp):
                print (f" [{time.strftime('%H:%M:%S')}] [INFO] line:{numhash+1}/{len(self.hashes)} | percent: {int(((numtemp+1) / len(list_temp)) * 100)}% ({int(((numhash+1) / len(self.hashes)) * 100)}%) | total: {len(words)} ",end="\r")
                if word not in words:
                    words.append(word)
        print ("") # new line
        tampil(f"Total words generated: {len(words)} words.")
        return words

# main function
class zevcrack:
    def __init__(self,hash,type):
        self.func = { "sha256":sha256, "md5":md5, "sha3_384":sha3_384, "sha512":sha512, "sha224":sha224, "blake2s":blake2s, "sha3_224":sha3_224,       "sha1":sha1, "shake_128":shake_128, "sha384":sha384, "sha3_256":sha3_256, "blake2b":blake2b, "sha3_512":sha3_512 }
        self.bin2hex = lambda s: "".join(hex(ord(i)) for i in s).replace("0x","")
        self.hash = hash
        self.type = type

    def mode1(self):
        for num,i in enumerate(wordlist):
            if (self.func[self.type](i.encode()).hexdigest()) == self.hash:
                return self._found(i,num+1,self.type,self.hash)
        return None

    def mode2(self):
        hash_ = ("*"+self.hash) if self.type == "mysql41" else self.hash
        for num,i in enumerate(wordlist):
            if passlib_hash_algos[self.type](i.encode()) == hash_:
                return self._found(i,num+1,self.type,hash_)

    def mode3(self):
        for num,i in enumerate(wordlist):
            h = new(self.type)
            h.update(i.encode())
            if (h.hexdigest()) == self.hash:
                return self._found(i,num+1,self.type,self.hash)

    def double(self):
        for num,i in enumerate(wordlist):
            obj1 = self.func[self.type[:3]](i.encode()).hexdigest()
            if self.func[self.type[:3]](obj1.encode()).hexdigest() == self.hash:
                return self._found(i,num+1,self.type,self.hash)

    def _found(self,plaintext,line,type,hash):
        space = ("(space)" if plaintext == " " else "")
        return (f"\n\n * Clear text:\t\t{plaintext} (0x{self.bin2hex(plaintext)}) {space}\n * tries attempted:\t{line}\n * Hash:\t\t{hash}\n * Algorithm used:\t{type}\n")

def _start(types,hash):
    for type in types:
        prog(f"algorithm: {type}      ")
        if type in hashlib_hash_algos:
            obj = [zevcrack(hash,type).mode1()]
            if obj[0]: return (obj[0])
        elif type == "md5md5":
            obj = [zevcrack(hash,type).double()]
            if obj[0]: return (obj[0])
        elif type in passlib_hash_algos:
            obj = [zevcrack(hash,type).mode2()]
            if obj[0]: return (obj[0])
        else:
            obj = [zevcrack(hash,type).mode3()]
            if obj[0]: return (obj[0])
    return (f"\n\n * Status:\t\tNOT FOUND\n * Hash:\t\t{hash}\n")

# ---------------------- end of all funtions -------------------- #

def main():

    parse = argparse.ArgumentParser(usage="python %(prog)s <arguments>",epilog="** if the hash type is more than one. use separator \",\" **")
    parse.add_argument("-c",metavar="<hash>",dest="hash",help="Specify a hash to crack.")
    parse.add_argument("-l",metavar="<file-path>",dest="file",help="Provide a file of hashes to crack.")
    parse.add_argument("-w",metavar="<wordlist>",dest="wordlist",help="Wordlist or \"stdin\" for standard input.")
    parse.add_argument("-t",metavar="<hash type>",dest="type",help="The type of hash.")
    parse.add_argument("-o",metavar="<output file>",dest="output",help="Save session/results to file.")
    parse.add_argument('-d',metavar='<string>',dest='string',help='Hash <string> with all supported hash types.')
    parse.add_argument("--verify",action="store_true",dest="verify",help="Attempt to find the type of algorithm used by the hash.")
    parse.add_argument("--show-hash",action="store_true",dest="show",help="show all supported hash type.")
    parse.add_argument("--verbose",action="store_true",dest="verbose",help="Run the application verbosely.")
    parse.add_argument('--version',action='store_true',dest='version',help='Display the version information and exit.')
    arg = parse.parse_args()

    try:
        if arg.version: print (f'{__version__}');exit()
        if arg.string: hashing();exit()
        if arg.show:
            print ("\nSupported hash types:")
            for num,i in enumerate(__all__):
                if num == 0: sys.stdout.write("\t")
                sys.stdout.write(i+" ")
                if (num+1) % 4 == 0:sys.stdout.write("\n\t")
            print ("\n** Do not include the * in mysql41 hashes. **\n");exit() # new line and exit

        if arg.hash or arg.file:
            print (f" {__description__} v{__version__}: {__github__}\n")
            hashes = [i.strip() for i in open(arg.file,"r").readlines()] if arg.file else [arg.hash]
            if arg.verbose: tampil(f"Begin executing: {time.strftime('%c')}")
            if arg.output: tampil(f"Session file: {arg.output}")
            if arg.hash: tampil(f"Hash: {arg.hash}")
            elif arg.file: tampil(f"Hash file: {os.path.join(os.getcwd(),arg.file)}")

            # verify
            if arg.verify:
                tampil("Automatic hash type detection is activated.")
                if arg.file: tampil(f"Found a total of {len(hashes)} hashes to verify.")
                for hash in hashes:
                    if arg.verbose: prog(f"Analizing hash: {hash[:25]}..")
                    verify(hash)
                if arg.verbose: print ("") # new line
                if arg.hash and len(final) > 0: tampil(f"Use possible hash type: {final[arg.hash]}")
                elif arg.file and len(final) > 0: tampil(f"Can only analyze {len(final)} out of {len(hashes)} hashes.")
                else: tampil("Can\"t find an algorithm that is suitable.\n Aborting..\n");exit()

            elif arg.verify == False or arg.type == None:
                if arg.type == None: tampil("Hash type not entered.","warn")
                elif arg.verify == False: tampil("Automatic hash detection is not activated.","warn")
                if arg.type:
                    for hash in hashes:
                        type_temp = []
                        for type in arg.type.split(","):
                            if type not in type_temp:
                                type_temp.append(type)
                        final[hash] = type_temp
                    if arg.type: tampil(f"Use hash type: {arg.type.split(',')}")
                else:
                    tampil("use all existing hash types..")
                    for hash in hashes:
                        final[hash] = __all__

            if arg.wordlist == None:
                tampil(f"Wordlist file can\"t be found, create new wordlist.","warn")
                wordlist = create_new_wordlist()._create()

            elif arg.wordlist:
                tampil(f"Wordlist path: {os.path.join(os.getcwd(),arg.wordlist)}")
                wordlist = [i.strip() for i in open(arg.wordlist,"r").readlines()]
                tampil(f"{len(wordlist)} words loaded.")

            if len(wordlist) >= 5000: tampil("The wordlist that is used too much, maybe it will take a little longer.\n","warn")
            else: print ("") # new line

            # start cracking
            if len(hashes) > 0:
                tampil("start cracking with brute force method.")
                for hash,types in final.items():
                    start_time = time.time()
                    result = [_start(types,hash)]
                    if result: print(result[0])
                    if arg.output:
                        output = open(arg.output,"a")
                        output.write(f"\n # {' '*21}{time.strftime('%c')}\n{result[0][2:]}")
                        if arg.wordlist:
                            output.write(f' * In wordlist:\t\t{os.path.join(os.getcwd(),arg.wordlist)}\n')
                    elapsed(start_time)
                if arg.verbose: tampil(f"Completed on: {time.strftime('%c')}\n")
        else: parse.print_help()

    except KeyboardInterrupt: print("\r \n Signal Interrupt caught.\n Aborting..\n")
    except Exception as e: print(f"\r \n {e}.\n Aborting..\n")
