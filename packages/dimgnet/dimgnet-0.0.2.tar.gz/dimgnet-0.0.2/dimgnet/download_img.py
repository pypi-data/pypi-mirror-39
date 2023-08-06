import urllib.request as request
import sys
import string
import random
import argparse
import os
import time 
from dimgnet.bar import Bar

def get_resp(url):
    try:
        u = request.urlopen(url,timeout=2)
        return u
    except :
        return False

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getArguments():
    parser = argparse.ArgumentParser('Download image from ImageNet')
    parser.add_argument('-i','--wnid',help='Wnid of category')
    parser.add_argument('-f','--folder',help='Create new folder',default='image_'+id_generator())
    parser.add_argument('-q','--quantity',help='Quantity of Images',default=1e+10)
    args = parser.parse_args()
    return (args.wnid,args.folder,args.quantity)

def main():
    min_size = 8000
    wnid,folder,quantity = getArguments()

    link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='+wnid
    html = request.urlopen(link)
    content = html.read().decode('utf-8').split()
    if content[0] == 'Invalid':
       print('Wnid Invalid!')
       return
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    else :
        print('Folder name existed!')
        return

    random.shuffle(content)
    if int(quantity) < len(content):
        max = int(quantity)
    else :
        max = len(content)

    i = 0
    count = 0
    bar = Bar('Processing', max=max)
	
    while count < max and i<len(content) :
        line = content[i]
        resp = get_resp(line)
        if resp != False:
            name = id_generator()
            img = '{}/{}.jpg'.format(folder,name)
            #request.urlretrieve(line, img)
            save_img(resp,line,img)
            if os.stat(img).st_size < min_size :
                os.remove(img)
            else:
                count += 1
                bar.next()
                
        i+=1
    bar.finish()
    print('\nDone!')
           
def save_img(resp,link,file_name):
	respHtml = resp.read()
	binfile = open(file_name, "wb")
	binfile.write(respHtml)
	binfile.close()  

if __name__ == '__main__':
    main()
