import requests
import shutil
import os
import img2pdf


def numToNdigit(n,N):
    # N is always greater than number of digits in n
    l = len(str(n))
    ans = "0"*(N-l)
    ans += str(n)
    return ans

def downloadChapter(base_url, base_dir, chapter):
    chapter_name = numToNdigit(chapter,4) # XXXX
    
    # create a folder with the chapter number as the name
    os.mkdir(f"{base_dir}/{chapter}") # this is the images folder
    os.chdir(f"{base_dir}/{chapter}")
    
    # download all the images here
    for page in range(1,75):
        page_name = numToNdigit(page,3) # XXX
        request_url = base_url+chapter_name+"-"+page_name+".png"
        r = requests.get(request_url, stream=True)
        if r.status_code == 200:
            file_name = page_name+".png"
            with open(file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            break
    
    # compile all images into pdf
    images = os.listdir(f"{base_dir}/{chapter}")
    images.sort()
    
    if (len(images)==0):
        return chapter
    
    with open(f"{base_dir}/{chapter_name}.pdf","wb") as f:
        f.write(img2pdf.convert(images))
    
    # delete the images folder
    os.chdir(base_dir)
    shutil.rmtree(f"{base_dir}/{chapter}")
    
    return chapter