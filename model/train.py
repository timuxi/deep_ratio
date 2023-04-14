import os.path

import numpy as np
import torch
import torchvision.models as models
from torch.utils.data import DataLoader

from model.Resnet import SatelliteDataset, getModel

ep = 100

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    model = getModel()

    # define a data loader for the satellite dataset
    path = 'data/train/npy'

    train_data = np.load(os.path.join(path, 'train_sat.npy'))
    train_labels = np.load(os.path.join(path, 'train_tag.npy'))
    val_data = np.load(os.path.join(path, 'val_sat.npy'))
    val_labels = np.load(os.path.join(path, 'val_tag.npy'))

    train_loader = DataLoader(SatelliteDataset(train_data, train_labels), batch_size=300, shuffle=True)
    val_loader = DataLoader(SatelliteDataset(val_data, val_labels), batch_size=300, shuffle=True)

    # define the loss function and optimizer
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss = 0
    # train the model
    for epoch in range(100):
        for batch in train_loader:
            optimizer.zero_grad()
            x, y = batch
            pre_y = model(x)
            loss = criterion(pre_y, y.flatten().long())
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_accuracy = 0
            for val_batch in val_loader:
                val_x, val_y = val_batch
                pre_y = model(val_x)
                pre_y = torch.argmax(pre_y, dim=1)
                val_accuracy += (pre_y == val_y.flatten()).sum().item()
            val_accuracy /= len(val_loader.dataset)
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| val accuracy: %.2f' % val_accuracy)
        model.train()

    torch.save(model.state_dict(), 'ration_model_3.pth')
