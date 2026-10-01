"""Lectura de la estructura HTML de la exportación local de Facebook."""
from html.parser import HTMLParser
from datetime import datetime, timedelta, timezone
import re

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
BLOCK = {'div','section','p','h1','h2','h3','tr','td','footer','header','li','br','main'}
MONTHS = {'ene':1,'jan':1,'enero':1,'feb':2,'febrero':2,'mar':3,'marzo':3,'abr':4,'apr':4,'abril':4,
          'may':5,'mayo':5,'jun':6,'junio':6,'jul':7,'julio':7,'ago':8,'aug':8,'agosto':8,
          'sep':9,'sept':9,'septiembre':9,'oct':10,'octubre':10,'nov':11,'noviembre':11,'dic':12,'dec':12,'diciembre':12}
DATE = re.compile(r'\b('+'|'.join(MONTHS)+r')\s+(\d{1,2}),\s*(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})\s*([ap])\s*\.?\s*m\.?',re.I)
LONG_DATE = re.compile(r'\b(\d{1,2})\s+de\s+('+'|'.join(MONTHS)+r')\s+de\s+(\d{4})\s+a las?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([ap])\s*\.?\s*m\.?',re.I)


class Node:
    def __init__(self,tag='root',attrs=None,parent=None,pos=None):
        self.tag=tag;self.attrs=attrs or {};self.parent=parent;self.children=[];self.pos=pos
    def nodes(self,tag=None):
        for c in self.children:
            if isinstance(c,Node):
                if tag is None or c.tag==tag:yield c
                yield from c.nodes(tag)
    def text(self):
        if self.tag in ('style','script'):return ''
        s=''.join(c.text() if isinstance(c,Node) else c for c in self.children)
        return '\n'+s+'\n' if self.tag in BLOCK else s
    def clean(self):return '\n'.join(s.strip() for s in self.text().splitlines() if s.strip())
    def has_class(self,name):return name in self.attrs.get('class','').split()
    def find(self,tag=None,cls=None):
        return next((n for n in self.nodes(tag) if cls is None or n.has_class(cls)),None)


class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(text)
    def handle_starttag(self,tag,attrs):
        n=Node(tag,dict(attrs),self.stack[-1],self.getpos());self.stack[-1].children.append(n)
        if tag not in VOID:self.stack.append(n)
    def handle_startendtag(self,tag,attrs):
        self.stack[-1].children.append(Node(tag,dict(attrs),self.stack[-1],self.getpos()))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];return
    def handle_data(self,data):self.stack[-1].children.append(data)
    @property
    def title(self):
        n=self.root.find('title');return n.clean() if n else ''
    @property
    def links(self):
        return [(n.attrs['href'],n.clean(),n.pos) for n in self.root.nodes('a') if n.attrs.get('href')]
    def tables(self):
        for n in self.root.nodes('table'):
            rows={}
            for row in n.children:
                if not isinstance(row,Node) or row.tag!='tr':continue
                cells=[c for c in row.children if isinstance(c,Node) and c.tag in ('td','th')]
                if len(cells)==2:rows[cells[0].clean()]=cells[1].clean()
                elif len(cells)==1:
                    parts=cells[0].clean().splitlines()
                    if parts and parts[0] in ('Recibida el','Creado el','Fecha','Fecha y hora'):
                        rows[parts[0]]='\n'.join(parts[1:])
            yield n,rows


def facebook_date(s):
    s=s.replace('\u202f',' ').replace('\xa0',' ')
    match=DATE.search(s)
    if match:month,day,year,hour,minute,second,ap=match.groups()
    else:
        match=LONG_DATE.search(s)
        if not match:return None
        day,month,year,hour,minute,second,ap=match.groups();second=second or '0'
    return datetime(int(year),MONTHS[month.lower()],int(day),int(hour)%12+(12 if ap.lower()=='p' else 0),
                    int(minute),int(second),tzinfo=timezone(timedelta(hours=-6)))
