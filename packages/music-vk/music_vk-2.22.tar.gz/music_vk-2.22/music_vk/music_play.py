import pygame,time,vk_api,bot_vk,wget,urllib
from io import BytesIO
#s = requests.post("https://vrit.me/action.php",headers={"Accept": "*/*","Accept-Encoding": "gzip, deflate, br","Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7","Connection": "keep-alive","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116","X-Requested-With": "XMLHttpRequest"},data={"method": "audio.get","user_id": str(f),"offset": "0","count": "20000"}).json()
    
#if "html" in s:
#    q = re.findall("""<div class="play" data="(.+?)"></div>""",s["html"].replace(r"/download.php","https://vrit.me/download.php"))
#    for i in range(len(q)):
#        q[i] = "https://vrit.me/audio.php?play="+q[i]
class play(object):
    def __init__(self,vk):
        self.mixer = None
        self.vk = vk
        
    def start(self,url):
        f = urllib.request.urlopen(url);file = BytesIO(f.read())
        self.mixer = pygame.mixer
        self.mixer.init() 
        self.mixer.music.load(file)
        self.mixer.music.play()
    def stop(self):
        self.mixer.music.stop()
    def download(self,url,file):
        f = wget.download(url,out=file);
        
