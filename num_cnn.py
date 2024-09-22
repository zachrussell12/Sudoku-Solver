import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim

class LeNet_5(nn.Module):

    def __init__(self):

        super(LeNet_5, self).__init__()

        self.c1 = nn.Sequential(nn.Conv2d(1,6,5,1,2), nn.ReLU(), nn.MaxPool2d(2,2))
        self.c2 = nn.Sequential(nn.Conv2d(6,16,5), nn.ReLU(), nn.MaxPool2d(2,2))

        self.flatten = nn.Flatten()

        self.layer1 = nn.Linear(400, 120)
        self.layer2 = nn.Linear(120, 84)
        self.layer3 = nn.Linear(84, 10)

        def forward(self, node):

            node = self.c1(node)

            node = self.c2(node)

            node = self.flatten(node)

            node = self.layer1(node)
            node = F.relu(node)

            node = self.layer2(node)
            node = F.relu(node)

            node = self.layer3(node)

            return F.softmax(node, 1)
        
LeNet_5_model = LeNet_5()

sgd = optim.SGD(LeNet_5_model.parameters(), lr=0.01, momentum=0.9, weight_decay=4e-5, nesterov=True)
loss_function = nn.CrossEntropyLoss()


