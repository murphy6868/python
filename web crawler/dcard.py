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

