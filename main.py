import math

class Bike:
    def __init__(self, stack=0.0, reach=0.0, headAngle=0.0, seatAngle=0.0, seatTubeLength=0.0):
        self.stack = stack
        self.reach = reach
        self.headAngle = headAngle
        self.seatAngle = seatAngle
        self.offsetAngle = 0
        self.seatTubeLength = seatTubeLength
        self.totSeatLength = 0

    def calcSeatXY(self, seatHeight=0.0, seatpostOffset=0.0, saddleOffset=0.0):
        #Seat height is measured from the center of the BB to the BRP of the saddle.
        #Saddle offset is measured horizontally from center of seat clamp to BRP
        # Saddle offset is negative when BRP is in front of seatpost
        # y |
        #   |x seat       x handlebars
        #   | \           |
        #   |  \---------/\
        #   |   \       /  \
        #   |    \     /    \
        #   |     \   /
        #   |      \ /
        #   |_______x BB_________________________ x

        offsets = seatpostOffset+saddleOffset
        offsetAngle = math.asin((offsets*math.sin(math.radians(self.seatAngle)))/seatHeight)
        self.offsetAngle = self.seatAngle-math.degrees(offsetAngle)
        y = seatHeight * math.sin(math.radians(self.offsetAngle))
        x = seatHeight * math.cos(math.radians(self.offsetAngle))

        B = 180-self.offsetAngle
        self.totSeatLength = seatHeight*math.sin(math.radians(B))/math.sin(math.radians(self.seatAngle))

        return int(x),int(y)

    def calcHandBarXY(self, stemLength=0.0, stemAngle=0.0, spacers=0.0, hstem=0.0, dHandlebars=31.8):
        rHandlebars = dHandlebars/2
        # StemAngle is positive if it increases the head angle
        totStemAngle = self.headAngle + stemAngle

        ## Calculate x,y added by stem
        stemx = math.sin(math.radians(totStemAngle))*stemLength
        stemy = math.cos(math.radians(totStemAngle))*stemLength

        ## Calculate x,y added by spacers and stem.
        forkx = - rHandlebars + math.cos(math.radians(self.headAngle))*(spacers+hstem/2) * (1,-1)[self.headAngle<90]  # negative if head angle is below 90
        forky = rHandlebars + math.sin(math.radians(self.headAngle))*(spacers+hstem/2)

        x = self.reach + stemx + forkx
        y = self.stack + stemy + forky
        return int(x),int(y)

    def calcSeatPostIncertion(self, seatpostLength=0.0):

        assert (self.totSeatLength!=0),print("Calculate BRP first!")
        return seatpostLength+self.seatTubeLength-self.totSeatLength

CurrentBike = Bike(stack=609, reach=391, headAngle=72.3, seatAngle=73, seatTubeLength=580)



brp = CurrentBike.calcSeatXY(787, 0, -20)

hb = CurrentBike.calcHandBarXY(100, 7, 45, 40)

seatPostIncertion = CurrentBike.calcSeatPostIncertion(330)

print("brp: ", brp)
print("hb: ", hb)
print(f"Seatpost Insert: {seatPostIncertion:.2f}\n")

d = math.sqrt((hb[0]+brp[0])**2+(hb[1]-brp[1]))
print(f"Distance from BRP to HB is: {d:.2f}mm")
print(f"Real angle of BB to seat is: {CurrentBike.offsetAngle:.2f} degrees\n\n")

ParalaneL = Bike(stack=602.6, reach=389, headAngle=72, seatAngle=74, seatTubeLength=535)

PLbrp = ParalaneL.calcSeatXY(787, 15, -20)

PLhb = ParalaneL.calcHandBarXY(110, 8, 25, 40)

seatPostIncertion = ParalaneL.calcSeatPostIncertion(350)

print("Paralane L brp: ", PLbrp)
print("Paralane L hb: ", PLhb)
print(f"Seatpost Insert: {seatPostIncertion:.2f}\n\n")

#d = math.sqrt((hb[0]+brp[0])**2+(hb[1]-brp[1]))
#print(f"Distance from BRP to HB is: {d:.2f}mm")
#print(f"Real angle of BB to seat is: {ParalaneL.offsetAngle:.2f} degrees")

ParalaneXL = Bike(stack=633.1, reach=403, headAngle=72.5, seatAngle=73, seatTubeLength=575)

PXLbrp = ParalaneXL.calcSeatXY(787, 15, -35)

PXLhb = ParalaneXL.calcHandBarXY(80, 8, 25, 40)

seatPostIncertion = ParalaneXL.calcSeatPostIncertion(350)

print("Paralane XL brp: ", PXLbrp)
print("Paralane XL hb: ", PXLhb)
print(f"Seatpost Insert: {seatPostIncertion:.2f}")

#d = math.sqrt((hb[0]+brp[0])**2+(hb[1]-brp[1]))
#print(f"Distance from BRP to HB is: {d:.2f}mm")
#print(f"Real angle of BB to seat is: {ParalaneXL.offsetAngle:.2f} degrees")