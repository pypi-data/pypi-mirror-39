# -*- coding: utf-8 -*-
# internal imports
import time

# external imports
import numpy as np
import torch
from torch.autograd import Variable
from tqdm import tqdm

# custom imports


class Wrapper(object):
    def __init__(self, model=None):
        self.model = model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    @staticmethod
    def _transfer_tensor(tensor):
        """ Static method to return any tensor to a numpy equivalent """
        return tensor.cpu().detach().numpy()
        
    def _run_epoch(self, loader, train=False, optimizer=None, criterion=None, verbose=True):
        """ Run a single epoch over the loader
        
        Args:
            loader: PyTorch Dataloader Object to iterate over
            train: Boolean, updates gradients in the model if set to True
            optimizer: PyTorch optimizer to use when performing backprop
            criterion: Loss function
        Returns:
            An numpy array of the predictions made during this epoch
        """
        self.model.train() if train else self.model.eval()  # set model into correct mode
        y_hats = []  # placeholder for the predictions made during this epocha
        # iterate over the dataset
        pbar = tqdm(loader)
        for idx, (X, y) in enumerate(pbar):
            if train: optimizer.zero_grad()
            # create variables and predict
            X = Variable(X).to(self.device)
            y = Variable(y).to(self.device)
            y_hat = self.model(X)
            y_hats.append(self._transfer_tensor(y_hat).flatten())
            # update grads if training
            if train:
                loss = criterion(y_hat, y)
                loss.backward()
                optimizer.step()
                if verbose: pbar.set_description('Loss {}'.format(round(loss.item(), 4)))
        return np.array(y_hats)  # return all the predictions for this epoch
            
    def set_model(self, model):
        """ Set the classes' model """
        self.model = model
        
    def get_model(self, model):
        """ Get the model from the class """
        return self.model
        
    def fit(self, train_loader, optimizer, criterion, epochs=10, val_loader=None, verbose=2):
        """ Fit function for the model
        
        Args:
            train_loader: The PyTorch DataLoader object for the training data
            optimizer: PyTorch optimizer to use for the backprop
            citerion: Function to calculate the loss
            epochs: Number of epoch to train for
            val_loader: PyTorch DataLoader object for the validation data
        """
        # set up verbose output
        verbosity = True if verbose > 1 else False
        pbar = tqdm(range(1, epochs+1))
        if verbose == 0:
            pbar.disable = True
        # run the training process
        for epoch in pbar:
            pbar.set_description('Epoch {}'.format(epoch))
            y_hats = self._run_epoch(train_loader, 
                                     train=True, 
                                     optimizer=optimizer, 
                                     criterion=criterion, 
                                     verbose=verbosity)
            if val_loader:
                self._run_epoch(val_loader, verbose=verbosity)
        return y_hats