# StylePoseGAN Implementation for Photoshoot
2020-2021 Startup Project where we were building a consumer app that generates completely new, high-quality photos of users for social media profiles. 

Our approach was based on a paper before its code was released: "Style and Pose Control for Image Synthesis of Humans from a Single Monocular View" Sarkar et al 2021.

In our implementation, we forked Lucidrains implementation of StyleGAN2. We also used Meta's DensePose through Detectron2.

## Project Overview
Taking good photos is hard. With the rising importance of having high-quality (HQ) portraits and photos in today's digital world, we sought to provide users with photorealistic images of themselves for their digital profiles. We called this project Photoshoot AI (before several groups were using that name. 

In 2021, Sarkar et al. proposed a DL model known as _StyleposeGAN_. The theoretical assumption of this paper was that a portrait can be thought of as two components: 1) the pose, how the person is oriented in 3D space, and 2) the texture, how their appearance reflects their identity. See here:

**Portraits consist of Pose and Texture**
![SPGAN_fig1 drawio (1)](https://github.com/photoshootai/styleposgan-stylegan2/assets/41484082/944242a7-8d26-445a-a391-88a22ba41009)
Samples from our implementation. A. Sample portrait B. "pose map" extracted by densepose (a DL model) C. Texture map extracted by a separate algorithm that models the images as a mesh and maps each body part to a specific part of the SMPL texture map.

**StyleposeGAN combines Pose and Texture to Reconstruct original Image**
![SPGAN_architecture drawio](https://github.com/photoshootai/styleposgan-stylegan2/assets/41484082/a4ca8721-e4fb-47c4-b837-ff861e10878a)
StyleposeGAN Architecture. 
A. Densepose Map is fed into a CNN feature extractor "PNet" which encodes the pose into a 3D Tensor.
B. SMPL Texture Map is fed into a separate CNN feature extractor "ANet" which encodes the appearance (texture) into a vector.
C. The core functionality of StyleposeGAN is GNet, a generative adversarial network (GAN) that aims to reconstruct the original image. Quality is enforced by a discriminator network, while identity is maintained with a face loss, L1 and VGG loss both enforce the model to pose the person correctly. 

#### Our product idea was to take in users' texture map, but replace their pose with that of a professional model. At the click of a button, our app would choose a random pose, and the network would then produce an image of the user, posed like a model. We could even generate them with a random model's clothing too. 

We started building. We implemented each component piece-by-piece: Deep Pose, ANet, PNet, and StyleGAN2 as GNet. Stitched them together, and with a bit of hard work, we reproduced the high-quality images in the paper. 

We were stoked... Until we tried inserting out own images; the results looked nothing like us.
 
I went back to the paper looking for answers. What had we done wrong? Surely, it must work on people outside of the dataset? (I was a naïve 21 year old)

While reveiwing this figure, I realized a fatal oversight, see if you notice it too.

![SPGAN_overfitted drawio](https://github.com/photoshootai/styleposgan-stylegan2/assets/41484082/a343e3ac-03ee-4773-81fb-e01d1a3ac1e9)
Real image on the left. The same model has been generated in the same pose, wearing different clothes by splicing the texture map. 

The authors had mentioned that one of the failure modes of their paper was that pants sometimes blend with skin like the black pants. 

But what they didn't realize was that in all these images, the background is the same. And that should have been impossible. 

Remember, the model only has access to the pose, and a texture map with this format (nowhere does it have access to the background of the image): 

![Screen Shot 2024-05-27 at 4 32 26 PM](https://github.com/photoshootai/styleposgan-stylegan2/assets/41484082/c5c2f35b-868d-445b-8c9b-0b3d8ece38f3)

This shows that the model has not in fact learned to sew a texture onto a pose, but in fact had memorized the dataset. 

We knew this meant we were halfway through our summer of allotted time, nobody in the world had actually solved the problem we wanted to solve, which makes this a much, much harder problem than we expected. 

We devised a new pipeline to try to get it to learn properly. 
1. we downloaded more similar datasets from Kaggle. The more identities, the better.
2. we used VGGFace to encode each image's face as a vector
3. we used K-means clustering on the face vectors to sort the images into folders arranged by the model's identity.
4. within each folder of a single identity, we created ordered [N*(N-1)] source-target image pairs where N is the nubmer of unique images in the folder.
5. By splicing a texture map with the face of the source with the clothes of the target image, we created the perfect "re-pose" task where the goal is to simply generate the target image.

We had just enough time to train this model a few times, and our results were as follows:
- the model could generate high quality images
- the model could approximate the colour and texture of the intended clothes
- the pose was almost always correct
- But, the face was not preserved. We saw a heavy bias from the dataset.

Here are some examples, where it generates a consistent pose and consistent clothing, but not correct identity. It had issues with longer hair on men, shadows in the input images (like the image of me in the centre column), and older people, like Bill on the right. 
![SPGAN_results drawio (1) copy](https://github.com/RickSugden/styleposegan-stylegan2/assets/41484082/5daa41fe-668c-48d0-8213-3cbad1f0fd77)

Unofortunately, that marked the end of our time and money to pursue this problem. And we no longer had a clear blueprint that we thought would suffice for our product. 

Here is a gallery of some of our results:

coming soon....
