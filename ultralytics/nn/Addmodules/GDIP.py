import math
import warnings

import numpy as np
import torch
import torchvision
#from PIL.Image import Image
import cv2
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')


class GatedDIP(torch.nn.Module):
    """_summary_
    Args:
        torch (_type_): _description_
    """

    def __init__(self,
                 encoder_output_dim=256,
                 num_of_gates=7):
        """_summary_
        Args:
            encoder_output_dim (int, optional): _description_. Defaults to 256.
            num_of_gates (int, optional): _description_. Defaults to 7.
        """
        super(GatedDIP, self).__init__()
        # Encoder Model
        self.encoder = torchvision.models.vgg16(pretrained=False)

        # Changed 4096 --> 256 dimension
        self.encoder.classifier[6] = torch.nn.Linear(4096, encoder_output_dim, bias=True)

        # Gating Module
        self.gate_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, num_of_gates, bias=True))

        # White-Balance Module
        self.wb_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 3, bias=True))

        # Gamma Module
        self.gamma_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 1, bias=True))

        # Sharpning Module
        self.gaussian_blur = torchvision.transforms.GaussianBlur(13, sigma=(0.1, 5.0))
        self.sharpning_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 1, bias=True))

        # De-Fogging Module
        self.defogging_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 1, bias=True))

        # Contrast Module
        self.contrast_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 1, bias=True))

        # Contrast Module
        self.tone_module = torch.nn.Sequential(torch.nn.Linear(encoder_output_dim, 8, bias=True))

    def rgb2lum(self, img):
        """_summary_
        Args:
            img (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        img = 0.27 * img[:, 0, :, :] + 0.67 * img[:, 1, :, :] + 0.06 * img[:, 2, :, :]
        return img

    def lerp(self, a, b, l):
        return (1 - l.unsqueeze(2).unsqueeze(3)) * a + l.unsqueeze(2).unsqueeze(3) * b

    def dark_channel(self, x):
        """_summary_
        Args:
            x (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        z = x.min(dim=1)[0].unsqueeze(1)
        return z

    def atmospheric_light(self, x, dark, top_k=1000):
        """_summary_
        Args:
            x (torch.tensor): _description_
            top_k (int, optional): _description_. Defaults to 1000.
        Returns:
            _type_: _description_
        """
        h, w = x.shape[2], x.shape[3]
        imsz = h * w
        numpx = int(max(math.floor(imsz / top_k), 1))
        darkvec = dark.reshape(x.shape[0], imsz, 1)
        imvec = x.reshape(x.shape[0], 3, imsz).transpose(1, 2)
        indices = darkvec.argsort(1)
        indices = indices[:, imsz - numpx:imsz]
        atmsum = torch.zeros([x.shape[0], 1, 3]).cuda()
        for b in range(x.shape[0]):
            for ind in range(1, numpx):
                atmsum[b, :, :] = atmsum[b, :, :] + imvec[b, indices[b, ind], :]
        a = atmsum / numpx
        a = a.squeeze(1).unsqueeze(2).unsqueeze(3)
        return a

    def blur(self, x):
        """_summary_
        Args:
            x (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        return self.gaussian_blur(x)

    def defog(self, x, latent_out, fog_gate):
        """Defogging module is used for removing the fog from the image using ASM
        (Atmospheric Scattering Model).
        I(X) = (1-T(X)) * J(X) + T(X) * A(X)
        I(X) => image containing the fog.
        T(X) => Transmission map of the image.
        J(X) => True image Radiance.
        A(X) => Atmospheric scattering factor.
        Args:
            x (torch.tensor): Input image I(X)
            latent_out (torch.tensor): Feature representation from DIP Module.
            fog_gate (torch.tensor): Gate value raning from (0. - 1.) which enables defog module.
        Returns:
            torch.tensor : Returns defogged image with true image radiance.
        """
        omega = self.defogging_module(latent_out).unsqueeze(2).unsqueeze(3)
        omega = self.tanh_range(omega, torch.tensor(0.1), torch.tensor(1.))
        dark_i = self.dark_channel(x)
        a = self.atmospheric_light(x, dark_i)
        i = x / a
        i = self.dark_channel(i)
        t = 1. - (omega * i)
        j = ((x - a) / (torch.maximum(t, torch.tensor(0.01)))) + a
        j = (j - j.min()) / (j.max() - j.min())
        j = j * fog_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3)
        return j

    def white_balance(self, x, latent_out, wb_gate):
        """ White balance of the image is predicted using latent output of an encoder.
        Args:
            x (torch.tensor): Input RGB image.
            latent_out (torch.tensor): Output from the last layer of an encoder.
            wb_gate (torch.tensor): White-balance gate used to change the influence of color scaled image.
        Returns:
            torch.tensor: returns White-Balanced image.
        """
        log_wb_range = 0.5
        wb = self.wb_module(latent_out)
        wb = torch.exp(self.tanh_range(wb, -log_wb_range, log_wb_range))

        color_scaling = 1. / (1e-5 + 0.27 * wb[:, 0] + 0.67 * wb[:, 1] +
                              0.06 * wb[:, 2])
        wb = color_scaling.unsqueeze(1) * wb
        wb_out = wb.unsqueeze(2).unsqueeze(3) * x
        wb_out = (wb_out - wb_out.min()) / (wb_out.max() - wb_out.min())
        wb_out = wb_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3) * wb_out
        return wb_out

    def tanh01(self, x):
        """_summary_
        Args:
            x (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        return torch.tanh(x) * 0.5 + 0.5

    def tanh_range(self, x, left, right):
        """_summary_
        Args:
            x (torch.tensor): _description_
            left (float): _description_
            right (float): _description_
        Returns:
            _type_: _description_
        """
        return self.tanh01(x) * (right - left) + left

    def gamma_balance(self, x, latent_out, gamma_gate):
        """_summary_
        Args:
            x (torch.tensor): _description_
            latent_out (torch.tensor): _description_
            gamma_gate (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        log_gamma = torch.log(torch.tensor(2.5))
        gamma = self.gamma_module(latent_out).unsqueeze(2).unsqueeze(3)
        gamma = torch.exp(self.tanh_range(gamma, -log_gamma, log_gamma))
        g = torch.pow(torch.maximum(x, torch.tensor(1e-4)), gamma)
        g = (g - g.min()) / (g.max() - g.min())
        g = g * gamma_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3)
        return g

    def sharpning(self, x, latent_out, sharpning_gate):
        """_summary_
        Args:
            x (torch.tensor): _description_
            latent_out (torch.tensor): _description_
            sharpning_gate (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        out_x = self.blur(x)
        y = self.sharpning_module(latent_out).unsqueeze(2).unsqueeze(3)
        y = self.tanh_range(y, torch.tensor(0.1), torch.tensor(1.))
        s = x + (y * (x - out_x))
        s = (s - s.min()) / (s.max() - s.min())
        s = s * (sharpning_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3))
        return s

    def identity(self, x, out_x, identity_gate):
        """_summary_
        Args:
            x (torch.tensor): _description_
            identity_gate (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        g = identity_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3)
        x = (x * g) + ((torch.tensor(1.).cuda() - g) * out_x)
        return x

    def contrast(self, x, latent_out, contrast_gate):
        """_summary_
        Args:
            x (torch.tensor): _description_
            latent_out (torch.tensor): _description_
            contrast_gate (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        alpha = torch.tanh(self.contrast_module(latent_out))
        luminance = torch.minimum(torch.maximum(self.rgb2lum(x), torch.tensor(0.0)), torch.tensor(1.0)).unsqueeze(1)
        contrast_lum = -torch.cos(math.pi * luminance) * 0.5 + 0.5
        contrast_image = x / (luminance + 1e-6) * contrast_lum
        contrast_image = self.lerp(x, contrast_image, alpha)
        contrast_image = (contrast_image - contrast_image.min()) / (contrast_image.max() - contrast_image.min())
        contrast_image = contrast_image * contrast_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3)
        return contrast_image

    def tone(self, x, latent_out, tone_gate):
        """_summary_
        Args:
            x (torch.tensor): _description_
            latent_out (torch.tensor): _description_
            tone_gate (torch.tensor): _description_
        Returns:
            _type_: _description_
        """
        curve_steps = 8
        tone_curve = self.tone_module(latent_out).reshape(-1, 1, curve_steps)
        tone_curve = self.tanh_range(tone_curve, 0.5, 2)
        tone_curve_sum = torch.sum(tone_curve, dim=2) + 1e-30
        total_image = x * 0
        for i in range(curve_steps):
            total_image += torch.clamp(x - 1.0 * i / curve_steps, 0, 1.0 / curve_steps) \
                           * tone_curve[:, :, i].unsqueeze(2).unsqueeze(3)
        total_image *= curve_steps / tone_curve_sum.unsqueeze(2).unsqueeze(3)
        total_image = (total_image - total_image.min()) / (total_image.max() - total_image.min())
        total_image = total_image * tone_gate.unsqueeze(1).unsqueeze(2).unsqueeze(3)
        return total_image

    def forward(self, x):
        """_summary_
        Args:
            x (torch.Tensor): _description_
        Returns:
            _type_: _description_
        """
        latent_out = torch.nn.functional.relu_(self.encoder(x))
        gate = self.tanh_range(self.gate_module(latent_out), 0.01, 1.0)
        wb_out = self.white_balance(x, latent_out, gate[:, 0])
        gamma_out = self.gamma_balance(x, latent_out, gate[:, 1])
        sharpning_out = self.sharpning(x, latent_out, gate[:, 3])
        fog_out = self.defog(x, latent_out, gate[:, 4])
        contrast_out = self.contrast(x, latent_out, gate[:, 5])
        tone_out = self.tone(x, latent_out, gate[:, 6])
        out_x = wb_out + gamma_out + fog_out + sharpning_out + contrast_out + tone_out
        out_x = (out_x - out_x.min()) / (out_x.max() - out_x.min())
        x = self.identity(x, out_x, gate[:, 2])
        return x


if __name__ == '__main__':
    #------------------------------------------------------------
    def load_and_preprocess_image(image_path):
        img = cv2.open(image_path)
        img = img.resize((224, 224))  # 调整图片大小，根据你的模型需求进行调整
        img_array = np.array(img)
        img_array = img_array / 255.0  # 像素值归一化
        return img_array


    encoder_out_dim = 256
    image_path = "E:/LQYY/dataset/DOTA2-1024-split/images/train/P0010__1024__822___824.jpg"
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image
    transform = transforms.Compose([transforms.Resize((256, 256)),
                                    transforms.ToTensor()])
    image_tensor = transform(image).unsqueeze(0).cuda()

    # Create model instance
    model = GatedDIP(encoder_output_dim=encoder_out_dim).cuda()  # or AODnet()

    # Perform dehazing
    with torch.no_grad():
        output_tensor = model(image_tensor)

    # Convert output tensor to image
    output_image = transforms.ToPILImage()(output_tensor.squeeze(0))

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



    # image_path = 'E:/LQYY/dataset/DOTA2-1024-split/images/train/P0000__1024__1648___0.jpg'
    # img=load_and_preprocess_image(image_path)
    # img_array = np.expand_dims(img, axis=0)  # 增加 batch 维度
    # x = torch.from_numpy(img_array)
    # #--------------------------------------------------------------------
    # batch_size = 2
    # encoder_out_dim = 256
    # #x = torch.randn(1, 3, 640, 640).cuda()
    # x = (x - x.min()) / (x.max() - x.min())
    #
    # model = GatedDIP(encoder_output_dim=encoder_out_dim).cuda()
    # #print(model)
    # out = model(x)
    # print('out shape:', out.shape)

