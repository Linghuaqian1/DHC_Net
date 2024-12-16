import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch
from PIL import Image
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
torch.autograd.set_detect_anomaly(True)
__all__ = ['AOD_pono_net']


class AODnet(nn.Module):
    def __init__(self):
        super(AODnet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=1, stride=1, padding=0)
        self.conv2 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=6, out_channels=3, kernel_size=5, stride=1, padding=2)
        self.conv4 = nn.Conv2d(in_channels=6, out_channels=3, kernel_size=7, stride=1, padding=3)
        self.conv5 = nn.Conv2d(in_channels=12, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.b = 1

    def forward(self, x):
        x1 = F.relu(self.conv1(x))
        x2 = F.relu(self.conv2(x1))
        cat1 = torch.cat((x1, x2), 1)
        x3 = F.relu(self.conv3(cat1))
        cat2 = torch.cat((x2, x3), 1)
        x4 = F.relu(self.conv4(cat2))
        cat3 = torch.cat((x1, x2, x3, x4), 1)
        k = F.relu(self.conv5(cat3))

        if k.size() != x.size():
            raise Exception("k, haze image are different size!")

        output = k * x - k + self.b
        return F.relu(output)


class AOD_pono_net(nn.Module):
    def __init__(self):
        super(AOD_pono_net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=1, stride=1, padding=0)
        self.conv2 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=6, out_channels=3, kernel_size=5, stride=1, padding=2)
        self.conv4 = nn.Conv2d(in_channels=6, out_channels=3, kernel_size=7, stride=1, padding=3)
        self.conv5 = nn.Conv2d(in_channels=12, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.b = 1

        self.pono = PONO(affine=False)
        self.ms = MS()

    def forward(self, x):
        x1 = F.relu(self.conv1(x))
        x2 = F.relu(self.conv2(x1))
        cat1 = torch.cat((x1, x2), 1)
        x1, mean1, std1 = self.pono(x1)
        x2, mean2, std2 = self.pono(x2)
        x3 = F.relu(self.conv3(cat1))
        cat2 = torch.cat((x2, x3), 1)
        x3 = self.ms(x3, mean1, std1)
        x4 = F.relu(self.conv4(cat2))
        x4 = self.ms(x4, mean2, std2)
        cat3 = torch.cat((x1, x2, x3, x4), 1)
        k = F.relu(self.conv5(cat3))

        if k.size() != x.size():
            raise Exception("k, haze image are different size!")

        output = k * x - k + self.b
        output = F.relu(output)
        return output


class PONO(nn.Module):
    def __init__(self, input_size=None, return_stats=False, affine=True, eps=1e-5):
        super(PONO, self).__init__()
        self.return_stats = return_stats
        self.input_size = input_size
        self.eps = eps
        self.affine = affine

        if affine:
            self.beta = nn.Parameter(torch.zeros(1, 1, *input_size))
            self.gamma = nn.Parameter(torch.ones(1, 1, *input_size))
        else:
            self.beta, self.gamma = None, None

    def forward(self, x):
        mean = x.mean(dim=1, keepdim=True)
        std = (x.var(dim=1, keepdim=True) + self.eps).sqrt()
        x = (x - mean) / std
        if self.affine:
            x = x * self.gamma + self.beta
        return x, mean, std


class MS(nn.Module):
    def __init__(self, beta=None, gamma=None):
        super(MS, self).__init__()
        self.gamma, self.beta = gamma, beta

    def forward(self, x, beta=None, gamma=None):
        beta = self.beta if beta is None else beta
        gamma = self.gamma if gamma is None else gamma
        if gamma is not None:
            y = x.mul(gamma)  # 使用非原地操作mul
        else:
            y = x  # 如果不乘gamma，保持y不变
        if beta is not None:
            y = y.add(beta)  # 使用非原地操作add

        return y


if __name__ == "__main__":
    # Generating Sample image
    # image_size = (1, 3, 640, 640)
    # path='E:/yyj_file/datasets/DOTA2.0obb/DOTA2-1024-split/images/train/P0000__1024__824___0.jpg'
    # im0 = cv2.imread(path)
    # print(im0.shape)
    # image = torch.rand(*image_size)
    # out = AOD_pono_net()
    # out = out(image)
    #
    # print(out.size())

    image_path = "E:/LQYY/dataset/DOTA2-1024-split/images/train/P0010__1024__822___824.jpg"
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image
    transform = transforms.Compose([transforms.Resize((256, 256)),
                                    transforms.ToTensor()])
    image_tensor = transform(image).unsqueeze(0)

    # Create model instance
    model = AOD_pono_net()  # or AODnet()

    # Perform dehazing
    with torch.no_grad():
        output_tensor = model(image_tensor)

    # Convert output tensor to image
    output_image = transforms.ToPILImage()(output_tensor.squeeze(0).cpu())

    # Display the dehazed image
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(image)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Dehazed Image')
    plt.imshow(output_image)
    plt.axis('off')
    plt.show()

