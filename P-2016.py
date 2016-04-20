from zipfile import ZipFile
import codecs
import temp


fout = open("top-of-150-users.html", "w", encoding='utf-8')
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')


class User:
    d_name = ''
    age = None
    id_ = None
    comm = 0

    def __init__(self, name, age, id_):
        self.d_name = name
        self.age = age
        self.id_ = id_
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
        id_ = None

        for elem in a:
            if elem.startswith('Id'):
                id_ = elem[4:-1]

                if id_.isdigit():
                    id_ = int(id_)
                else:
                    id_ = None
                    break

            if elem.startswith('DisplayName'):
                name = elem[13:-1]

            if elem.startswith('Age'):
                age = elem[5:-1]

                if age.isdigit():
                    age = int(age)
                else:
                    age = None
                    break

        if (name == '') or (age is None) or (id_ is None):
            continue

        if (20 <= age) and (age <= 25):
            new = User(name, age, id_)
            users[id_] = new

    return users


def read_comments(users):
    for s in f_comm.readlines():
        a = del_space(s)
        id_ = 0

        for elem in a:
            if elem.startswith('UserId'):
                id_ = int(elem[8:-1])

        if id_ in users:
            users[id_].comm += 1

    return users


def generate_table(users, rate):
    print(temp.STYLE_TEMPLATE, file=fout)
    print(temp.TABLE_TEMPLATE, file=fout)

    for i in range(150):
        table_user = users[rate[i][1]]
        print("<tr>", file=fout)
        print("<th>{0}</th>".format(i + 1), file=fout)
        print("<th> <a href='https://electronics.stackexchange.com/users/{0}'</a>".format(table_user.id_),  table_user.d_name, "</th>", sep='', file=fout)
        print("<th>{0}</th>".format(table_user.age), file=fout)
        print("<th>{0}</th>".format(table_user.comm), file=fout)
        print("</tr>", file=fout)

    print(temp.TABLE_END, file=fout)


_users = read_comments(read_users())

_rate = []
for id_ in _users.keys():
    _rate.append((_users[id_].comm, int(id_)))
_rate.sort(reverse=True)

generate_table(_users, _rate)



