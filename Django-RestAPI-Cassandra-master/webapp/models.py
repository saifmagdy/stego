# Create your models here.

import cv2
import numpy as np 
import types
import base64
import wave
import bitarray

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
            for values in image:
                for pixel in values:
                    r, g, b = self.messageToBinary(pixel)
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
        image = cv2.imread(image_name)  
        if (len(data) == 0): 
            raise ValueError('Data is empty')
        encoded_image = self.hideData(image, data) # call the hideData function to hide the secret message into the selected image
        cv2.imwrite(filename, encoded_image)

    def decode_text(self,image_name):
        image = cv2.imread(image_name)
        text = self.showData(image)
        return text

    def decode_textLeast(self,image_name):
        image = cv2.imread(image_name)
        text = self.showDataLeast(image)
        return text

            

class Audio_LSB():
   
   def __init__(self):
      pass
   
   def isValid(self, string, framebytes):
      bits = bitarray.bitarray()
      bits.frombytes(string.encode('utf-8'))
      if len(bits) < len(frame_bytes):
         return True
      else:
         return False
   

   def encode(self, string):
      print("\nEncoding Starts..")
      ##string = "DR.HALA is goodd"
      ##print(string)
      string = string + '#####'
      ba= bitarray.bitarray()
      ba.frombytes(string.encode('utf-8'))
      bits = ba.tolist()
      ##print(len(string.encode('utf-8')))
      ##print(len(frame_bytes))
      for i, bit in enumerate(bits):
         frame_bytes[i] = (frame_bytes[i] & 254) | bit
      frame_modified = bytes(frame_bytes)
    
      newAudio =  wave.open('sampleStego.wav', 'wb')
      newAudio.setparams(audio.getparams())
      newAudio.writeframes(frame_modified)

      newAudio.close()
      audio.close()
      print(" |---->succesfully encoded inside sampleStego.wav")
      
   def twoEncode(self, string):
      print("\nEncoding Starts..")
      audio = wave.open("sample.wav",mode="rb")
      frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
      #string = "DR. Hala is good"
      #print(string)
      string = string + '#####'
    
      ba= bitarray.bitarray()
      ba.frombytes(string.encode('utf-8'))
      bits = ba.tolist()
    
    
      j=0
      for i in range(0,(len(bits)//2)):
         tmp = str(int(bits[j])) + str(int(bits[j+1]))
         frame_bytes[i] = (frame_bytes[i] & 252) | int(tmp,2)
         j+=2
      frame_modified = bytes(frame_bytes)
    
      newAudio =  wave.open('sampleStegoo.wav', 'wb')
      newAudio.setparams(audio.getparams())
      newAudio.writeframes(frame_modified)

      newAudio.close()
      audio.close()
      print(" |---->succesfully encoded inside sampleStego.wav")
      
      
   def decode(self):
      print("\nDecoding Starts..")
      audio = wave.open("sampleStego.wav", mode='rb')
      frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
      extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    
      string = bitarray.bitarray(extracted).tobytes().decode('utf-8','ignore')
    
      decoded = string.split("#####")[0]
      print("Sucessfully decoded: "+decoded)
      audio.close()	
   
   
   def twoDecode(self):
      print("\nDecoding Starts..")
      audio = wave.open("sampleStegoo.wav", mode='rb')
      frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
      extracted = ['{:02b}'.format(frame_bytes[i] & 3) for i in range(len(frame_bytes))]
      extracted = ''.join(extracted)
      string = bitarray.bitarray(extracted).tobytes().decode('utf-8','ignore')
    
      decoded = string.split("#####")[0]
      print("Sucessfully decoded: "+decoded)
      audio.close()


       
       