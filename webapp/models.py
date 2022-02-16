# Create your models here.

import cv2
import numpy as np 
import types

class Image_LSB():

    def __init__(self):
        pass

    def messageToBinary(self, message):
        if type(message) == str:
            return ''.join([ format(ord(i), "08b") for i in message ])
        elif type(message) == bytes or type(message) == np.ndarray:
            return [ format(i, "08b") for i in message ]
        elif type(message) == int or type(message) == np.uint8:
            return format(message, "08b")
        else:
            raise TypeError("Input type not supported")

    def hideData(self, image, secret_message):
    #Check if the number of bytes to encode is less than the maximum bytes in the image
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        n_bytes_double = image.shape[0] * image.shape[1] * 3 * 2 // 8
        secret_message += "#####" # you can use any string as the delimeter
        data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
        binary_secret_msg = self.messageToBinary(secret_message)
        data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
        if data_len < n_bytes:
            print("will use lsb technique as Maximum bytes to encode:" , n_bytes,data_len)
            for values in image:
                for pixel in values:
                    # convert RGB values to binary format
                    r, g, b = self.messageToBinary(pixel)
                    # modify the least significant bit only if there is still data to store
                    if data_index < data_len:
                        # hide the data into least significant bit of red pixel
                        pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                        data_index += 1
                    if data_index < data_len:
                # hide the data into least significant bit of green pixel
                        pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                        data_index += 1
                    if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                        pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                        data_index += 1
            # if data is encoded, just break out of the loop
                    if data_index >= data_len:
                        break
        
        
        elif n_bytes_double > data_len > n_bytes:
            print("will use two lsb technique as Maximum bytes to encode:", n_bytes_double,data_len)
        for values in image:
            for pixel in values:
            # convert RGB values to binary format
                r, g, b = self.messageToBinary(pixel)
            # modify the least significant bit only if there is still data to store
                if data_index < data_len:
                # hide the data into least significant bit of red pixel
                    pixel[0] = int(r[:-2] + binary_secret_msg[data_index]+ binary_secret_msg[data_index + 1], 2)
                    data_index += 2
                if data_index < data_len:
                # hide the data into least significant bit of green pixel
                    pixel[1] = int(g[:-2] + binary_secret_msg[data_index]+ binary_secret_msg[data_index + 1], 2)
                    data_index += 2
                if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                    pixel[2] = int(b[:-2] + binary_secret_msg[data_index]+ binary_secret_msg[data_index + 1], 2)
                    data_index += 2
            # if data is encoded, just break out of the loop
                if data_index >= data_len:
                    break

        return image

    def showData(self, image):
        binary_data = ""
        for values in image:
            for pixel in values:
                r, g, b = self.messageToBinary(pixel) #convert the red,green and blue values into binary format
                binary_data += r[-2] #extracting data from the least significant bit of red pixel  
                binary_data += r[-1] #extracting data from the least significant bit of red pixel
                binary_data += g[-2] #extracting data from the least significant bit of red pixel
                binary_data += g[-1] #extracting data from the least significant bit of red pixel
                binary_data += b[-2] #extracting data from the least significant bit of red pixel
                binary_data += b[-1] #extracting data from the least significant bit of red pixel
    # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        #convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
                break
    #print(decoded_data)
        return decoded_data[:-5]

    def showDataLeast(self, image):
        binary_data = ""
        for values in image:
            for pixel in values:
                r, g, b = self.messageToBinary(pixel) #convert the red,green and blue values into binary format
                binary_data += r[-1] #extracting data from the least significant bit of red pixel
                binary_data += g[-1] #extracting data from the least significant bit of red pixel
                binary_data += b[-1] #extracting data from the least significant bit of red pixel
                # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
                break
    #print(decoded_data)
        return decoded_data[:-5]

    def encode_text(self,image_name,data,filename):  
        image = cv2.imread(image_name) # Read the input image using OpenCV-Python.
    #It is a library of Python bindings designed to solve computer vision problems. 
    
    #details of the image
        print("The shape of the image is: ",image.shape) #check the shape of image to calculate the number of bytes in it
        print("The original image is as shown below: ")
        resized_image = cv2.resize(image, (500, 500)) #resize the image as per your requirement
        #cv2.imshow("images.jpg" ,resized_image)#display the image
        #cv2.waitKey()
    
         
        if (len(data) == 0): 
            raise ValueError('Data is empty')
    
        encoded_image = self.hideData(image, data) # call the hideData function to hide the secret message into the selected image
        cv2.imwrite(filename, encoded_image)

    def decode_text(self):
        image_name = input("Enter the name of the steganographed image that you want to decode (with extension) :")
    # read the image that contains the hidden image
    
        image = cv2.imread(image_name)#read the image using cv2.imread
        resized_image = cv2.resize(image, (500, 500))
        #cv2.imshow("steg.jpg" ,resized_image)#display the image
        #cv2.waitKey()

        print("The Steganographed image is as shown below: ")
    #resize the original image as per your requirement


        text = self.showData(image)
        return text

    def decode_textLeast(self):
        image_name = input("Enter the name of the steganographed image that you want to decode (with extension) :")
    # read the image that contains the hidden image
    
        image = cv2.imread(image_name)#read the image using cv2.imread
        #resized_image = cv2.resize(image, (500, 500))
        #cv2.imshow("steg.jpg" ,resized_image)#display the image
        #cv2.waitKey()

        print("The Steganographed image is as shown below: ")
    #resize the original image as per your requirement


        text = self.showDataLeast(image)
        return text

    def Steganography(self):
        a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data with least 2 significant bits \n 3. decode with least significant bit \n bit Your input is: ")
        userinput = int(a)
        if (userinput == 1):
            print("\nEncoding....")
            self.encode_text()     
        elif (userinput == 2):
            print("\nDecoding....") 
            print("Decoded message is " + self.decode_text()) 
        elif (userinput == 3):
            print("\nDecoding....") 
            print("Decoded message is " + self.decode_textLeast()) 
            

   

       