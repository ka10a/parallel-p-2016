from zipfile import ZipFile
import codecs

class User:
    displayname = ''
    age = -1
    id = -1
    comm = 0
    link = ''
    def new_user(self, name, age, id, link):
        self.displayname = name
        self.age = age
        self.id = id
        self.link = link
        self.comm = 0

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

fout = open("top-of-150-users.html", "w", encoding='utf-8')
#fout2 = open("test2.txt", "w")
#fout3 = open("test3.txt", "w")
#fout4 = open("test4.txt", "w")
#fout5 = open("test5.txt", "w")
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')
#f_links = codecs.open('Posts.xml', encoding='cp1251')
# 'cp1251')

users = {}
for s in f_users.readlines():
#for i in range(100):
    #s = f_users.readline()
    #print(s, file=fout3)
    a = del_space(s)
    name = ''
    age = -1
    id = -2
    link = ''
    #print(a, file=fout2)
    for elem in a:
        #print(elem[:3], file=fout2)
        #print(elem)
        if (elem[:2] == 'Id'):
            id = elem[4:-1]
            if (id.isdigit()):
                id = int(id)
            else:
                #print(s, file=fout)
                id = -2
                break
            #print(id)
        if (elem[:11] == 'DisplayName'):
            name = elem[13:-1]
        if (elem[:10] == 'WebsiteUrl'):
            link = elem[12:-1]
        if (elem[:3] == 'Age'):
            age = elem[5:-1]
            #print(age, file=fout2)
            #print(age.isdigit(), file=fout2)
            if (age.isdigit()):
                age = int(age)
            else:
                age = -1
                break
            #print(age, file=fout2)

    if ((name == '') or (age == -1) or (id == -2)):
        continue

    #print(age)

    if (20 <= age) and (age <= 25):
        x = User()
        x.new_user(name, age, id, link)
        users[id] = x

print(len(users))
#print(len(users), file=fout3)
#for elem in users:
#    print(elem.age, file=fout3)

#for i in range(100):
    #s = f_users.readline()
    #print(s, file=fout)

#print(len(users))

for s in f_comm.readlines():
    a = del_space(s)
    id = 0
    for elem in a:
        if (elem[:6] == 'UserId'):
            id = int(elem[8:-1])
    if id in users:
        users[id].comm += 1

rate = []
for id in users.keys():
    #print(id, file=fout2)
    rate.append((users[id].comm, int(id)))
rate.sort(reverse=True)

print('<style type="text/css">', file=fout)
print('table {', file=fout)
print('border-collapse: collapse;', file=fout)
print('}', file=fout)
print('table th,', file=fout)
print('table td {', file=fout)
print('padding: 0 10px;', file=fout)
print('}', file=fout)
print('table.brd th,', file=fout)
print('table.brd td {', file=fout)
print('border: 1px solid #000;', file=fout)
print('}', file=fout)
print('div', file=fout)
print('{', file=fout)
print('background-color: white;', file=fout)
print('border-radius: 20px;', file=fout)
print('font-family: "Georgia", serif;', file=fout)
print('paddind-top: 10px;', file=fout)
print('padding-bottom: 10px;', file=fout)
print('}', file=fout)
print('body {background-color: aliceblue;}', file=fout)
print('</style>', file=fout)
print('<body style="padding: 0 20%">', file=fout)
print('<div style="padding: 0 18%">', file=fout)
print('<h1 style="padding: 0 20%">Top of 150 users</h1>', file=fout)
print('<table>', file=fout)
print('<tr>', file=fout)
print('<th>#</th>', file=fout)
print('<th>DisplayName</th>', file=fout)
print('<th>Age</th>', file=fout)
print('<th>Comments</th>', file=fout)
#print('<th></th>', file=fout)
#print('<th></th>', file=fout)
#print('<th></th>', file=fout)
print('</tr>', file=fout)

for i in range(150):
    x = User()
    x = users[rate[i][1]]
    print('<tr>', file=fout)
    print('<th>', i + 1, '</th>', sep='', file=fout)
    if (x.link > ''):
        print('<th>','<a href=', "'",  x.link, "'", '</a>',  x.displayname, '</th>', sep='', file=fout)
    else:
        print('<th>',  x.displayname, '</th>', sep='', file=fout)
    print('<th>', x.age, '</th>', sep='', file=fout)
    print('<th>', x.comm, '</th>', sep='', file=fout)
    print('</tr>', file=fout)

print('</table>', file=fout)
print('</div>', file=fout)
print('</body>', file=fout)