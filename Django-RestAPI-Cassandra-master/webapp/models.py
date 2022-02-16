# Create your models here.

import cv2
import numpy as np
import bitstring 
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
####################################################################################################################
class DCT():
    def __init__(self):
        pass

    def encode_image(self, encoded_bits, dct_blocks):
        data_complete = False; encoded_bits.pos = 0
        encoded_data_len = bitstring.pack('uint:32', len(encoded_bits))
        converted_blocks = []
        for current_dct_block in dct_blocks:
            for i in range(1, len(current_dct_block)):
                curr_coeff = np.int32(current_dct_block[i])
                if (curr_coeff > 1):
                    curr_coeff = np.uint8(current_dct_block[i])
                    if (encoded_bits.pos == (len(encoded_bits) - 1)): data_complete = True; break
                    pack_coeff = bitstring.pack('uint:8', curr_coeff)
                    if (encoded_data_len.pos <= len(encoded_data_len) - 1): pack_coeff[-1] = encoded_data_len.read(1)
                    else: pack_coeff[-1] = encoded_bits.read(1)
                    # Replace converted coefficient
                    current_dct_block[i] = np.float32(pack_coeff.read('uint:8'))
            converted_blocks.append(current_dct_block)

        if not(data_complete): raise ValueError("Data didn't fully embed into cover image!")
        return converted_blocks
    
    def decode_image(self, dct_blocks):
        extracted_data = ""
        for current_dct_block in dct_blocks:
            for i in range(1, len(current_dct_block)):
                curr_coeff = np.int32(current_dct_block[i])
                if (curr_coeff > 1):
                    extracted_data += bitstring.pack('uint:1', np.uint8(current_dct_block[i]) & 0x01)
        return extracted_data
    

    def stitch_8x8_blocks_back_together(self, Nc, block_segments):
        image_rows = []
        temp = []
        for i in range(len(block_segments)):
            if i > 0 and not(i % int(Nc / 8)):
                image_rows.append(temp)
                temp = [block_segments[i]]
            else:
                temp.append(block_segments[i])
        image_rows.append(temp)

        return np.block(image_rows)

    def split_image_into_8x8_blocks(self, image):
        blocks = []
        for vert_slice in np.vsplit(image, int(image.shape[0] / 8)):
            for horiz_slice in np.hsplit(vert_slice, int(image.shape[1] / 8)):
                blocks.append(horiz_slice)
        return blocks

    def prepare_image(self, cover_image):
        height, width = cover_image.shape[:2]
        channels = [
                    split_image_into_8x8_blocks(cover_image[:,:,0]),
                    split_image_into_8x8_blocks(cover_image[:,:,1]),
                    split_image_into_8x8_blocks(cover_image[:,:,2]),
                    ]



class Audio_LSB():
   
   
   
   def __init__(self,audio_name):

        print(audio_name)
        self.audio_name = audio_name
        self.audio = wave.open(audio_name,mode="rb")
        self.frame_bytes = bytearray(list(self.audio.readframes(self.audio.getnframes())))

   
   def isValid(self, string, framebytes):
      bits = bitarray.bitarray()
      bits.frombytes(string.encode('utf-8'))
      if len(bits) < len(frame_bytes):
         return True
      else:
         return False
   

   def encode(self, string):
      string = string + '#####'
      ba= bitarray.bitarray()
      ba.frombytes(string.encode('utf-8'))
      bits = ba.tolist()

      for i, bit in enumerate(bits):
         self.frame_bytes[i] = (self.frame_bytes[i] & 254) | bit
      frame_modified = bytes(self.frame_bytes)
    
      newAudio =  wave.open('samplelsb.wav', 'wb')
      newAudio.setparams(self.audio.getparams())
      newAudio.writeframes(frame_modified)
    

      newAudio.close()
      self.audio.close()
      
      
   def twoEncode(self, string):
      string = string + '#####'
    
      ba= bitarray.bitarray()
      ba.frombytes(string.encode('utf-8'))
      bits = ba.tolist()
    
    
      j=0
      for i in range(0,(len(bits)//2)):
         tmp = str(int(bits[j])) + str(int(bits[j+1]))
         self.frame_bytes[i] = (self.frame_bytes[i] & 252) | int(tmp,2)
         j+=2
      frame_modified = bytes(self.frame_bytes)
    
      newAudio =  wave.open('twolsb.wav', 'wb')
      newAudio.setparams(self.audio.getparams())
      newAudio.writeframes(frame_modified)

      newAudio.close()
      self.audio.close()
      
      
   def decode(self):
      audio = wave.open(self.audio_name, mode='rb')
      self.frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
      extracted = [self.frame_bytes[i] & 1 for i in range(len(self.frame_bytes))]
    
      string = bitarray.bitarray(extracted).tobytes().decode('utf-8','ignore')
      self.audio.close()	
      decoded = string.split("#####")[0]
      return decoded
   
   
   def twoDecode(self):
      audio = wave.open("twolsb.wav", mode='rb')
      frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
      extracted = ['{:02b}'.format(frame_bytes[i] & 3) for i in range(len(frame_bytes))]
      extracted = ''.join(extracted)
      string = bitarray.bitarray(extracted).tobytes().decode('utf-8','ignore')
      audio.close()
      decoded = string.split("#####")[0]
      return decoded
      
      


       
       