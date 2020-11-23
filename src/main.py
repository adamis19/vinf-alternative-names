import csv
import re

title_count = 0
redirect_count = 0
actual_title = 0
read_next_line = False
is_redirect = False
is_disambiguation = False
disambiguation_count = 0
disambiguation_alt_names = 0
redirect2_alt_names = 0
redirect_alt_names = 0
alt_names = {}

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

    # if revision tag is found and is_redirect and is_disambiguation is False, it means that actual page is normal page
    if re.search("<revision", tag):
        if not is_redirect and not is_disambiguation:
            alt_names.setdefault(actual_title, [])

    if is_disambiguation:
        process_disambiguation(tag)


# function parses title of page
def get_title(title: any):
    global actual_title
    global is_disambiguation
    global disambiguation_count

    title = re.findall(">.*<", title)
    actual_title = title[0][1:-1]
    is_disambiguation = False
    if re.search("(disambiguation)", actual_title, re.IGNORECASE):
        is_disambiguation = True
        disambiguation_count += 1


def process_disambiguation(name):
    global disambiguation_alt_names

    # if line on disambig page begins with '*'
    if re.search("^\*", name, re.IGNORECASE):
        # find text behind ']],'
        alt_name = re.findall("]],.*$", name, re.IGNORECASE)
        if alt_name:
            alt_name = alt_name[0][4:]
            # if text is shorter than 5 words
            if len(alt_name.split()) < 5:
                # get text between parenthesis and store
                name = re.findall("\[\[.*]]", name, re.IGNORECASE)[0][2:-2]
                alt_names.setdefault(name, []).append(alt_name)
                disambiguation_alt_names += 1


# function catches  {{redirect2|AD|Before Christ}}  type of redirect
def get_redirects(tag: any):
    global redirect2_alt_names

    redirects = re.findall("redirect2|.*|", tag, re.IGNORECASE)

    if redirects:
        split = redirects[0].split("|")

        # add all alternative names from redirect2
        for s in split:
            if re.search("redirect2", s, re.IGNORECASE):
                continue
            if s not in REDIRECT_STOP and not re.search("disambiguation", s) and not re.search("other uses", s):
                alt_names.setdefault(actual_title, []).append(s)
                redirect2_alt_names += 1
            else:
                break


# this function catches  <redirect title="Alpha particle" />  type of redirect
def get_redirect_title(redirect_title: any):
    global alt_names
    global redirect_alt_names

    # if there is a small letter before a capital letter, do not save
    if not re.search("[^A-Z]+[^\\s][A-Z]", actual_title):
        redirect_title = re.findall("\".*\"", redirect_title)
        redirect_title = redirect_title[0][1:-1]
        alt_names.setdefault(redirect_title, []).append(actual_title)
        redirect_alt_names += 1


wikipedia = open('../../data/wikipedia.xml', 'r', encoding="utf-8", errors='ignore')
wiki_out = open('../wiki_out.xml', 'w', encoding="utf-8", errors='ignore')
w = csv.writer(open("../alternative_names.csv", "w", encoding="utf-8"), delimiter='\t', lineterminator='\n')

# 10 000 000 lines is cca 1 GB
for i in range(50000000):
    line = wikipedia.readline()
    find_string(line)
    wiki_out.write(line)
    if i % 1000000 == 0:
        print(i)

print("writing to file...")

print("titles =", title_count)
print("redirects =", redirect_count)
print("number of disambiguation pages = ", disambiguation_count)

print(len(alt_names), " names ")
print(disambiguation_alt_names, "alt names from disambig")
print(redirect_alt_names, "alt names from redirect")
print(redirect2_alt_names, "alt names from redirect2")

print("finding the most alternative names..")
maxLength = 0
for key, val in alt_names.items():
    w.writerow([key, val])
    if len(val) > maxLength:
        maxLength = len(val)
        name = key

print("The most alternative names(", maxLength, "): ", name, alt_names[name])
wikipedia.close()
wiki_out.close()

