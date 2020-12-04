import hashlib

hash = hashlib.md5()  #string in md5() is for add salt

passwd = 'yoyo'
# passwd is the string which to be encryted
hash.update(passwd.encode())

pwd = hash.hexdigest()

