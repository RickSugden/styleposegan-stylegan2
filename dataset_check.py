import torch
from torchvision import transforms
import PIL

from datasets import DeepFashionDataset
from torch.utils.data import DataLoader


def main():
    data_path = "./data/TrainingData"
    batch_size = 4
    num_workers = 1
    image_size = (512, 512)

    dataset = DeepFashionDataset(data_path, image_size=image_size)
    dataloader = DataLoader(
        dataset, batch_size=batch_size, num_workers=num_workers)

    batch = next(iter(dataloader))
    # x, y = batch, so x is  the tuple, and y is the triplet
    (I_s, P_s, A_s), (I_t, P_t) = batch
    for i in range(batch_size):
        print(I_s[i].size())
        im = transforms.ToPILImage()(I_s[i]).convert("RGB")
        im.show("Source Image")

        print(P_s[i].size())
        im = transforms.ToPILImage()(P_s[i]).convert("RGB")
        im.show("Source Pose Map")

        print(A_s[i].size())
        im = transforms.ToPILImage()(A_s[i]).convert("RGB")
        im.show("Source Texture Map")

        print(I_t[i].size())
        im = transforms.ToPILImage()(I_t[i]).convert("RGB")
        im.show("Target Image")

        print(P_t[i].size())
        im = transforms.ToPILImage()(P_t[i]).convert("RGB")
        im.show("Target Pose Map")

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
