from zipfile import ZipFile
import codecs

class User:
    displayname = ''
    age = -1
    def new_user(self, name, age):
        self.displayname = name
        self.age = age

def del_space(s):
    a = []
    i = 0
    while (i < len(s)):
        k = i
        while (i != len(s)) and (s[i] != ' '):
            i += 1
        a.append(s[k:i])
        i += 1
    return a


fout = open("test.txt", "w")
fout2 = open("test2.txt", "w")
fout3 = open("test3.txt", "w")
f_users = codecs.open('users.xml', encoding='cp1251')
# 'cp1251')

users = []
#for s in f_users.readlines():
for i in range(100):
    s = f_users.readline()
    a = del_space(s)
    name = ''
    age = -1
    #print(a, file=fout2)
    for elem in a:
        print(elem[:3], file=fout2)
        if (elem[:11] == 'DisplayName'):
            name = elem[13:-1]
        if (elem[:3] == 'Age'):
            age = elem[5:-1]
            age = int(age)
            print(age)

    if ((19 > age) or (age > 26) or (name == '')):
        continue

    x = User()
    x.new_user(name, age)
    users.append(x)

print(len(users), file=fout3)

#for i in range(100):
#    s = f_users.readline()
#    print(s, file=fout)