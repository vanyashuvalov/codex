from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, wave, struct, random

root = Path('src/client/resources')
(root/'assets/yourvisuals/textures/entity').mkdir(parents=True, exist_ok=True)
(root/'assets/yourvisuals/sounds').mkdir(parents=True, exist_ok=True)
(root/'assets/minecraft/textures/environment').mkdir(parents=True, exist_ok=True)

# Straw Chinese-hat texture
im=Image.new('RGBA',(64,64),(219,171,90,255)); d=ImageDraw.Draw(im)
for y in range(64):
    d.line((0,y,63,y),fill=(224-int(y*.45),177-int(y*.30),96-int(y*.15),255))
for y in range(4,64,6): d.line((0,y,63,y),fill=(154,105,50,90))
for x in range(0,64,8): d.line((x,0,x,63),fill=(255,230,160,35))
im.save(root/'assets/yourvisuals/textures/entity/chinese_hat.png')

# Anime sun
sun=Image.new('RGBA',(64,64),(0,0,0,0)); d=ImageDraw.Draw(sun)
for r,a in [(29,20),(25,45),(21,95)]: d.ellipse((32-r,32-r,32+r,32+r),fill=(255,176,210,a))
d.ellipse((14,14,50,50),fill=(255,238,247,255)); d.ellipse((18,18,46,46),fill=(255,184,216,255))
sun.filter(ImageFilter.GaussianBlur(.7)).save(root/'assets/minecraft/textures/environment/sun.png')

# Pink moon phase atlas
moon=Image.new('RGBA',(64,32),(0,0,0,0)); d=ImageDraw.Draw(moon)
for idx,shift in enumerate([0,4,7,10,13,10,7,4]):
    cx=(idx%4)*16+8; cy=(idx//4)*16+8
    d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=(255,224,244,255))
    if shift: d.ellipse((cx-7+shift,cy-7,cx+7+shift,cy+7),fill=(42,35,75,255))
moon.save(root/'assets/minecraft/textures/environment/moon_phases.png')

# Soft pink anime clouds
cloud=Image.new('RGBA',(256,256),(0,0,0,0)); d=ImageDraw.Draw(cloud); random.seed(2)
for row in range(4):
    basey=row*64+20
    for col in range(4):
        basex=col*64+random.randint(-8,8)
        for _ in range(7):
            x=basex+random.randint(-20,40); y=basey+random.randint(-8,14); r=random.randint(9,20)
            d.ellipse((x-r,y-r//2,x+r,y+r//2),fill=(255,244,250,170 if random.random()>.25 else 120))
        d.rectangle((basex-22,basey,basex+42,basey+13),fill=(255,241,249,150))
cloud.filter(ImageFilter.GaussianBlur(2)).save(root/'assets/minecraft/textures/environment/clouds.png')

# Cute synthetic hit sounds (converted to ogg by CI)
sr=44100
for kind,dur in [('uwu',.22),('nya',.18),('pop',.08)]:
    data=[]
    for i in range(int(sr*dur)):
        t=i/sr; env=min(1,t/.015)*max(0,1-t/dur)**1.8
        if kind=='uwu':
            f=430+120*math.sin(math.pi*t/dur); s=.52*math.sin(2*math.pi*f*t)+.24*math.sin(2*math.pi*f*2.02*t)+.12*math.sin(2*math.pi*760*t)
        elif kind=='nya':
            f=650+420*t/dur; s=.55*math.sin(2*math.pi*f*t)+.22*math.sin(2*math.pi*f*1.5*t)
        else:
            f=1150-650*t/dur; s=.7*math.sin(2*math.pi*f*t)+.08*random.uniform(-1,1)
        data.append(max(-1,min(1,s*env))*.65)
    with wave.open(str(root/f'assets/yourvisuals/sounds/{kind}.wav'),'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h',int(v*32767)) for v in data))
