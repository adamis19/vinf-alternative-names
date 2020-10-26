import re

title_count = 0
redirect_count = 0
actual_title = 0
read_next_line = False
titles = []
is_redirect = False

REDIRECT_STOP = ["other uses", "", "and"]


# this function is called in each line, it is searching for tags and strings
def find_string(tag: any):
    global title_count
    global redirect_count
    global is_redirect
    tag = tag.strip()
    if re.search("<title", tag):
        title_count += 1
        get_title(tag)
        is_redirect = False

    if re.search("redirect2", tag, re.IGNORECASE):
        get_redirects(tag)

    if re.search("<redirect", tag):
        redirect_count += 1
        title_count -= 1
        get_redirect_title(tag)
        is_redirect = True

    # if revision tag is found and is_redirect is False, it means that actual page is normal page
    if re.search("<revision", tag):
        if not is_redirect:
            exists = False
            for t in titles:
                if t[0] == actual_title:
                    exists = True
                    break
            if not exists:
                arr = [actual_title]
                titles.append(arr)


# function parses title of page
def get_title(title: any):
    global actual_title
    title = re.findall(">.*<", title)
    actual_title = title[0][1:-1]


# function catches  {{redirect2|AD|Before Christ}}  type of redirect
def get_redirects(tag: any):
    redirects = re.findall("redirect2|.*|", tag, re.IGNORECASE)

    if redirects:
        split = redirects[0].split("|")
        index = -1

        # find index of main title
        for t in titles:
            if t[0] == actual_title:
                index = titles.index(t)
                break

        # if index was not found, append new main title
        if index == -1:
            arr = [actual_title]
            titles.append(arr)
            index = len(titles - 1)

        # add all alternative names from redirect2
        for s in split:
            if re.search("redirect2", s, re.IGNORECASE):
                continue
            if s not in REDIRECT_STOP and not re.search("disambiguation", s) and not re.search("other uses", s):
                titles[index].append(s)
            else:
                break


# this function catches  <redirect title="Alpha particle" />  type of redirect
def get_redirect_title(redirect_title: any):
    redirect_title = re.findall("\".*\"", redirect_title)
    redirect_title = redirect_title[0][1:-1]
    exists = False

    # if redirect title already exists, only append alternative name
    for t in titles:
        if t[0] == redirect_title:
            exists = True
            titles[titles.index(t)].append(actual_title)
            break

    # if not, create new main title on the end of list and append alternative name
    if not exists:
        arr = [redirect_title]
        titles.append(arr)
        titles[len(titles) - 1].append(actual_title)


wikipedia = open('../../data/wikipedia.xml', 'r', encoding="utf-8", errors='ignore')
wiki_out = open('../wiki_out.xml', 'w', encoding="utf-8", errors='ignore')
alternative_names = open('../alternative_names.txt', 'w', encoding="utf-8", errors='ignore')

for i in range(1000000):
    line = wikipedia.readline()
    # print(line)
    find_string(line)
    wiki_out.write(line)
    if i % 1000000 == 0:
        print(i)

print("writing to file...")

names = 0
for t in titles:
    for r in t:
        alternative_names.write(r)
        alternative_names.write(", ")
        names += 1
    alternative_names.write("\n")

print("number of names: ", names)
print("titles =", title_count)
print("redirects =", redirect_count)

wikipedia.close()
wiki_out.close()
alternative_names.close()
