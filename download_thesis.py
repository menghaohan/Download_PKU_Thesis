import requests
import json
import os
import img2pdf

def request_img(fid, cookie, title):
    #set header
    header={}
    header['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    header['Accept']='*/*'
    header['Accept-Encoding']='gzip, deflate'
    header['Accept-Language']='zh-CN,zh;q=0.9,en;q=0.8'
    header['Cookie']=cookie
    header['Referer']='http://162.105.134.201/pdfindex.jsp?fid='+fid

    if not os.path.exists(title):
        os.mkdir(title)

    page=0
    img_ids=set()
    while True:
        url='http://162.105.134.201/jumpServlet?page='+str(page)+'&fid='+fid
        response=requests.get(url, headers=header)
        if response.status_code==200:
            try:
                json_urls=json.loads(response.text)['list']
                for li in json_urls:
                    img_id=li['id']
                    if img_id not in img_ids:
                        img=requests.get(li['src'])
                        if img.status_code==200:
                            with open(title+'/'+img_id+'.jpg', 'wb') as f:
                                f.write(img.content)
                            img_ids.add(int(img_id))
                        else:
                            print('下载图片失败\n')
                            page-=3
                    else:
                        continue
            except:
                print('解析失败')
                print(response.text)
                break
        else:
            print(response.status_code)
            break
        page+=3
    return max(img_ids)


def img_to_pdf(title, max_page):
    imgs=[]
    for page in range(max_page+1):
        imgs.append(title+'/'+str(page)+'.jpg')
    with open(title+'.pdf', 'wb') as f:
        f.write(img2pdf.convert(imgs))
    print(title+'.pdf已合成！')




cookie='JSESSIONID=FAB654785027E5C32B19AB265A9BDB84'
fid='35a98c62f193e0e92c45d909a7efc945'
title='基于地理大数据的全国尺度 人口移动和行业结构特征研究'
max_page=request_img(fid, cookie, title)
print(max_page)
img_to_pdf(title, max_page)
