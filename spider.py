# -*- coding: utf-8 -*-
__author__ = 'kingdee'
import requests;
from lxml import html;
import  re;
# httpconnetion
#获得历史快照信息
def urls():
    page = requests.get("https://coinmarketcap.com/historical/");
    tree = html.fromstring(page.text);
    nodes = tree.xpath("//li[@class=\"text-center\"]/a");
    array = [];
    for n in nodes:
         array.append("https://coinmarketcap.com/" + n.get("href"));
    return  array;

def marketCap():
    us = urls();
    for u in  us:
        page = requests.get(u);
        tree = html.fromstring(page.text);
        nodes = tree.xpath("//td");
        found = False;
        date = re.findall("\d{8}",u);
        data = [date][0];
        btccap = 0;
        for n in nodes:
            if found:
                btccap = n.get("data-usd");
                data.append(btccap);
                break;
            elif n.text == "BTC":
                found = True;
                data.append(n.text);
        captotal = tree.xpath("//span[@id=\"total-marketcap\"]")[0].text;
        captotal = re.findall("[\d+,?]+",captotal)[0].replace(",","");
        data.append(captotal);
        data.append(float(btccap)  / float(captotal) * 100);
        print  str(data).replace("[","").replace("]","");


marketCap();
#print urls();



