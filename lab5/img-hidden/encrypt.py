import sys
from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    pixel_index = 0

    # Chuyển đổi tin nhắn thành chuỗi bit
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Đánh dấu kết thúc thông điệp (stop sequence)
    binary_message += '1111111111111110'

    data_index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3): # Duyệt qua R, G, B
                if data_index < len(binary_message):
                    # Thay đổi bit cuối cùng của kênh màu
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                else:
                    # Nếu đã hết dữ liệu, thoát khỏi vòng lặp kênh màu
                    break
            
            # Cập nhật pixel
            img.putpixel((col, row), tuple(pixel))

            if data_index >= len(binary_message):
                break # Nếu đã hết dữ liệu, thoát khỏi vòng lặp cột
        if data_index >= len(binary_message):
            break # Nếu đã hết dữ liệu, thoát khỏi vòng lặp hàng

    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == "__main__":
    main()