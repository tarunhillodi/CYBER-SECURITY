from PIL import Image
import getpass

def encode(image_path, secret_message, output_path, password):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    index = 0

    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))

            # first value is length of message
            if row == 0 and col == 0 and index < len(secret_message):
                asc = len(secret_message)
            elif index < len(secret_message):
                c = secret_message[index]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g, b))
            index += 1

    encoded.save(output_path, "PNG")

def decode(image_path, password):
    img = Image.open(image_path)
    width, height = img.size
    msg = ""
    index = 0

    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                if img.mode == 'RGBA':
                    r, g, b, a = img.getpixel((col, row))
                else:
                    raise  # Re-raise the exception if it's not due to a missing alpha channel

            if row == 0 and col == 0:
                length = r
            elif index < length:
                msg += chr(r)
                index += 1

        if index >= length:
            break  # Break the outer loop when the entire message is decoded

    return msg


def main():
    task = input("Would you like to encode or decode? ")
    
    if task == "encode":
        image_path = input("Enter the image path: ")
        secret_message = input("Enter your message: ")
        output_path = input("Enter the output image path: ")
        password = getpass.getpass("Enter a password: ")
        encode(image_path, secret_message, output_path, password)
    elif task == "decode":
        image_path = input("Enter the image path: ")
        password = getpass.getpass("Enter the password: ")
        print("Decoded Message Is:")
        print("Secret Message")
    else:
        raise Exception("Invalid task. Please choose 'encode' or 'decode'.")

if __name__ == "__main__":
    main()
