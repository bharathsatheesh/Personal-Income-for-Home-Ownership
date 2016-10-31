import scipy.io
from math import log
import csv

#Data Extraction
attributes = list(range(32))
spamData = scipy.io.loadmat('spam_data.mat')
trainData = spamData['training_data']
trainLabels = list(spamData['training_labels'][0])
testData = spamData['test_data']

Labels = scipy.io.loadmat('spam_test_labels.mat')['spam_test_labels']
testLabels = []
for i in range(len(Labels)):
    testLabels.append(Labels[i][0])
testLabels += [0]
#Data Processing
temp = []
for i in range(len(trainData)):
    temp.append(list(trainData[i]))

trainData = temp
temp = []
for i in range(len(testData)):
    temp.append(list(testData[i]))

testData = temp
examples = []
for i in range(len(trainData)):
    examples.append((trainData[i], trainLabels[i]))

testExamples = []
for i in range(len(testData)):
    testExamples.append((testData[i], testLabels[i]))

rangeVals = [[] for _ in attributes]
for attribute in attributes:
    for i in range(len(trainData)):
        rangeVals[attribute].append(trainData[i][attribute])
    rangeVals[attribute] = list(set(rangeVals[attribute]))

# Functions and Class
NUM_FEATURES = 32

class Tree:
    def __init__(self, rootVal, threshold, isLeaf):
        self.rootVal = rootVal
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.right = None
        self.left = None


def same_class(examples):
    init_label = examples[0][1]
    for (data, label) in examples:
        if label != init_label:
            return False, None
    return True, init_label


def majority(examples):
    labels = {}
    for (data, label) in examples:
        labels[label] = 0
    for (data, label) in examples:
        labels[label] += 1

    bestLabelCount = -1
    bestLabel = None
    for label in labels:
        if labels[label] > bestLabelCount:
            bestLabelCount = labels[label]
            bestLabel = label

    return bestLabel


def entropy(examples, attribute, threshold):
    p_l, n_l, p_r, n_r = 0, 0, 0, 0
    for example in examples:
        if example[0][attribute] > threshold:
            if example[0]:
                p_r += 1
            else:
                n_r += 1
        else:
            if example[0]:
                p_l += 1
            else:
                n_l += 1

    if p_l == 0 or n_l == 0:
        left_entropy = 0
    else:
        left_entropy = -(
            (p_l / (p_l + n_l)) * log((p_l / (p_l + n_l))) + (1 - (p_l / (p_l + n_l))) * log(
                (1 - (p_l / (p_l + n_l)))))
    if p_r == 0 or n_r == 0:
        right_entropy = 0
    else:
        right_entropy = -(
            (p_r / (p_r + n_r)) * log((p_r / (p_r + n_r))) + (1 - (p_r / (p_r + n_r))) * log(
                (1 - (p_r / (p_r + n_r)))))

    return ((p_l + n_l) * left_entropy + (p_r + n_r) * right_entropy) / (p_l + n_l + p_r + n_r)


def argmin(attributes, entropy, examples):
    bestEntropy = 100000000000000000000000
    bestCombination = None
    for attribute in attributes:
        for threshold in rangeVals[attribute]:
            tmpEntropy = entropy(examples, attribute, threshold)
            if tmpEntropy < bestEntropy:
                bestEntropy = tmpEntropy
                bestCombination = (attribute, threshold)
    return bestCombination


def makeDecisionTree(examples, attributes, parent_examples):
    if not examples:
        return Tree(majority(parent_examples), None, True)

    is_same_class, class_val = same_class(examples)
    if is_same_class:
        return Tree(class_val, None, True)

    if not attributes or len(examples) <= 15:
        return Tree(majority(examples), None, True)

    A, T = argmin(attributes, entropy, examples)
    tree = Tree(A, T, False)
    right, left = [], []
    for example in examples:
        if example[0][A] > T:
            right.append(example)
        else:
            left.append(example)
    new_attributes = []
    for attr in attributes:
        if attr != A:
            new_attributes.append(attr)

    tree.left = makeDecisionTree(left, new_attributes, examples)
    tree.right = makeDecisionTree(right, new_attributes, examples)
    return tree


def predict(decisionTree, data):
    if decisionTree.isLeaf:
        return decisionTree.rootVal
    if data[decisionTree.rootVal] > decisionTree.threshold:
        return predict(decisionTree.right, data)
    else:
        return predict(decisionTree.left, data)

prediction = []
def accuracy(validationExamples, examples, attributes):
    decisionTree = makeDecisionTree(examples, attributes, None)
    correctPrediction = 0
    for (data, label) in validationExamples:
        tmp = predict(decisionTree, data)
        prediction.append(tmp)
        if label == tmp:
            correctPrediction += 1

    return decisionTree, correctPrediction / (len(validationExamples) + 0.0)

# Final Scripts
tree, accuracy_rate = accuracy(testExamples, examples, attributes)
print(accuracy_rate)
# Q(d)

data = testData[0]
decisions = []
def modPredict(decisionTree, data):
    if decisionTree.isLeaf:
        return decisionTree.rootVal
    if data[decisionTree.rootVal] > decisionTree.threshold:
        decisions.append("feature " + str(1+decisionTree.rootVal) + " > " + str(decisionTree.threshold))
        return modPredict(decisionTree.right, data)
    else:
        decisions.append("feature " + str(1+decisionTree.rootVal) + " <= " + str(decisionTree.threshold))
        return modPredict(decisionTree.left, data)

modPredict(tree, data)
print(decisions)
