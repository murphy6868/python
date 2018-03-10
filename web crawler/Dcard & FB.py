

from dcard import Dcard
target = '女友'
def hot(metas):
    return [m for m in metas if target in m['tags']]
d=Dcard()
f=d.forums('photography') # 攝影版
m=f.get_metas(num=50,callback=hot) #list
p=d.posts(m).get(comments=False,links=False)
r=p.parse_resources() #list: try r[0][1]
done,fails=p.download(r)
print('Got %d pics' % done if len(fails)==0 else 'Error!')




import json
import facebook
token='EAACEdEose0cBAJA4F8bZCZBOWjN6DO98mE1VfmAbEvcBbvcc51cZCnd32T7hE8T9ja8dup9GHeBAtVXpUBiXE3qmWjgrDP1QhQw7MzvU243pFXiTHba0Wyt6Cr0Nm7aSGTefIrYPUqSiXnAOIiUQZAaZAJIHBMN5dAdObZAlnETbzb6mUGU479loRkC3Nyox8ZD' 
graph=facebook.GraphAPI(token)

data = graph.get_object('me/friends')
#print(data)
num = 0
month = [0]*13
for j in range(len(data['data'])):
    ids = data['data'][j]['id']
    fdata = graph.get_object(ids, fields='birthday, name')
    #print(fdata)
    q = fdata.setdefault('birthday', '123')
    if len(q) > 3:
        num = num + 1
        t = 0
        t = int(q[0])*10 + int(q[1])
        month[t] = month[t] + 1
        #print(t)
print('自己的朋友總數 =', data['summary']['total_count'])
print('有透露生日的朋友數目 =', num)
print('各個出生月的人數 :')
for j in range(12):
    print(j+1, '月',month[j+1], '人')