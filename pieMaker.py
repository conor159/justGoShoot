#check disk space
import psutil
import turtle as t 
from PIL import Image , ImageDraw

def createLogoPie():
    hdd = psutil.disk_usage('/')
    free = (hdd.free // 2**30) 
    total = (hdd.total // 2**30)
    usedPersentage = (free / total )
    usedPersentage =  round(usedPersentage,1)
    usedPersentage =  usedPersentage * 10

    usedInt = str(int(usedPersentage))

    logo = Image.open("static/images/pie/"+usedInt+".png")
    logo.save("static/images/pie.png")


if __name__ == "__main__":
    createLogoPie()
