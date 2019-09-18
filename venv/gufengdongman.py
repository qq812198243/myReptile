from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from threading import Timer
import requests,js2xml,os,random
import xmltodict,json,time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
headerUrl = "https://m.gufengmh8.com"
headerUrl36 = "https://www.36mh.com"

imageHearderUrl = "https://res.gufengmh8.com/"
imageHearderUrl36 = "https://img001.yayxcc.com/"
mainUrl = "https://m.gufengmh8.com/manhua/bailianchengshen/"
numberUrl = []


def mkdir(path,name):#创建目录并返回目录位置1：ture false 2:路径名称
    path = os.path.join(path,name)#地址拼接函数
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+"创建目录成功")
        return True,path
    else:
        print(path+"目录已存在")
        return False,path
# print(os.getcwd())
# print(mkdir(os.getcwd(),'wqx')[1])

#----------------------------------------
def download(url, savepath='./'):
    """
    download file from internet
    :param url: path to download from
    :param savepath: path to save files
    :return: None
    """

    def reporthook(a, b, c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    filename = os.path.basename(url)
    # 判断文件是否存在，如果不存在则下载
    if not os.path.isfile(os.path.join(savepath, filename)):
        print('Downloading data from %s' % url)
        urlretrieve(url, os.path.join(savepath, filename), reporthook=reporthook)
        print('\nDownload finished!')
    else:
        print('File already exsits!')
    # 获取文件大小
    filesize = os.path.getsize(os.path.join(savepath, filename))
    # 文件大小默认以Bytes计， 转换为Mb
    print('File size = %.2f Mb' % (filesize / 1024 / 1024))
#-------------------------------------------------------------


def getUrl(url):#获得漫画全部话数的url
    try:
        href = []
        wb_data = requests.get(url,headers=headers)
        wb_data.encoding = "utf-8"
        soup = BeautifulSoup(wb_data.text,'html.parser')
        selction = soup.select('#chapter-list-1 li a')
        for tag in selction:
            href.append(headerUrl+str(tag.get("href")))
    except:
        print("获取漫画话数出错")
    return href

def getUrl36(url):#获得漫画全部话数的url
    try:
        pieceUrl = url.split('/')
        url = headerUrl36 + '/' + pieceUrl[-3] + '/' + pieceUrl[-2]
        href = []
        wb_data = requests.get(url,headers=headers)
        wb_data.encoding = "utf-8"
        soup = BeautifulSoup(wb_data.text,'html.parser')
        selction = soup.select('#chapter-list-4 li a')
        # print("section:",selction)
        for tag in selction:
            href.append(headerUrl36+str(tag.get("href")))
    except :
        print("获取漫画话数出错")
    return href

def autoJsToxml(url):#js转换成xml格式
    wb_data = requests.get(url,headers=headers)
    wb_data.encoding = "utf-8"
    soup = BeautifulSoup(wb_data.text,"html.parser")
    selction = soup.select('script')
    # print(selction)
    i = 0
    for keyWord in selction:#自动匹配需要script字段
        keyWord = keyWord.get_text()
        if keyWord.find("jpg") != -1:
            key = i
        else:
            i = i+1
    # print(key) 自动匹配
    l = selction[key].string
    src_text = js2xml.parse(l,encoding='utf-8',debug=False)
    # print(type(src_text))
    src_tree = js2xml.pretty_print(src_text)
    # print(src_tree)
    return src_tree

def getImagesUrl36(url):#输出36漫画下载链接
    imagesUrl = []
    myXml = autoJsToxml(url)
    soup = BeautifulSoup(myXml, 'lxml')
    # print('soup',soup)
    numberJpg = soup.select('array > string')
    # print('numberJpg',numberJpg)
    linkUrl = soup.find("var", attrs={'name': 'chapterPath'}).get_text()
    linkUrl = linkUrl.strip('\n')
    for imageTag in numberJpg:
        imagesUrl.append(imageHearderUrl36 + linkUrl + imageTag.get_text())
    return imagesUrl



def getPcImageUrl(url):#输出PC漫画下载链接 error
    imagesUrl = []
    myXml = autoJsToxml(url)
    soup = BeautifulSoup(myXml, 'lxml')
    # print('soup',soup)
    numberJpg = soup.select('array > string')
    # print('numberJpg',numberJpg)
    linkUrl = soup.find("var", attrs={'name': 'chapterPath'}).get_text()
    linkUrl = linkUrl.strip('\n')
    for imageTag in numberJpg:
        imagesUrl.append(imageHearderUrl + linkUrl + imageTag.get_text())
    return imagesUrl




def getPhoneImageUrl(url):#输出phone漫画下载链接
    imagesUrl = []
    myXml = jsToxml2(url)
    soup = BeautifulSoup(myXml,'lxml')
    numberJpg = soup.select('array > string')
    linkUrl = soup.find("var", attrs={'name': 'chapterPath'}).get_text()
    linkUrl = linkUrl.strip('\n')
    for imageTag in numberJpg:
        imagesUrl.append(imageHearderUrl+linkUrl+imageTag.get_text())
    return imagesUrl


def newDownload(urls):#更新的漫画优化使用
    for myUrl in urls:
        for myUrl in urls:  # 获得每个漫画首页地址
            manhuaName = myUrl.split('/')
            manhuaPath = os.getcwd() + '\\' + manhuaName[-2]
            try:
                numbersUrl = getUrl(myUrl)  # 获得每个漫画的话数地址
                print("漫画数地址:", numbersUrl)
                mkdir(manhuaPath, str(len(numbersUrl)))
                images = getPcImageUrl(numbersUrl[-1])  # 获得话数的图片下载地址
                print("漫画图片下载地址:", images)
                time.sleep(random.uniform(0, 1))
                # i = 0
                for image in images:  # 分别下载话数地址
                    try:
                        downloadPath = manhuaPath + '\\' + str(len(numbersUrl))
                        # print(image.split('/'))
                        oldName = image.split('/')
                        download(image, downloadPath)
                        # print("old",downloadPath+'\\'+oldName[-1])
                        # print('new',downloadPath+'\\'+str(i)+'.jpg')
                    except Exception as e :
                        print("404获取图片超时或者异常")
                        print(e.args)
                    # else:
                    #     os.rename(downloadPath+'//'+oldName[-1],downloadPath+'//'+str(i)+'.jpg')
                    # i = i + 1
            except:
                print("主程序获取链接超时或者异常")
        print("完成时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def newDownload36(urls):#更新的漫画优化使用
    for myUrl in urls:
        for myUrl in urls:  # 获得每个漫画首页地址
            manhuaName = myUrl.split('/')
            manhuaPath = os.getcwd() + '\\' + manhuaName[-2]
            try:
                numbersUrl = getUrl36(myUrl)  # 获得每个漫画的话数地址
                print("漫画数地址:", numbersUrl)
                mkdir(manhuaPath, str(len(numbersUrl)))
                images = getImagesUrl36(numbersUrl[-1])  # 获得话数的图片下载地址
                print("漫画图片下载地址:", images)
                time.sleep(random.uniform(0, 1))
                # i = 0
                for image in images:  # 分别下载话数地址
                    try:
                        downloadPath = manhuaPath + '\\' + str(len(numbersUrl))
                        # print(image.split('/'))
                        oldName = image.split('/')
                        download(image, downloadPath)
                        # print("old",downloadPath+'\\'+oldName[-1])
                        # print('new',downloadPath+'\\'+str(i)+'.jpg')
                    except Exception as e :
                        print("404获取图片超时或者异常")
                        print(e.args)
                    # else:
                    #     os.rename(downloadPath+'//'+oldName[-1],downloadPath+'//'+str(i)+'.jpg')
                    # i = i + 1
            except:
                print("主程序获取链接超时或者异常")
        print("完成时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



def inputListUrl():#输入并创建漫画文件夹
    print('请输入多个URl,使用空格隔开,注意结尾务必添加/')
    myList = list(map(str, input().strip().split()))
    for manhuaList in myList:
        manhuaName = manhuaList.split('/')
        mkdir(os.getcwd(),manhuaName[-2])
    return myList


def downloadManhua(*urls):#下载漫画
    # print(urls)
    for myUrl in urls:#获得每个漫画首页地址
        p = 0
        manhuaName = myUrl.split('/')
        manhuaPath = os.getcwd()+'\\'+manhuaName[-2]
        if manhuaName[2] == "www.gufengmh8.com":#gufengdongman
            try:
                numbersUrl = getUrl(myUrl)  # 获得每个漫画的话数地址
                print("漫画数地址:", numbersUrl)
                for numberUrl in numbersUrl:  # 将话数地址遍历出来
                    mkdir(manhuaPath, str(p))
                    images = getPcImageUrl(numberUrl)  # 获得话数的图片下载地址
                    print("漫画图片下载地址:", images)
                    time.sleep(random.uniform(0, 1))
                    # i = 0
                    for image in images:  # 分别下载话数地址
                        try:
                            downloadPath = manhuaPath + '\\' + str(p)
                            oldName = image.split('/')
                            download(image, downloadPath)

                        except Exception as e:
                            print("404获取图片超时或者异常")
                            print(e.args)
                        # else:
                        #     try:
                        #         os.rename(downloadPath + '//' + oldName[-1], downloadPath + '//' + str(i) + '.jpg')
                        #     except:
                        #         print("重命名失败或者已命名")
                        # i = i + 1
                    print('剩余', len(numbersUrl) - p - 1)
                    p = p + 1
            except Exception as e:
                print("主程序获取链接超时或者异常")
                print(e.args)
            # print("gu",manhuaName)
        elif manhuaName[2] == "www.36mh.com":#36mh
            try:
                numbersUrl = getUrl36(myUrl)  # 获得每个漫画的话数地址
                print("漫画数地址:", numbersUrl)
                for numberUrl in numbersUrl:  # 将话数地址遍历出来
                    mkdir(manhuaPath, str(p))
                    images = getImagesUrl36(numberUrl)  # 获得话数的图片下载地址
                    print("漫画图片下载地址:", images)
                    time.sleep(random.uniform(0, 1))
                    # i = 0
                    for image in images:  # 分别下载话数地址
                        try:
                            downloadPath = manhuaPath + '\\' + str(p)
                            oldName = image.split('/')
                            download(image, downloadPath)
                        except Exception as e:
                            print("404获取图片超时或者异常")
                            print(e.args)
                        # else:
                        #     try:
                        #         os.rename(downloadPath + '//' + oldName[-1], downloadPath + '//' + str(i) + '.jpg')
                        #     except:
                        #         print("重命名失败或者已命名")
                        # i = i + 1
                    print('剩余', len(numbersUrl) - p - 1)
                    p = p + 1
            except Exception as e:
                print("主程序获取链接超时或者异常")
                print(e.args)
            # print("36",manhuaName)
        else:
            print("请输入正确的网址链接")

    print("完成时间：",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))



if __name__ == '__main__':

    upOrDownload = input("请选择下载(1)漫画或者更新gufengdongman(2)36mh(3)漫画：\n")
    upOrDownload = upOrDownload.strip()
    if int(upOrDownload) == 1:
        numThread = input("请选择单线程或者双线程 单（1）双（2）：\n")
        numThread = numThread.strip()
        if int(numThread) == 1:
            print("进入单线程模式")
            print("线程1")
            numberUrl1 = inputListUrl()
            a = Timer(5.0, downloadManhua, numberUrl1)
            a.start()
        else:
            print("进入双线程模式")
            print("线程1")
            numberUrl1 = inputListUrl()
            print("线程2")
            numberUrl2 = inputListUrl()

            a = Timer(5.0, downloadManhua, numberUrl1)
            b = Timer(5.0,v,numberUrl2)
            a.start()
            b.start()
    elif int(upOrDownload) == 2:
        numberUrl = inputListUrl()
        newDownload(numberUrl)
    elif int(upOrDownload) == 3:
        numberUrl = inputListUrl()
        newDownload36(numberUrl)
    else:
        print("请输入正确的gufengdongman和36mh链接")
    # numberUrl = inputListUrl()
    # urls36 = getUrl36(numberUrl[0])
    # print(urls36)
    # print(getImagesUrl36(urls36[0]))

    # numberUrl = inputListUrl()
    # print(numberUrl)
    # newDownload(numberUrl)
    # a = Timer(1.0, downloadManhua, numberUrl)
    # a.start()

# numberUrl = inputListUrl()
# for i in range(0, 5):
#     downloadManhua(numberUrl)
#     a = random.uniform(1, 10)
#     time.sleep(a)