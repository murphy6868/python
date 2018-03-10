import re
tweets=['RT @spiketren No class tomorrow',
'No class tomorrow (via @spiketren)']
#rt=re.compile('(RT|via) (@\w+)')
#rt=re.compile('(RT|\(via) (@\w+\)*)')
rt=re.compile('(RT|\(via) (@\w+\)*)')
for t in tweets:
    m=rt.search(t)
    t = t.replace(m.group(0), "")
    #print(m.group(0))
    #print(m.group(1))
    #print(m.group(2))
    if t[0] == ' ': t = t[1:len(t)]
    if t[len(t)-1] == ' ': t = t[0:len(t)-1]
    print(t)
    
#########################################################


import urllib, lxml.html
u='https://www.csie.ntu.edu.tw/members/teacher.php?mclass1=110'
r=urllib.request.Request(u,headers={'User-Agent':''})
data=urllib.request.urlopen(r).read()
t=lxml.html.fromstring(data.decode('utf-8'))

for link in t.xpath('//script'): 
    if type(link.text) == str and len(link.text) > 30:
        a = link.text
        a = a[a.index('l[0]'):a.index('for')]
        #print('=='*30)
        #print(a)
        filt = re.compile('l\[\d+\]=\'[^\']+\'')
        out = filt.findall(a)
        #print(out)
        total = ""
        for j in out:
            p0 = j.index('\'')
            p0 = p0 + 1
            p1 = j.index('\'', p0)
            cut = j[p0:p1]
            if cut[0] == '|':
                cut = cut.replace('|', '')
                cut = chr(int(cut))
            total = cut + total
            
        p3 = total.index(':')
        p3 = p3 + 1
        p4 = total.index('"', p3)
        print(total[p3:p4])