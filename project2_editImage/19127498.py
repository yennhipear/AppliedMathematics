from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def truncate(val):
    if val < 0:     return 0
    if val > 255:   return 255
    return val

def changeBrightness(image):
    pixels = np.array(image)
    new_pixels = pixels
    brightness  = 40
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            red, green, blue = pixels[i][j][0], pixels[i][j][1], pixels[i][j][2]
            new_pixels[i][j][0] = truncate(red + brightness)
            new_pixels[i][j][1] = truncate(green + brightness)
            new_pixels[i][j][2] = truncate(blue + brightness)
    new_img = Image.fromarray(new_pixels)
    return new_img

def changeConstract(image):
    pixels = np.array(image)
    new_pixels = pixels
    alpha  = 2
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            red, green, blue = pixels[i][j][0], pixels[i][j][1], pixels[i][j][2]
            new_pixels[i][j][0]    = truncate(red * alpha)
            new_pixels[i][j][1]    = truncate(green * alpha)
            new_pixels[i][j][2]    = truncate(blue * alpha)
    new_img = Image.fromarray(new_pixels)
    return new_img

def convert_ColorImg_into_GrayscaleImg(image):
    pixels = np.array(image)
    new_pixels = pixels

    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            red, green, blue = pixels[i][j][0], pixels[i][j][1], pixels[i][j][2]

            grayscale = int(round(0.3 * red + 0.59 * green + 0.11 * blue))
            new_pixels[i][j][0] = truncate(grayscale)
            new_pixels[i][j][1] = truncate(grayscale)
            new_pixels[i][j][2] = truncate(grayscale)

    new_img = Image.fromarray(new_pixels)
    return new_img

def flipImage(image):
    pixels = np.array(image)
    new_pixels = np.fliplr(pixels)

    new_img = Image.fromarray(new_pixels)
    return new_img

def overlay2Image(image1, image2):
    img1_gray = convert_ColorImg_into_GrayscaleImg(image1)
    img2_gray = convert_ColorImg_into_GrayscaleImg(image2)

    pixels1 = np.array(img1_gray)
    pixels2 = np.array(img2_gray)
    new_pixels = pixels1 + pixels2

    for i in range(len(new_pixels)):
        for j in range(len(new_pixels[i])):
            new_pixels[i][j][0] = truncate(new_pixels[i][j][0])
            new_pixels[i][j][1] = truncate(new_pixels[i][j][1])
            new_pixels[i][j][2] = truncate(new_pixels[i][j][2])

    new_img = Image.fromarray(new_pixels)
    return new_img

def averageColor(pixels, i, j, blurFactor):
    r_sum = g_sum = b_sum = 0
    for k in range(i - blurFactor, i + blurFactor + 1):
        for l in range(j - blurFactor, j + blurFactor + 1):
            red, green, blue = pixels[k][l][0], pixels[k][l][1], pixels[k][l][2]
            r_sum += red
            g_sum += green
            b_sum += blue
    r_avg = r_sum // ((blurFactor * 2 + 1) ** 2)
    g_avg = g_sum // ((blurFactor * 2 + 1) ** 2)
    b_avg = b_sum // ((blurFactor * 2 + 1) ** 2)
    return r_avg, g_avg, b_avg

def blurImage (image):
    pixels = np.array(image)
    new_pixels = pixels
    
    blurFactor = 3
    for i in range(blurFactor, len(pixels) - blurFactor):
        for j in range(blurFactor, len(pixels[i]) - blurFactor):
            new_pixels[i][j][0], new_pixels[i][j][1], new_pixels[i][j][2] = averageColor(pixels, i, j, blurFactor)

    new_img = Image.fromarray(new_pixels)
    return new_img

if __name__ == "__main__":
    rose_img      = Image.open("rose.jpeg")
    coverflag_img = Image.open("coverflag.jpeg")
    flag_img      = Image.open("flag.jpeg")

    img_bri  = changeBrightness(rose_img)
    img_bri.save("brightnessImg.jpeg")

    img_cons = changeConstract(rose_img)
    img_cons.save("constractImg.jpeg")

    img_gray = convert_ColorImg_into_GrayscaleImg(rose_img)
    img_gray.save("grayscaleImg.jpeg")

    img_flip = flipImage(rose_img)
    img_flip.save("flipImg.jpeg")

    img_ovrlay = overlay2Image(coverflag_img, flag_img)
    img_ovrlay.save("overlayImg.jpeg")

    img_blur = blurImage(rose_img)
    img_blur.save("blurImg.jpeg")
    
    plt.imshow(img_bri)
    plt.show()
    plt.imshow(img_cons)
    plt.show()
    plt.imshow(img_gray)
    plt.show()
    plt.imshow(img_flip)
    plt.show()
    plt.imshow(img_ovrlay)
    plt.show()
    plt.imshow(img_blur)
    plt.show()
