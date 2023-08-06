# Google Encoding Helper Package

This package is intended to be used to quickly translate the normal text into polyline encoded format.

This package must not be used for other purposes, and if it is, it may throw in exception and may also cause your program to crash.

To use this package, simply import gencoder after install it using the pip installer.
Then, call the encoding function through the path:
`gencoder.polycoder.super_encoder`

This function requires the coordinates to be provided as the input in `str` format.
The latitude and longitude must be separated with a comma.

Also, this package provides the facility to use the encoder on multiple coordinates.
This is facilitated by the use of lists, which means that you would need to separate the coordinates with the usage of lists.

Here is an example input:

`super_encoder(['38.5, -120.2', '40.7, -120.95', '43.252, -126.453'])`

The ideal output to this query shall be:

`_p~iF~ps|U_ulLnnqC_mqNvxq@`

Output Type: `str`

<hr>

**Important:** The author of this package does not allow anyone to copy the code without written permission.
If you need to use the code independently, you may contact the author of this package at rachitbhargava99@gmail.com.
