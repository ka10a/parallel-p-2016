from zipfile import ZipFile
import codecs


fout = open("top-of-150-users.html", "w", encoding='utf-8')
#fout2 = open("test2.txt", "w")
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')


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


def read_users():
    users = {}
    for s in f_users.readlines():
        a = del_space(s)
        name = ''
        age = None
        id = None
        link = ''

        for elem in a:
            if (elem.startswith('Id')):
                id = elem[4:-1]

                if (id.isdigit()):
                    id = int(id)
                else:
                    id = -2
                    break

            if (elem.startswith('DisplayName')):
                name = elem[13:-1]

            if (elem.startswith('WebsiteUrl')):
                link = elem[12:-1]

            if (elem.startswith('Age')):
                age = elem[5:-1]

                if (age.isdigit()):
                    age = int(age)
                else:
                    age = -1
                    break

        if ((name == '') or (age is None) or (id is None)):
            continue

        if (20 <= age) and (age <= 25):
            x = User()
            x.new_user(name, age, id, link)
            users[id] = x

    #print(len(users))
    return users


def read_comments(users):
    for s in f_comm.readlines():
        a = del_space(s)
        id = 0

        for elem in a:
            if (elem.startswith('UserId')):
                id = int(elem[8:-1])

        if id in users:
            users[id].comm += 1

    return users


def generate_table(users, rate):
    print("""
        <style type="text/css">
        table
        {
        border-collapse: collapse;
        }
        table th,
        table td {
        padding: 0 10px;
        }
        table.brd th,
        table.brd td {
        border: 1px solid #000;
        }
        div
        {
        background-color: white;
        border-radius: 20px;
        font-family: "Georgia", serif;
        paddind-top: 10px;
        padding-bottom: 10px;,
        }
        body {background-color: aliceblue;}
        </style>
        <body style="padding: 0 20%">
        <div style="padding: 0 18%">
        <h1 style="padding: 0 20%">Top of 150 users</h1>
        <table>
        <tr>
        <th><h3>#</h3></th>
        <th><h3>DisplayName</h3></th>
        <th><h3>Age</h3></th>
        <th><h3>Comments</h3></th>
        </tr>
        """, file=fout)

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

    print("""
        </table>
        </div>
        </body>
        """, file=fout)


users = read_comments(read_users())

rate = []
for id in users.keys():
    rate.append((users[id].comm, int(id)))
rate.sort(reverse=True)

generate_table(users, rate)



