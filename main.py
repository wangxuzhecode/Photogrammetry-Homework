from math import cos, sin
import numpy as np
from InnerElement import InnerElement
from OutterElement import OutterElement
from GroundPoint import GroundPoint
from PhotoPoint import PhotoPoint
from utils import getMatrix_A, getMatrix_L


class Sovle:

    def __init__(self, innerElement, gp1, gp2, gp3, gp4, pp1, pp2, pp3, pp4):

        self.innerElement = innerElement
        self.outterElement = OutterElement()
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.gp4 = gp4
        self.pp1 = pp1
        self.pp2 = pp2
        self.pp3 = pp3
        self.pp4 = pp4
        self.gpList = [self.gp1, self.gp2, self.gp3, self.gp4]
        self.ppList = [self.pp1, self.pp2, self.pp3, self.pp4]
        self.m = 50000
        self.get_init()
        self.L = np.zeros((len(self.gpList) * 2, 1), dtype=np.float32)  # (2n,1)
        self.A = np.zeros((len(self.gpList) * 2, 6), dtype=np.float32)  # (2n,6)

    def get_init(self):
        for item in self.gpList:
            self.outterElement.Xs += item.X
            self.outterElement.Ys += item.Y
            self.outterElement.Zs += item.Z
        self.outterElement.Xs /= len(self.gpList)
        self.outterElement.Ys /= len(self.gpList)
        self.outterElement.Zs = self.outterElement.Zs / len(self.gpList) + self.m * self.innerElement.f

    def get_RotationMatrix(self):
        fi = self.outterElement.fi
        omg = self.outterElement.omg
        ka = self.outterElement.ka
        a1 = cos(fi) * cos(ka) - sin(fi) * sin(omg) * sin(ka)
        a2 = -cos(fi) * sin(ka) - sin(fi) * sin(omg) * cos(ka)
        a3 = -sin(fi) * cos(omg)
        b1 = cos(omg) * sin(ka)
        b2 = cos(omg) * cos(ka)
        b3 = -sin(omg)
        c1 = sin(fi) * cos(ka) + cos(fi) * sin(omg) * sin(ka)
        c2 = -sin(fi) * sin(ka) + cos(fi) * sin(omg) * cos(ka)
        c3 = cos(fi) * cos(omg)

        self.R = np.array(
            [[a1, a2, a3],
             [b1, b2, b3],
             [c1, c2, c3]]
        )

    def process(self):
        self.get_RotationMatrix()

        for i in range(len(self.ppList)):
            groundPoint = self.gpList[i]
            photoPoint = self.ppList[i]
            l = getMatrix_L(groundPoint, photoPoint, self.outterElement, self.innerElement, self.R)

            a = getMatrix_A(groundPoint, photoPoint, self.outterElement, self.innerElement, self.R)
            self.A[2 * i:2 * i + 2, :] = a
            self.L[2 * i:2 * i + 2, :] = l

        tmp1 = np.linalg.inv(np.dot(self.A.T, self.A))
        tmp2 = np.dot(tmp1, self.A.T)
        X = np.dot(tmp2, self.L)
        self.X = X
        self.Update(X)

    def Update(self, X):
        self.outterElement.update(X)

    def is_Limit(self):
        t = self.X[3]
        w = self.X[4]
        k = self.X[5]
        if abs(t) < 0.01 and abs(w) < 0.01 and abs(k) < 0.01:
            return True
        else:
            return False

    def display(self):
        self.outterElement.display()

    def main(self):
        self.process()
        while not self.is_Limit():
            self.process()
        self.display()


if __name__ == '__main__':
    innerElement = InnerElement(0, 0, 153.24 / 1000.0)

    gp1 = GroundPoint(36589.41, 25273.32, 2195.17)
    gp2 = GroundPoint(37631.08, 31324.51, 728.69)
    gp3 = GroundPoint(39100.97, 24934.98, 2386.50)
    gp4 = GroundPoint(40426.54, 30319.81, 757.31)

    pp1 = PhotoPoint(-86.15, -68.99)
    pp2 = PhotoPoint(-53.40, 82.21)
    pp3 = PhotoPoint(-14.78, -76.63)
    pp4 = PhotoPoint(10.46, 64.43)

    Sovle(innerElement, gp1, gp2, gp3, gp4, pp1, pp2, pp3, pp4).main()
