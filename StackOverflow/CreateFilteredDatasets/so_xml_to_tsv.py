#
# This script filters the posts and keeps those posts that are or belong
# to a question that has been asked in 2011 or 2012.
#

import os
import re
try:
    import ujson as json  # UltraJSON if available
except:
    import json
from dateutil import parser as dateparser

from operator import itemgetter
from xml.etree import cElementTree as etree
from collections import defaultdict

from data import DATA_DIR


#filename = os.path.join(DATA_DIR, "posts-2011-12.xml")
filename = os.path.join(DATA_DIR, "stackoverflow.com-Posts")
filename_filtered = os.path.join(DATA_DIR, "filtered.tsv")

q_creation = {}  # creation datetimes of questions
q_accepted = {}  # id of accepted answer

meta = defaultdict(
    list)  # question -> [(answer Id, IsAccepted, TimeToAnswer, Score), ...]

# regegx to find code snippets
code_match = re.compile('<pre>(.*?)</pre>', re.MULTILINE | re.DOTALL)
link_match = re.compile(
    '<a href="http://.*?".*?>(.*?)</a>', re.MULTILINE | re.DOTALL)
img_match = re.compile('<img(.*?)/>', re.MULTILINE | re.DOTALL)
tag_match = re.compile('<[^>]*>', re.MULTILINE | re.DOTALL)


def filter_html(s):
    num_code_lines = 0
    link_count_in_code = 0
    code_free_s = s

    num_images = len(img_match.findall(s))

    # remove source code and count how many lines
    for match_str in code_match.findall(s):
        num_code_lines += match_str.count('\n')
        code_free_s = code_match.sub("", code_free_s)

        # sometimes source code contain links, which we don't want to count
        link_count_in_code += len(link_match.findall(match_str))

    anchors = link_match.findall(s)
    link_count = len(anchors)

    link_count -= link_count_in_code

    html_free_s = re.sub(
        " +", " ", tag_match.sub('', code_free_s)).replace("\n", "")

    link_free_s = html_free_s
    for anchor in anchors:
        if anchor.lower().startswith("http://"):
            link_free_s = link_free_s.replace(anchor, '')

    num_text_tokens = html_free_s.count(" ")

    return link_free_s, num_text_tokens, num_code_lines, link_count, num_images

years = defaultdict(int)
num_questions = 0
num_answers = 0


def print_file(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        with open(os.path.join(DATA_DIR, "sample.txt"), "w") as o:
            for i in range(100):
               o.write( f.readline())




def testParse(filename):

    it = etree.iterparse(os.path.join(DATA_DIR, filename), events=("start","end"))
    root = it.next()
    path= []
    for event, elem in it:
        if event == 'start':
            path.append(elem.tag)
        elif event == 'end':
            if elem.tag == 'row':
                 print elem.get('CreationDate')

            # process the tag
            if elem.tag == 'name':
                if 'members' in path:
                    print 'member'
                else:
                    print 'nonmember'
            path.pop()



def parsexml(filename):
    global num_questions, num_answers

    counter = 0
    it = etree.iterparse(os.path.join(DATA_DIR, filename), events=("start","end"))

    for event, elem in it:
        if event == 'end':
            if counter % 100000 == 0:
                print(counter)

            counter += 1

            if elem.tag == 'row':
                creation_date = dateparser.parse(elem.get('CreationDate'))

                # import pdb;pdb.set_trace()
                if creation_date.year < 2013:
                    continue

                Id = int(elem.get('Id'))
                PostTypeId = int(elem.get('PostTypeId'))
                Score = int(elem.get('Score'))

                if PostTypeId == 1:
                    num_questions += 1
                    years[creation_date.year] += 1

                    ParentId = -1
                    TimeToAnswer = 0
                    q_creation[Id] = creation_date
                    accepted = elem.get('AcceptedAnswerId')
                    if accepted:
                        q_accepted[Id] = int(accepted)
                    IsAccepted = 0

                elif PostTypeId == 2:
                    num_answers += 1

                    ParentId = int(elem.get('ParentId'))
                    if not ParentId in q_creation:
                        # question was too far in the past
                        continue

                    TimeToAnswer = (creation_date - q_creation[ParentId]).seconds

                    if ParentId in q_accepted:
                        IsAccepted = int(q_accepted[ParentId] == Id)
                    else:
                        IsAccepted = 0

                    meta[ParentId].append((Id, IsAccepted, TimeToAnswer, Score))

                else:
                    continue

                Text, NumTextTokens, NumCodeLines, LinkCount, NumImages = filter_html(
                    elem.get('Body'))

                elem.clear()
                values = (Id, ParentId,
                          IsAccepted,
                          TimeToAnswer, Score,
                          Text.encode('utf-8'),
                          NumTextTokens, NumCodeLines, LinkCount, NumImages)

                yield values
            elem.clear()



count = 0;
#print_file(filename)
#testParse("sample.txt")
with open(os.path.join(DATA_DIR, filename_filtered), "w") as f:
    for item in parsexml(filename):
        try:
            line = "\t".join(map(str, item))
            f.write(line.encode("utf-8") + "\n")
            count = count + 1;
        except:
            print (item)
        if ( count % 1000== 0):
            print("finished %i" % count)


with open(os.path.join(DATA_DIR, "filtered-meta.json"), "w") as f:
    json.dump(meta, f)

print("years:", years)
print("#qestions: %i" % num_questions)
print("#answers: %i" % num_answers)
