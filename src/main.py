import re
title_count = 0
redirect_count = 0
actual_title = 0


def find_string(tag: any):
    global title_count
    global redirect_count
    tag = tag.strip()
    if re.search("<title", tag):
        title_count += 1
        # print(tag)
        get_title(tag)

    if re.search("<redirect", tag):
        redirect_count += 1
        title_count -= 1
        get_redirect_title(tag)


def get_title(title: any):
    global actual_title
    title = re.findall(">.*<", title)
    actual_title = title[0][1:-1]
    # print(actual_title)


def get_redirect_title(redirect_title: any):
    redirect_title = re.findall("\".*\"", redirect_title)
    redirect_title = redirect_title[0][1:-1]
    # print(actual_title, "--->",  redirect_title)


wikipedia = open('../data/wikipedia.xml', 'r', encoding="utf-8", errors='ignore')
wiki_out = open('../wiki_out.xml', 'w', encoding="utf-8", errors='ignore')
for i in range(10000000):
    line = wikipedia.readline()
    find_string(line)
    wiki_out.write(line)
    if i % 1000000 == 0:
        print(i)

print("titles =", title_count)
print("redirects =", redirect_count)
