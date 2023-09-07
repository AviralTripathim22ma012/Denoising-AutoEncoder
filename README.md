## What would happen if we use a skip connection at 
the bottle-neck of a denoising auto encoder?
With a deep autoencoder, skipping connections has a number of 
### possible advantages:
Increased reconstruction quality: By preserving information from 
the input space to the output space, skip connections can aid in 
improving the output quality of reconstruction.
Better gradient flow: The vanishing gradient problem can affect 
deep autoencoders, making it challenging to train deep neural 
networks. Use of skip connections, which allows the gradient to 
go through the network more readily, can lessen this problem.
Faster training: By enabling the network to absorb input data 
more quickly, skip connections can also hasten the training 
process.
## What would happen if we use LSTM for image 
classification?
Pictures contain a grid-like structure, where each pixel has a spatial 
relationship with its neighbouring pixels. This spatial information is not 
captured by the sequential structure of LSTMs, which process one input 
at a time in a predetermined order.
LSTMs demand a significant amount of memory and computational 
resources, which can make training on large image datasets exceedingly 
slow and resource-intensive.
write a code for a denoising auto-encoder from 
scratch using basic liberaries such as numpy, and 
open cv, use this model to denoise a noisy image 
