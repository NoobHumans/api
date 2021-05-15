from PIL import Image

class cropping:
    def crop1(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 450
        y1 = yc - 400
        x2 = xc + 450
        y2 = yc + 400
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')
    def crop2(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 480
        y1 = yc - 460
        x2 = xc + 480
        y2 = yc + 460
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')
    def crop3(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 450
        y1 = yc - 275
        x2 = xc + 450
        y2 = yc + 275
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')
    def crop4(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 500
        y1 = yc - 275
        x2 = xc + 500
        y2 = yc + 275
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')
    def crop5(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 540
        y1 = yc - 955
        x2 = xc + 540
        y2 = yc + 910
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')
    def crop6(self, fname):
        image = Image.open('./img/'+fname+'.jpg')
        xc = image.width/2
        yc = image.height/2
        x1 = xc - 500
        y1 = yc - 345
        x2 = xc + 500
        y2 = yc + 335
        cropped = image.crop((x1, y1, x2, y2))
        cropped.save('./img/'+fname+'.jpg')