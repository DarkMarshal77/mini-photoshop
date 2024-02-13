import Core
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    image_path = "input/image1.bmp"
    loaded_image = Core.open_image(image_path)
    grayscale_image = Core.convert_to_grayscale(loaded_image)
    dithered_image = Core.ordered_dither(grayscale_image)
    leveled_image = Core.auto_level(grayscale_image)
    compressed_data = Core.huffman_encode(loaded_image)

    resized_image = Core.resize_image(loaded_image, 300, 200)
    cropped_image = Core.crop_image(loaded_image, 50, 50, 250, 150)

    brighter_image = Core.adjust_brightness(loaded_image, 1.2)
    higher_contrast_image = Core.adjust_contrast(loaded_image, 1.5)
    balanced_image = Core.adjust_color_balance(loaded_image, 1.2, 0.8, 1.0)
    equalized_image = Core.histogram_equalization(grayscale_image)




