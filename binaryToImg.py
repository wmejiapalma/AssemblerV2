import binascii
class img_converter():
    def convert_to_hex(self, binary):
        hex_str = hex(int(binary, 2))
        self.hexstr = hex_str
    def flip_hex(self):
        #input is 0xe340600f
        #output is 0f6040e3
        #flip every 2 characters
        hex_str = self.hexstr
        hex_str = hex_str[2:]
        hex_str = hex_str[6:8] + hex_str[4:6] + hex_str[2:4] + hex_str[0:2]
        self.hexstr = hex_str
    def convert_to_bytes(self,binary):
        self.convert_to_hex(binary)
        self.flip_hex()
        #convert to bytes
        return bytes.fromhex(self.hexstr)