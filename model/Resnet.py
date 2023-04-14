import torch
import torchvision.models as models
from torch.utils.data import Dataset


def getModel():
    # load the pre-trained ResNet-18 model
    model = models.resnet18(pretrained=False)
    model.conv1 = torch.nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    # modify the last layer to output 100 classes
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    model = model.to(torch.float64)
    for param in model.parameters():
        param.requires_grad = True
        param.data = param.data.to(torch.float64)
        if param.grad is not None:
            param.grad.data = param.grad.data.to(torch.float64)
    return model


class SatelliteDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        x = torch.from_numpy(x).type(torch.float64)
        y = self.labels[idx]
        return x, y
