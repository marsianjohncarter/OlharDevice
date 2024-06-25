import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)

pn532 = PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()

print("Ожидание NFC карты...")

uid = pn532.read_passive_target(timeout=0.5)
while uid is None:
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
print("\nНайдена карта с UID:", [hex(i) for i in uid])

url = 'https://yoururl.com'
ndef_message = bytearray([0xD1, 0x01, len(url) + 1, 0x55, 0x01]) + url.encode('ascii')


block_number = 4  
ndef_message_padded = ndef_message + bytearray(16 - len(ndef_message)) 
if pn532.ntag2xx_write_block(block_number, ndef_message_padded):
    print("URL успешно записан на NFC метку!")
else:
    print("Не удалось записать URL на NFC метку.")
