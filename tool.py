# -*- coding:utf-8 -*-
# @Time    :2021/3/12 20:05
# @Author  :Benjamin
# @File    :tool.py


folder='src/'
urlFile='urls.txt'
import requests
import os
import sys
import time



if __name__=='__main__':

    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        os.chdir(folder)
        for f in os.listdir():
            os.unlink(f)
        os.chdir('../')

    if len(sys.argv)==1:
        with open(urlFile,'r') as f:
            urls=f.read().strip()
            urls=urls.split('\n')
    else:
        urls=sys.argv[1:]

    print('需要下载文件数：'+str(len(urls)))
    for url in urls:
            start = time.time()
            r = requests.get(url=url,stream=True)
            size =0
            chunk_size=1024
            content_size = int(r.headers['content-length'])  # 下载文件总大小
            fileName = r.headers['Content-Disposition'].split(';')[1].split('=')[1]
            fileName = bytes.decode(fileName.encode('ISO-8859-1'),'utf-8')
            try:
                if r.status_code == 200:  # 判断是否响应成功
                    print('正在下载：'+fileName+'\t文件大小:{:.2f} MB'.format(
                        content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小

                    with open(folder + fileName, 'wb') as f:
                        for data in r.iter_content(chunk_size=chunk_size):
                            f.write(data)
                            size += len(data)
                            print('\r' + 'Downloading:[{0}]{1:.2%}' .format (
                                '>' * int(size * 50 / content_size), float(size / content_size)), end=' ')
            except Exception as e:
                print(e.args)
            end = time.time()  # 下载结束时间
            print('\tDownload completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间



    print('finished!')
