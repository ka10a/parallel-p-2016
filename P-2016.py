from zipfile import ZipFile
import codecs


fout = open("top-of-150-users.html", "w", encoding='utf-8')
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')
f_style_temp = open("style_template.txt", "r")
f_table_temp = open("table_template.txt", "r")
f_table_end = open("table_end.txt", "r")


class User:
    displayname = ''
    age = None
    id = None
    comm = 0
    link = ''

    def new_user(self, name, age, _id, link):
        self.displayname = name
        self.age = age
        self.id = _id
        self.link = link
        self.comm = 0


def del_space(s):
    a = []
    i = 0
    while i < len(s):
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
        _id = None
        link = ''

        for elem in a:
            if elem.startswith('Id'):
                _id = elem[4:-1]

                if _id.isdigit():
                    _id = int(_id)
                else:
                    _id = None
                    break

            if elem.startswith('DisplayName'):
                name = elem[13:-1]

            if elem.startswith('WebsiteUrl'):
                link = elem[12:-1]

            if elem.startswith('Age'):
                age = elem[5:-1]

                if age.isdigit():
                    age = int(age)
                else:
                    age = None
                    break

        if (name == '') or (age is None) or (_id is None):
            continue

        if (20 <= age) and (age <= 25):
            new = User()
            new.new_user(name, age, _id, link)
            users[_id] = new

    #print(len(users))
    return users


def read_comments(users):
    for s in f_comm.readlines():
        a = del_space(s)
        _id = 0

        for elem in a:
            if elem.startswith('UserId'):
                _id = int(elem[8:-1])

        if _id in users:
            users[_id].comm += 1

    return users


def generate_table(users, rate):
    fout.write(f_style_temp.read())
    fout.write(f_table_temp.read())

    for i in range(150):
        table_user = User()
        table_user = users[rate[i][1]]
        print("<tr>", file=fout)
        print("<th>{0}</th>".format(i + 1), file=fout)
        if table_user.link != "":
            print("<th> <a href='{0}'</a>".format(table_user.link),  table_user.displayname, "</th>", sep='', file=fout)
        else:
            print("<th>{0}</th>".format(table_user.displayname), file=fout)
        print("<th>{0}</th>".format(table_user.age), file=fout)
        print("<th>{0}</th>".format(table_user.comm), file=fout)
        print("</tr>", file=fout)

    fout.write(f_table_end.read())


_users = read_comments(read_users())

_rate = []
for _id in _users.keys():
    _rate.append((_users[_id].comm, int(_id)))
_rate.sort(reverse=True)

generate_table(_users, _rate)



