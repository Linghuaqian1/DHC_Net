import cv2
import torch
import torch.nn as nn
import math

import torchvision
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms

class unfog_net(nn.Module):
    GT = torch.zeros((1, 3, 1024, 1024))
    defog = torch.zeros((1, 3, 1024, 1024))


    def __init__(self):
        super(unfog_net, self).__init__()

        self.relu = nn.ReLU(inplace=True)

        self.e_conv1 = nn.Conv2d(3, 3, 1, 1, 0, bias=True)
        self.e_conv2 = nn.Conv2d(3, 3, 3, 1, 1, bias=True)
        self.e_conv3 = nn.Conv2d(6, 3, 5, 1, 2, bias=True)
        self.e_conv4 = nn.Conv2d(6, 3, 7, 1, 3, bias=True)
        self.e_conv5 = nn.Conv2d(12, 3, 3, 1, 1, bias=True)

    def forward(self, x):


        # print(x.shape)

        unfog_net.GT = x
        x1 = self.relu(self.e_conv1(x))
        x2 = self.relu(self.e_conv2(x1))

        concat1 = torch.cat((x1, x2), 1)
        x3 = self.relu(self.e_conv3(concat1))

        concat2 = torch.cat((x2, x3), 1)
        x4 = self.relu(self.e_conv4(concat2))

        concat3 = torch.cat((x1, x2, x3, x4), 1)
        x5 = self.relu(self.e_conv5(concat3))

        clean_image = self.relu((x5 * x) - x5 + 1)

        unfog_net.defog=clean_image

        #torchvision.utils.save_image(torch.cat((x, clean_image), 0), 'E:/yyj_file/ultralytics-main/runscode/1.png')

        return clean_image

class unfog_M(nn.Module):



    def __init__(self):
        super(unfog_M, self).__init__()
        self.unfog_net = unfog_net()





    def forward(self, x):

        # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #x=x.to('cuda')
        #print(x)
        dehaze_net = self.unfog_net

        #dehaze_net.to(device)
        dehaze_net.load_state_dict(torch.load('E:/yyj_file/ultralytics-main/weight/dehazer.pthEpoch9.pth'))
        clean_image= dehaze_net(x)
        torchvision.utils.save_image(torch.cat((x, clean_image), 0), 'E:/yyj_file/ultralytics-main/runscode/2.png')





        return clean_image


if __name__ == "__main__":
    # Generating Sample image
    # image_size = (1, 3, 640, 640)
    # image = torch.rand(*image_size)
    # print(image)
    # #image_path='E:/LQYY/dataset/DOTA2-1024-split/fog_images/train/P0020__1024__3296___824.jpg'
    # #image = cv2.imread(image_path)
    # #cv2.imshow("image", image)
    # out = unfog_net()
    # out = out(image)
    # #cv2.imshow("image", image)
    # print(out.size())
    # print(out)

    image_path = "E:/LQYY/dataset/DOTA2-1024-split/images/train/P0010__1024__822___824.jpg"
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image
    transform = transforms.Compose([transforms.Resize((256, 256)),
                                    transforms.ToTensor()])
    image_tensor = transform(image).unsqueeze(0)

    # Create model instance
    model = unfog_net()  # or AODnet()

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