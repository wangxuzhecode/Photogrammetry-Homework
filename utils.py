from math import cos, sin
import numpy as np


def getMatrix_L(groundPoint, photoPoint, outterElement, innerElement, R):
    """

    :param groundPoint:
    :param photoPoint:
    :param outterElement:
    :param innerElement:
    :param R:
    :return:
    """
    xx = -innerElement.f * (
            R[0][0] * (groundPoint.X - outterElement.Xs) + R[1][0] * (groundPoint.Y - outterElement.Ys) + R[2][0]
            * (groundPoint.Z - outterElement.Zs)) / \
         (R[0][2] * (groundPoint.X - outterElement.Xs) + R[1][2] * (groundPoint.Y - outterElement.Ys) + R[2][2] *
          (groundPoint.Z - outterElement.Zs))

    yy = -innerElement.f * (
            R[0][1] * (groundPoint.X - outterElement.Xs) + R[1][1] * (groundPoint.Y - outterElement.Ys) + R[2][1]
            * (groundPoint.Z - outterElement.Zs)) / \
         (R[0][2] * (groundPoint.X - outterElement.Xs) + R[1][2] * (groundPoint.Y - outterElement.Ys) + R[2][2] *
          (groundPoint.Z - outterElement.Zs))

    lx = photoPoint.x - xx
    ly = photoPoint.y - yy
    if type(lx) is np.ndarray:
        lx = lx[0]
        ly = ly[0]
    matrix_l = np.array([[lx], [ly]])
    return matrix_l


def getMatrix_A(groundPoint, photoPoint, outterElement, innerElement, R):
    """

    :param groundPoint:
    :param photoPoint:
    :param outterElement:
    :param innerElement:
    :param R:
    :return:
    """
    Z = R[0][2] * (groundPoint.X - outterElement.Xs) + R[1][2] * (groundPoint.Y - outterElement.Ys) + R[2][2] * (
            groundPoint.Z - outterElement.Zs)
    f = innerElement.f
    x = photoPoint.x
    y = photoPoint.y
    omg = outterElement.omg
    ka = outterElement.ka
    a11 = (R[0][0] * f + R[0][2] * x) / Z
    a12 = (R[1][0] * f + R[1][2] * x) / Z
    a13 = (R[2][0] * f + R[2][2] * x) / Z
    a21 = (R[0][1] * f + R[0][2] * y) / Z
    a22 = (R[1][1] * f + R[1][2] * y) / Z
    a23 = (R[2][1] * f + R[2][2] * y) / Z

    a14 = y * sin(omg) - (x * (x * cos(ka) - y * sin(ka)) / f + f * cos(ka)) * cos(omg)
    a15 = -f * sin(ka) - x * (x * sin(ka) + y * cos(ka)) / f
    a16 = y
    a24 = -x * sin(omg) - (y * (x * cos(ka) - y * sin(ka)) / f - f * sin(ka)) * cos(omg)
    a25 = -f * cos(ka) - (y * (x * sin(ka) + y * cos(ka))) / f
    a26 = -x

    matrix_a = np.array(
        [[a11, a12, a13, a14, a15, a16],
         [a21, a22, a23, a24, a25, a26]],
        dtype=object)
    return matrix_a
