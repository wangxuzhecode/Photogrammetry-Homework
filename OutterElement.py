class OutterElement:
    """
        :param Xs
        :param Ys
        :param Zs
        :param fi
        :param omg
        :param ka
    """

    def __init__(self):
        self.Xs = 0
        self.Ys = 0
        self.Zs = 0
        self.fi = 0.0
        self.omg = 0.0
        self.ka = 0.0

    def update(self, X):
        self.Xs += X[0]
        self.Ys += X[1]
        self.Zs += X[2]
        self.fi += X[3]
        self.omg += X[4]
        self.ka += X[5]

    def display(self):
        print('Xs:', self.Xs)
        print('Ys:', self.Ys)
        print('Zs:', self.Zs)
        print('fi:', self.fi)
        print('omg:', self.omg)
        print('ka:', self.ka)
