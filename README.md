# Colour to DMC Thread

A CLI tool to translate image colours to closest DMC threads.

To find the colours, the image is quantized and then the nearest colour is looked up from a table of DMC colour threads.

The identified thread numbers will be returned added to the quantized image.

The user can specify the number of colours to reduce the image to before looking up the threads.

The user can also specify the percentage number to use filter out the threads as opposed to the default which returns all threads used more than 1% in the image.

It's assumed that the user won't be using more than 50 threads for the work. Therefore, if more than 50 threads are returned, only the top 50 most used threads will be found in the returned image.

<img src="https://github.com/kkumykova/colour_to_dmc/blob/master/examples/roses_dmc_palette.jpg" data-canonical-src="https://github.com/kkumykova/colour_to_dmc/blob/master/examples/roses_dmc_palette.jpgg" width="400" />

