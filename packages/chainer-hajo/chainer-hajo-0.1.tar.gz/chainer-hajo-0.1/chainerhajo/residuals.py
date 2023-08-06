import chainer
import chainer.functions as F
import chainer.links as L


class ClassifyModify(chainer.Chain):
    def __init__(self, n_inout, ksize=1, stride=1, pad=0, dilate=1, initialW=None):
        super(ClassifyModify, self).__init__()
        with self.init_scope():
            self.c1 = L.Convolution2D(n_inout, n_inout, ksize=ksize, stride=stride, pad=pad, dilate=dilate, initialW=initialW)
            self.c2 = L.Convolution2D(n_inout, n_inout, ksize=ksize, stride=stride, pad=pad, dilate=dilate, initialW=initialW)

    def __call__(self, x):
        return x + self.c2(F.elu(self.c1(x)))


class ClassifyModifyChain(chainer.Chain):
    def __init__(self, n_inout, iterations=3, ksize=1, stride=1, pad=0, dilate=1, initialW=None):
        super(ClassifyModifyChain, self).__init__()
        with self.init_scope():
            self.iterations = []
            for i in range(iterations):
                child = ClassifyModify(n_inout, ksize=ksize, stride=stride, pad=pad, dilate=dilate, initialW=initialW)
                setattr(self, 'it{0:2d}'.format(i), child)
                self.iterations.append(child)

    def __call__(self, x):
        for _, child in enumerate(self.iterations):
            x = child(x)
        return x


class ClassifyModifySequence(chainer.Chain):
    def __init__(self, n_inout, ksize=(3, 3, 3), stride=(1, 1, 1), pad=(16, 4, 1), dilate=(16, 4, 1), initialW=None):
        super(ClassifyModifySequence, self).__init__()
        with self.init_scope():
            self.iterations = []
            for i,_ in enumerate(ksize):
                child = ClassifyModify(n_inout, ksize=ksize[i], stride=stride[i], pad=pad[i], dilate=dilate[i], initialW=initialW)
                setattr(self, 'it{0:2d}'.format(i), child)
                self.iterations.append(child)

    def __call__(self, x):
        for _, child in enumerate(self.iterations):
            x = child(x)
        return x

