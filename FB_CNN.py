import urllib, lxml.html
import facebook
import pandas as pd
token='EAACEdEose0cBAPOjobYEt5jmOkaXX30XIgZBxQ7kLEgTgVS90UpOQZCEyHH3ecKa72gSZBqIgT1PdKcTbRukxcB1ntdk8ZAah3XdPucNBNAP6cmiRLMkPuZCnFWGZAHZCB2E2bYCi78pGBaZCZANMegNCLuAy55gDzjnKwEemlajCLpA5ighajhleiNqmRsgWDFQZD' 
graph = facebook.GraphAPI(access_token=token, version='2.6')
post_limit = 14
reaction_limit = 2000

def str_contain(string, target):
    if string.find(target) == -1:
        return 0
    else:
        return 1

def search_data(target, date):
    data = graph.get_object(target)
    information_list = []
    for news in data['data']:
        info = []
        u = news['link']
        if str_contain(u, "videos") or str_contain(u, "photos"): 
            continue
        r=urllib.request.Request(u,headers={'User-Agent':''})
        d=urllib.request.urlopen(r).read()
        t=lxml.html.fromstring(d.decode('utf-8'))
        for title in t.xpath('//title'): 
                #print("link: ", u)
                info.append(u)
                #print("title : " + title.text)
                info.append(title.text)
        contents = ""
        for content in t.xpath('//p/text()'):
            if content[0:7] == "Updated" or content[0:9] == "Chat with" or content[0:11] == 'Set edition':
                continue
            contents += content
            #print("內文 : " + content)
        info.append(contents)
        like = 0
        love = 0
        haha = 0
        wow = 0
        sad = 0
        angry = 0
        j = 0
        for j in range(len(news['reactions']['data'])):
            #print(j, news['reactions']['data'][j].keys(), news['id'])
            if 'type' in news['reactions']['data'][j]:
                if news['reactions']['data'][j]['type'] == 'LIKE' :
                    like += 1
                elif news['reactions']['data'][j]['type'] == 'LOVE' :
                    love += 1
                elif news['reactions']['data'][j]['type'] == 'HAHA' :
                    haha +=+ 1
                elif news['reactions']['data'][j]['type'] == 'WOW' :
                    wow += 1
                elif news['reactions']['data'][j]['type'] == 'SAD' :
                    sad += 1
                elif news['reactions']['data'][j]['type'] == 'ANGRY' :
                    angry += 1
            else:
                print(-1)
        info.append(like)
        info.append(love)
        info.append(haha)
        info.append(wow)
        info.append(sad)
        info.append(angry)
        info.append(j + 1)
        information_list.append(info)
    information_df = pd.DataFrame(information_list, columns=['link', 'title', 'content', 'like', 'love',
                                                             'haha', 'wow', 'sad', 'angry',
                                                             'total(limit='+ str(reaction_limit) +')'])
    date = date[7:]
    date += '.csv'
    information_df.to_csv(date)
    
for y in range(2016, 2018):
    for m in range(1, 13):
        for d in range(7, 29, 7):
            date = '&until=' + str(y) + '-' + str(m) + '-' + str(d)
            print(date)
            target = '5550296508/posts?fields=link,created_time,id,reactions.limit('+ str(reaction_limit) +')&limit='+ str(post_limit) + date
            search_data(target, date)