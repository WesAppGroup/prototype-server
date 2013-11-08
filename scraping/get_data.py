from xml.dom import minidom
import urllib2
from bs4 import BeautifulSoup
import datetime
import re
from operator import itemgetter, attrgetter

# def time_parser(time_string):
#     x_to_z = re.compile('[\d]{2}(am|pm).*[\d]{1,2}(am|pm)')
#     c1 = x_to_z.findall(p1,re.I)
#     print c1
#     if c1:
#         time = c1[0]
#         first = re.compile('[\d]{1,2}')
#         start = int(first.findall(time)[0])
#         print start
#         am_pm = re.compile('(am|pm)')
#         to_24 = am_pm.findall(time)[0]
#         if to_24 == 'pm':
#             start += 12

#         end = re.compile

#         #make sure to handle an event that has an AM that goes to the next day
#         #handle 10:XX - YY:ZZ
#         print time


# identifiers = {"date":["Date:"],"time":["Time:"],"place":["Place:"]}

# import get_data;get_data.content_parser()

# def unicode_hack(unicodey_string):
#     """gets all unicode shit out of a string. Hackily"""
#     word = ""
#     for i in unicodey_string:
#         if len(i) == 1:

#             word += i
#     return word

def content_parser(content,identifiers):
    """
    Content is a list of words and identifiers is a dict of lists
    """


    ########ADD FILTERING TO GRAB EVENTS ONLY ###########
  
    # content = [u'1962.', u'USA.', u'Dir:', u'John', u'Ford.', u'With', u'James', u'Stewart,', u'John', u'Wayne.', u'123', u'min.', u'In', u'a', u'town', u'terrorized', u'by', u'the', u'titular', u'outlaw,', u'an', u'educated', u'lawyer', u'and', u'an', u'individualistic', u'frontiersman', u'strike', u'up', u'uneasy', u'friendship', u'in', u'the', u'name', u'of', u'peace', u'and', u'progress.', u'Western', u'master', u'Ford', u'uses', u'flashbacks', u'to', u'detail', u'a', u'thrilling,', u'cynically', u'self-reflexive', u'commentary', u'on', u'American', u'mythology.', u'Tonight.', u'8pm.', u'Goldsmith', u'Family', u'Cinema.', u'Free.']
    # content = [u'\n', u'From ', u'Keenan Burgess\u201916', u':', u'\n', u'Electronic up-and-comer ', u'Druid Cloak\u2019s', u' coming to Psi U this Saturday for the first party/concert of the fall semester. Wes\u2019 own Ron Beatz and cone+ will be opening.', u'\n', u'Date:', u' Sat, Sept 7', u'\n', u'Time: \xa0', u'9 pm- 2 am', u'\n', u'Place:', u' Psi U', u'\n', u'Cost:', u' FREE', u'\n', u'FB Event.', u'\n']

    info_list = []
    index = 0
    for word in content:
        # print word,"I AM THE WORD"
        for i in identifiers.keys():
            # curr_list = []
            try:
                word = str(word)
                # print word,len(word)
            except:
                try:
                    # print word,"PROBLEM HERE",len(word)
                    word = word.split()[0]
                    # print word,"w1"
                except:
                    #some random instances of unicode weird things.
                    pass 
            e = [str(z) for z in identifiers[i]]
            # print e,"EEEEEEEEEEE",word
            for t in e:
                # print t,word,t in word
                # print len(t),len(word)
                # print [t,word]
                if t in word:
                    # print "MATCH for ",word
                    info_list.append((word,index))
                    break
            # if curr_list:
            #     info_list.append(curr_list)
        index += 1
    if info_list:
        return info_list

def content_builder(content,identifiers,matches):
    """
    Builds list of associated content from list based on given subset/indexes of matches 
    """
    # identifiers = {"date":["Date:"],"time":["Time:"],"place":["Place:","Place"]}
    inverse_dict = {}
    for i in identifiers:
        for z in identifiers[i]:
            inverse_dict[z] = i

    # print inverse_dict,"INVERSE"

    #sort matches by index ascending
    matches = sorted(matches,key=itemgetter(1))
    # print matches,"matches"

    #iterating through the matches and building up a list of words that 
    #occur before the next match item. If no next match, grab everything
    #until end.
    event = {}
    index = 0
    for m in matches:
        if m[0] in inverse_dict:
            try:
                stop = matches[index+1][1]
                words = [word for word in content[m[1]+1:stop]]
                # print words,"words"
            except:
                words = [word for word in content[m[1]+1:]]
                # print words,"words"
            event[inverse_dict[m[0]]] = words
        index += 1

    return event



# import get_data;a = get_data.xml_parser()
def get_xml():
    xml = urllib2.urlopen("http://wesleying.org/feed/")
    dom = minidom.parse(xml)
    items = dom.getElementsByTagName('item')
    return items

def only_events(posts):
    """
    Goes through the category elements in each post and looks
    for an "event"-like tag. Returns false if no event tag is found.
    """
    categories = []
    actual_events = []
    for post in posts:
        cats = post.getElementsByTagName('category')
        for c in cats:
            categories.append(c.childNodes[0].data)
            if "event" in c.childNodes[0].data.lower():
                if post not in actual_events:
                    actual_events.append(post)
            
    return actual_events,categories



"""
FOR WESLEYING. Wes events is a little diff, they don't give tags/categories
in the feed. Could scrape the site every time we update since they
do give a link to the page which does have tags? Could talk to them too.

Idea:::: could create some lists of possible tags for certain 
categories in order to identify what kind of event each item is.
For example, music identifiers could be 
    [concert, band, a capella, ...]
Can look through the categories/gather some data to figure out
what these would be. WANT categories so that we can have
colored pins on the map and for filtering/searching purposes.
Could go through all the categories and figure out which cat best fits,
do some sort of max matches = category thing. Could also use description
as context for guessing but that gets a little more complicated. Might 
also be worth just talking to Wesleying people and asking them to 
put in some more generalized categories in their feed. Also better locations.
"""

cats_tags = {
'Film':['film','movie','film series'],
'Auditions':['auditions','seek','try','out'],
'Theater':['play','see','92','theater','stage','second'],
'Performances':['dance','slam','poetry','reading','mic','open'],
'Student Groups':['cause','education','meeting','food','student','group',
    'student group','queer','?','community','club','sustain','environment',
    'help','civic','engage','art'],
'Sports':['football','soccer','baseball','swimming','lacross','basketball',
    'softball','varsity','tennis'],
'Admissions':[],
'Other':[]
}

def xml_parser():
    """FOR WESLEYING"""
    all_items = get_xml()
    events = []
    items = only_events(all_items)[0]
    for i in items:
        # print i,"ITEM"
        title = i.getElementsByTagName('title')[0].childNodes[0].data
        url = i.getElementsByTagName('link')[0].childNodes[0].data
        description = i.getElementsByTagName('description')[0].childNodes[0].data
        content_html = i.getElementsByTagName('content:encoded')[0].childNodes[0].data
        parsed_content = BeautifulSoup(content_html)
        # print parsed_content
        try:
            full_description = parsed_content.find('blockquote').text
        except:
            full_description = ""
        # info = parsed_content('p')[3]
        # print info,"INFO"
        # times = ['time']
        # dates = ['date']
        # locations = ['place','where?','location','where']

        event_location = ""
        event_time = ""
        event_date = ""
        # info_str = str(info).lower()
        # print info_str,"INFO STR"
        # print times
        # for t in times:
        #   print t
        #   if t in info_str:
        #       c = re.compile(t+'.*?<.*?<',re.I)
        #       p = c.findall(info_str)[0]
        #       print p,"P!!!!!!!1"
        #       c2 = re.compile('>.*<')
        #       p2 = c2.findall(p)[0][1:-1]
        #       print p2,"P2!!!!!"
        #       event_time = ""
        #       break

        # for t in dates:
        #   if t in info_str:
        #       event_date = t
        #       break

        # for t in locations:
        #   if t in info_str:
        #       event_location = t
        #       break

        # print event_location,event_time,event_date,"Stuff"
        identifiers = {"date":["Date:"],"time":["Time:","Time"],"place":["Place:","Place"]}
        soup = BeautifulSoup(content_html)
        # print '\/n',soup,"SOOOOOOOOOOUP"
        # print "CONTENT",content_html,"END CONTENT"
        content = soup.get_text('|').split('|')
        # print content,"CONTENT"
        # print info,"INFO"
        match = content_parser(content,identifiers)
        if match:
            ##DO MORE THINGS
            built = content_builder(content,identifiers,match)
            # print built
            if built.get("place"):
                event_location = built.get("place")
            if built.get("time"):
                event_time = built.get("time")
            if built.get("date"):
                event_date = built.get("date")  

            event = {"title":title,"url":url,"description":description,
                "location":event_location,"time":event_time,
                "date":event_date,"full_description":full_description}
        else:
            event = {"title":title,"url":url,"description":description,
                "location":event_location,"time":event_time,
                "date":event_date,"full_description":full_description}

        #HOW THE HELL DO I DO MULTIPLE OPTIONS...
        # p1 = re.compile('Place:.*</p>')
        # p2 = re.compile('WHERE?:.*</p>')

        # z = p1.findall(parsed_content)
        # w = re.compile('>.*<')
        # w.findall(z)[0][1:-1]

        #Check to see if stuff is in the database?

        # event = {"title":title,"url":url,"description":description,
        #         "location":event_location,"time":event_time,
        #         "date":event_date}

        # events.append(event)
        events.append(event)

    return events
