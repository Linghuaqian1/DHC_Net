#!/user/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy

import torch
from torch import nn


class BatchNormm2D(nn.Module):
    def __init__(self, num_channels, epsilon=1e-5, momentum=0.9, rescale=True):
        super(BatchNormm2D, self).__init__()
        self.num_channels = num_channels
        self.epsilon = epsilon
        self.momentum = momentum
        self.rescale = rescale

        if (self.rescale == True):
            # define parameters gamma, beta which are learnable
            # dimension of gamma and beta should be (num_channels) ie its a one dimensional vector
            # initializing gamma as ones vector and beta as zeros vector (implies no scaling/shifting at the start)
            self.gamma = nn.Parameter(torch.ones(num_channels))
            self.beta = nn.Parameter(torch.zeros(num_channels))
        # define parameters running mean and variance which is not learnable
        # keep track of mean and variance(but donot learn them), momentum is used which weighs current batch-mean and
        # variance with the running mean and variance using (momentum*runningmean+(1-momentum)*currentmean)
        self.register_buffer('runningmean', torch.zeros(num_channels))
        self.register_buffer('runningvar', torch.ones(num_channels))

    def forward(self, x):
        assert x.shape[1] == self.num_channels
        assert len(x.shape) == 4  # 4 because (batchsize, numchannels, height, width)

        if (self.training):
            # calculate mean and variance along the dimensions other than the channel dimension
            # variance calculation is using the biased formula during training
            variance = torch.var(x, dim=[0, 2, 3], unbiased=False)
            mean = torch.mean(x, dim=[0, 2, 3])
            self.runningmean.mul_(self.momentum).add_((1 - self.momentum) * mean.detach())
            self.runningvar.mul_(self.momentum).add_((1 - self.momentum) * variance.detach())
            out = (x - mean.view([1, self.num_channels, 1, 1])) / torch.sqrt(
                variance.view([1, self.num_channels, 1, 1]) + self.epsilon)
        else:
            m = x.shape[0] * x.shape[2] * x.shape[3]
            out = (x - self.runningmean.view([1, self.num_channels, 1, 1])) / torch.sqrt(
                (m / (m - 1)) * self.runningvar.view([1, self.num_channels, 1, 1]) + self.epsilon)
            # during testing just use the running mean and (UnBiased) variance
        if (self.rescale == True):
            return out


class LayerNormm2D(nn.Module):
    def __init__(self, num_channels, epsilon=1e-5):
        super(LayerNormm2D, self).__init__()
        self.num_channels = num_channels
        self.epsilon = epsilon

        self.gamma = nn.Parameter(torch.ones(num_channels))
        self.beta = nn.Parameter(torch.zeros(num_channels))

    def forward(self, x):
        assert list(x.shape)[1] == self.num_channels
        assert len(x.shape) == 4  # 4 because len((batchsize, numchannels, height, width)) = 4
        variance, mean = torch.var(x, dim=[1, 2, 3], unbiased=False), torch.mean(x, dim=[1, 2, 3])

        out = (x - mean.view([-1, 1, 1, 1])) / torch.sqrt(variance.view([-1, 1, 1, 1]) + self.epsilon)
        return out


class LayerBatchNorm(nn.Module):
    def __init__(self, num_channels, epsilon=1e-5, momentum=0.9):
        super(LayerBatchNorm, self).__init__()
        self.num_channels = num_channels
        self.epsilon = epsilon
        self.momentum = momentum
        self.Batchh = BatchNormm2D(self.num_channels, epsilon=self.epsilon)
        self.layeer = LayerNormm2D(self.num_channels, epsilon=self.epsilon)
        # The BCN variable to be learnt
        self.BCN_var = nn.Parameter(torch.ones(self.num_channels))
        # Gamma and Beta for rescaling
        self.gamma = nn.Parameter(torch.ones(num_channels))
        self.beta = nn.Parameter(torch.zeros(num_channels))

    def forward(self, x):
        X = self.Batchh(x)
        Y = self.layeer(x)
        out = self.BCN_var.view([1, self.num_channels, 1, 1]) * X + (
                1 - self.BCN_var.view([1, self.num_channels, 1, 1])) * Y
        out = self.gamma.view([1, self.num_channels, 1, 1]) * out + self.beta.view([1, self.num_channels, 1, 1])
        return out


