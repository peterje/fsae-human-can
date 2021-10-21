import cantools
from numpy import int8
from bitstream import BitStream

class CANFrame:
    # Terminology:
    # Dominant: 0-bit
    # Recessive: 1-bit
    def __init__(self, db, bs: BitStream):
        self.db = db
        # The single dominant start of frame (SOF) bit marks the start of a message.
        self.sof = bs.read(1)
        print(self.sof)
        # The Standard CAN 11-bit identifier establishes the priority of the message.
        self.identifier = bs.read(11)
        print(self.identifier)
        # The single remote transmission request (RTR) bit is dominant when information is required from another node.
        # This is usually recessive
        self.rtr = bs.read(1)
        print(self.rtr)
        # A dominant single identifier extension (IDE) bit means that a standard CAN identifier with no extension
        # is being transmitted. Recessive if using standard 11-bit ID
        self.ide = bs.read(1)
        # Reserved bit, perhaps will be used in future standards.
        self.r0 = bs.read(1)
        # The 4-bit data length code (DLC) contains the number of bytes of data being transmitted.
        self.dlc = bs.read(4)
        # Up to 64 bits of application data may be transmitted
        self.data = bs.read(64)
        # The 16-bit (15 bits plus delimiter) cyclic redundancy check (CRC) contains the checksum
        # (number of bits transmitted) of the application data for error detection
        self.crc = bs.read(16)
        # Every node receiving an accurate message overwrites this recessive bit in the original message
        # with a dominate bit, indicating an error-free message has been sent.
        self.ack = bs.read(2)
        # This end-of-frame (EOF), 7-bit field marks the end of a CAN frame
        self.eof = bs.read(7)

    def __repr__(self):
        return str(self.db.decode_message(self.get_message_id(), self.data))

    def get_message_id(self):
        print(type(self.identifier))
        print(self.identifier)
        print(str(self.identifier))
        return int(str(self.identifier), 2)


def main():
    db = cantools.db.load_file("fsae.dbc")
    raw_bytes = b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00'
    bus = BitStream(raw_bytes)
    print(bus.read(1))
    frame = CANFrame(db, bus)
    print(frame)


if __name__ == '__main__':
    main()
