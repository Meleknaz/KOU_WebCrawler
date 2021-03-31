import requests
import operator 
from bs4 import BeautifulSoup, SoupStrainer
from flask import Flask, render_template, request
from collections import Counter,OrderedDict

# Creates a dictionary conatining each word's
def create_dictionary(clean_list):
    word_count = {}

    #her wordnin tek tek tümtüm wordsde aranması
    for word in clean_list:
        #word tekrarı varsa değer 1 arttırılır
        if word in word_count:
            word_count[word] += 1
        else:
            #word sadece 1 kere kullanılmıssa değeri 1 e eşitlenir
            word_count[word] = 1
    return word_count


# Function removes any unwanted symbols
def clean_wordlist(clean_list):
   sembolsuzwords = []
   semboller = "!@#$%^&*()_-+={[}]|\;:\"<>?/., " + chr(775)
   for word in clean_list:
      for sembol in semboller:
         if sembol in word:
            word = word.replace(sembol,"")
      if(len(word)>0):
         sembolsuzwords.append(word)
   return  sembolsuzwords

def calculateFrequency(url):
    clean_list = []
    r =requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    for each_text in soup.find_all("p"):
        # print(each_text) p etiketine sahip word gruplarını aldık
        content = each_text.text
        #print(content) word gruplarının text kısımlarını alıp içerik değişkenine atıyoruz
        words = content.lower().split()
        #print(words) tüm wordsi lower ile küçük harfe dönüştürdük split ile boşluklara göre wordsi aldık

        for word in words:
            clean_list.append(word)
            #print(word) tüm wordsi aldık


    clean_list = clean_wordlist(clean_list)
    #for word in clean_list:
    #print(word)

    word_count = create_dictionary(clean_list)
    #wordsin frekanslarının sıralı olarak verilmesi
    for key,value in sorted(word_count.items(), key = operator.itemgetter(0)):
    #sorted metodunun ikinci parametresi hangi değere göre sıralanacağını belirler
        print(key,value)
        
    return word_count

def calculateKeyword(url):
    clean_list = []
    r =requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    for each_text in soup.find_all("p"):
        # print(each_text) p etiketine sahip word gruplarını aldık
        content = each_text.text
        #print(content) word gruplarının text kısımlarını alıp içerik değişkenine atıyoruz
        words = content.lower().split()
        #print(words) tüm wordsi lower ile küçük harfe dönüştürdük split ile boşluklara göre wordsi aldık

        for word in words:
            clean_list.append(word)
            #print(word) tüm wordsi aldık


    clean_list = clean_wordlist(clean_list)
    #for word in clean_list:
    #print(word)

    word_count = create_dictionary(clean_list)
    #wordsin frekanslarının sıralı olarak verilmesi
    for key,value in sorted(word_count.items(), key = operator.itemgetter(1)):
    #sorted metodunun ikinci parametresi hangi değere göre sıralanacağını belirler
        print(key,value)
    
    c = Counter(word_count)
    top = c.most_common(5)
    return top

def skorlamaHesapla(url1, url2):
    top1 = ()
    top2 = ()
    clean_list1 = []
    clean_list2 = []
    convertation = []
    new_list = []
    top1_size =0
    r1 =requests.get(url1)
    r2 =requests.get(url2)
    soup1 = BeautifulSoup(r1.content, "html.parser")
    soup2 = BeautifulSoup(r2.content, "html.parser")
    
    for each_text1 in soup1.find_all("p"):
        content1 = each_text1.text
        words1 = content1.lower().split()

        for word1 in words1:
            clean_list1.append(word1)

    clean_list1 = clean_wordlist(clean_list1)       
    word_count1 = create_dictionary(clean_list1)
    #wordsin frekanslarının sıralı olarak verilmesi
    for key1,value1 in sorted(word_count1.items(), key = operator.itemgetter(1)):
    #sorted metodunun ikinci parametresi hangi değere göre sıralanacağını belirler
        print(key1,value1)

    #2.url için****************************

    for each_text2 in soup2.find_all("p"):
        content2 = each_text2.text
        words2 = content2.lower().split()

        for word2 in words2:
            clean_list2.append(word2)
            #print(word) tüm wordsi aldık

    clean_list2 = clean_wordlist(clean_list2)       
    word_count2 = create_dictionary(clean_list2)

    for key2,value2 in sorted(word_count2.items(), key = operator.itemgetter(1)):
        print(key2,value2)

    c1 = Counter(word_count1)
    c2 = Counter(word_count2)
    top1 = c1.most_common(5)
    top2 = c2.most_common(5)
    convertation = list(top1)


    for i in clean_list2:
        for j in convertation:
            if i == j[0]:
                new_list.append(i)
                
    result = list(OrderedDict.fromkeys(new_list)) #valueler tekrar etmesin diye 
    
    for i in range(5):
        top1_size+=top1[i][1]

    #skor = 100*((len(clean_list2)) /(len(clean_list1)))
    skor = 100*((len(new_list) / len(clean_list2)) /(top1_size/len(clean_list1)))
    print(f"len(new_list){len(new_list)}")
    print(f"len(clean_list2){len(clean_list2)}")
    print(f"top1_size{top1_size}")
    print(f"len(clean_list1){len(clean_list1)}")
    print(f"skor{skor}")
    print(f"new list:{result}")

    return top1,clean_list2,result,skor

def WebIndexing(url):

    set_of_url_list = ["https://www.bbc.com/news/world-europe-56580728",
                    "https://www.cbc.ca/news/politics/astrazeneca-under-55-1.5968128",
                    "https://www.aljazeera.com/news/2021/3/29/canada-to-pause-use-of-astrazeneca-vaccine-for-those-under-55",
                    "https://www.bbc.com/news/av/science-environment-56303321",
                    "https://www.bbc.com/news/science-environment-56297996",
                    "https://www.geeksforgeeks.org/",
                    "https://meleknazablak.medium.com/github-hesab%C4%B1n%C4%B1za-readme-dosyas%C4%B1-ekleme-c1f8553723d8",
                    "https://www.geeksforgeeks.org/python-program-crawl-web-page-get-frequent-words/",
                    "https://practice.geeksforgeeks.org/courses/",
                    "https://meleknazablak.medium.com/github-hesab%C4%B1n%C4%B1za-readme-dosyas%C4%B1-ekleme-c1f8553723d8",
                    "https://www.geeksforgeeks.org/python-program-crawl-web-page-get-frequent-words/",                    
                    "https://www.geeksforgeeks.org/write-interview-experience/"]
    top1 = ()
    top2 = ()
    clean_list1 = []
    clean_list2 = []
    convertation = []
    convertation2 = []
    new_list = []
    skor_list = []
    top2_list = []
    top1_size =0
    r1 =requests.get(url)  
    soup1 = BeautifulSoup(r1.content, "html.parser")
    r2 =requests.get(set_of_url_list[0])
    soup2 = BeautifulSoup(r2.content, "html.parser")

    # ******URL kümesine request atma işlemi******
    for i in range(4):
        r2 =requests.get(set_of_url_list[i])
        soup2 = BeautifulSoup(r2.content, "html.parser")
        new_list.append(soup2)


    # *********ana url işlemleri*********
    for each_text1 in soup1.find_all("p"):
        content1 = each_text1.text
        words1 = content1.lower().split()
        
        for word1 in words1:
            clean_list1.append(word1)
            
    clean_list1 = clean_wordlist(clean_list1)
    word_count1 = create_dictionary(clean_list1)

    # *********URL kümesi işlemleri*********
    for i in range(4):
        for each_text2 in new_list[i].find_all("p"):
            content2 = each_text2.text
            words2 = content2.lower().split()

            for word2 in words2:
                clean_list2.append(word2)

        clean_list2 = clean_wordlist(clean_list2)       
        word_count2 = create_dictionary(clean_list2)
        #print(f"clean list*****:{clean_list2}")      
    
    c1 = Counter(word_count1)
    c2 = Counter(word_count2)
    top1 = c1.most_common(5)
    top2 = c2.most_common(5)
    convertation2 = list(top2)
    top2_list.append(top2)
    convertation = list(top1)

    for k in word_count2:
        for i in clean_list2:
            for j in convertation:
                if i == j[0]:
                    new_list.append(i)
                    
    result = list(OrderedDict.fromkeys(new_list)) #valueler tekrar etmesin diye 
    #print( f"********result********{result}") 

    # ********* URL kümesi skorlama işlemleri **********

    for i in range(4):
        top1_size+=top1[i][1]
        skor = ((len(new_list) / len(clean_list2)) /(top1_size/len(clean_list1)))/10
        print(f"skor{skor}")
        skor_list.append(skor)


    print(f"len(new_list){len(new_list)}")
    print(f"len(clean_list2){len(clean_list2)}")
    print(f"top1_size{top1_size}")
    print(f"len(clean_list1){len(clean_list1)}")


    # ********** alt url işlemleri *********

    for link in soup1.find_all("a"):
        sub_url_list = link.get('href')
        list(sub_url_list)
        print(f"sub_url_list{sub_url_list}")   

    """# ****** DERİNLİK BULMA ÇABAMIZ ******

    r2 =requests.get(url)
    soup2 = BeautifulSoup(r2.content, "html.parser", from_encoding="utf-8")
    depth1= list()
    for link in soup2.find_all("a"):
        depth1.append(link['href'])

    r3 =requests.get(depth1)  
    soup3 = BeautifulSoup(r3.content, "html.parser", from_encoding="utf-8")
    depth2 = list()
    for link2 in soup3.find_all("a"):
        if "http://" in link2['href'] or "https://" in link2['href']:
            depth2.append(link2['href'])

    r4= requests.get(depth2)
    soup4 = BeautifulSoup(r4.content, "html.parser", from_encoding="utf-8")
    depth3 = list()
    for link3 in soup4.find_all("a"):
        if "http://" in link2['href'] or "https://" in link2['href']:
            depth3.append(link3['href'])

    
    print(f"Derinlik 1 sub_url_list: {depth1[:5]}")
    print(f"Derinlik 2 sub_url_list: {depth1[:5]}")
    print(f"Derinlik 3 sub_url_list: {depth3[:5]}")"""

    return skor_list[0],skor_list[1],skor_list[2],skor_list[3],max(skor_list)
    
def SemantikAnaliz(url):

    r =requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    for link in soup.find_all("a"):
        depth1.append(link['href'])



app = Flask(__name__)
@app.route('/')   #kök url
def index():
    return render_template("PageOne.html",methods=["GET","POST"])

@app.route("/1",methods=["GET","POST"])
def frekansSayfasi():
    if request.method == "POST":
        url = request.form.get("url")
        veri=calculateFrequency(url)
        return render_template("PageOne.html",veri=veri)
    else:
        return render_template("PageOne.html")

@app.route("/2",methods=["GET","POST"])
def keywordBulma():
    if request.method == "POST":
        url2 = request.form.get("url")
        veri=calculateKeyword(url2)
        return render_template("PageTwo.html",veri=veri)
    else:
        return render_template("PageTwo.html")

@app.route("/3",methods=["GET","POST"])
def Skorlama():
    if request.method == "POST":
        url1= request.form.get("url1")
        url2= request.form.get("url2")
        veri1,veri2,result,skor =skorlamaHesapla(url1,url2)
        return render_template("PageThree.html",veri1=veri1, veri2=veri2, result=result, skor=skor)
    else:
        return render_template("PageThree.html")

@app.route("/4",methods=["GET","POST"])
def getURL():
    if request.method == "POST":
        url= request.form.get("url")
        #url2= request.form.get("url_set")
        skor1,skor2,skor3,skor4,Maxskor=WebIndexing(url)
        return render_template("PageFour.html", skor1=skor1, skor2=skor2, skor3=skor3,skor4=skor4,Maxskor=Maxskor)
        #top1,veri1,veri2,veri3,veri4,veri5,result,skor=WebIndexing(url1)
        #return render_template("PageFour.html", top1=top1,veri1=veri1, veri2=veri2,  veri3=veri3, veri4=veri4,veri5=veri5,result=result, skor=skor)
        
    else:
        return render_template("PageFour.html")

@app.route("/5",methods=["GET","POST"])
def SemantikAnaliz():
    if request.method == "POST":
        url = request.form.get("url")
        veri=SemantikAnaliz(url)
        return render_template("PageFive.html",veri=veri)
    else:
        return render_template("PageFive.html")

if __name__ == '__main__':
    app.run(debug = True)

