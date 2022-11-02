import struct
from NN import *


# 导入训练集
def load_minist(labels_path, images_path):
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)

    with open(images_path, "rb") as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
    return images, labels


images, labels = load_minist('mnist/train-labels.idx1-ubyte', 'mnist/train-images.idx3-ubyte')
test_images, test_labels = load_minist('mnist/t10k-labels.idx1-ubyte', 'mnist/t10k-images.idx3-ubyte')

labels = label_binarizer(labels)

nn = NeuralNetwork([784, 250, 10], 'logistic')

nn.fit(images, labels)
