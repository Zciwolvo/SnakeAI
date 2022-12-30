import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize) -> None:
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, fileName="Model.pth"):
        modelFolderPath = "./model"
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)
        
        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)



class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def TrainStep(self, state, action, reward, nextState, done):
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, ) #tuple conversion

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Qnew = reward[idx]
            if not done[idx]:
                Qnew = reward[idx] + self.gamma * torch.max(self.model(nextState[idx]))

            target[idx][torch.argmax(action).item()] = Qnew

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

