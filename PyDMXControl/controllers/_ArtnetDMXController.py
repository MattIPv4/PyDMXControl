"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""
import socket
from typing import List

from ._TransmittingController import TransmittingController


class ArtnetDMXController(TransmittingController):

    UDP_PORT = 6454

    def __init__(self, *args, **kwargs):
        # Device information
        self.__target_ip = kwargs.pop("target_ip", "127.0.0.1")
        self.__universe = kwargs.pop("universe", 0)
        self.__subnet = 0
        self.__net = 0
        self.__sequence = 0
        self.__make_even = kwargs.pop("even_packet_size", True)
        self.__packet_size = put_in_range(kwargs.pop("packet_size", 512), 2, 512, self.__make_even)
        self.__packet_header = bytearray()
        self.__buffer = bytearray(self.__packet_size)
        self.__broadcast=kwargs.pop("broadcast", False)

        

        self.__is_simplified = True		# simplify use of universe, net and subnet

        # UDP SOCKET
        self.__socket_client = None

        # Create the parent controller
        super().__init__(*args, **kwargs)

    def make_header(self):
        """Make packet header."""
        # 0 - id (7 x bytes + Null)
        self.__packet_header = bytearray()
        self.__packet_header.extend(bytearray('Art-Net', 'utf8'))
        self.__packet_header.append(0x0)
        # 8 - opcode (2 x 8 low byte first)
        self.__packet_header.append(0x00)
        self.__packet_header.append(0x50)  # ArtDmx data packet
        # 10 - prototocol version (2 x 8 high byte first)
        self.__packet_header.append(0x0)
        self.__packet_header.append(14)
        # 12 - sequence (int 8), NULL for not implemented
        self.__packet_header.append(self.__sequence)
        # 13 - physical port (int 8)
        self.__packet_header.append(0x00)
        # 14 - universe, (2 x 8 low byte first)
        if self.__is_simplified:
            # not quite correct but good enough for most cases:
            # the whole net subnet is simplified
            # by transforming a single uint16 into its 8 bit parts
            # you will most likely not see any differences in small networks
            msb, lsb = shift_this(self.__universe)   # convert to MSB / LSB
            self.__packet_header.append(lsb)
            self.__packet_header.append(msb)
        # 14 - universe, subnet (2 x 4 bits each)
        # 15 - net (7 bit value)
        else:
            # as specified in Artnet 4 (remember to set the value manually after):
            # Bit 3  - 0 = Universe (1-16)
            # Bit 7  - 4 = Subnet (1-16)
            # Bit 14 - 8 = Net (1-128)
            # Bit 15     = 0
            # this means 16 * 16 * 128 = 32768 universes per port
            # a subnet is a group of 16 Universes
            # 16 subnets will make a net, there are 128 of them
            self.__packet_header.append(self.__subnet << 4 | self.__universe)
            self.__packet_header.append(self.__net & 0xFF)
        # 16 - packet size (2 x 8 high byte first)
        msb, lsb = shift_this(self.__packet_size)		# convert to MSB / LSB
        self.__packet_header.append(msb)
        self.__packet_header.append(lsb)    

    def _connect(self):
         # Try to close if exists
        if self.__socket_client is not None:
            try:
                self._close()
            except Exception:
                pass

        # Get new device
        self.__socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.__broadcast:
            self.__socket_client.setsockopt(
                socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.make_header()

    def _close(self):         
        self.__socket_client.close()
        print("CLOSE: ArtnetDMX closed")

    def _transmit(self, frame: List[int], first: int):
        # Convert to a bytearray and pad the start of the frame
        # We're transmitting direct DMX data here, so a frame must start at channel 1, but can end early
        
        self.__buffer=bytearray(([0] * (first - 1)) + frame)
        # Write
        packet = bytearray()
        packet.extend(self.__packet_header)
        packet.extend(self.__buffer)
        try:
            self.__socket_client.sendto(packet, (self.__target_ip, self.UDP_PORT))
        except socket.error as error:
            print(f"ERROR: Socket error with exception: {error}")

    """Provides common functions byte objects."""

    def set_universe(self, universe):
        """Setter for universe (0 - 15 / 256).

        Mind if protocol has been simplified
        """
        # This is ugly, trying to keep interface easy
        # With simplified mode the universe will be split into two
        # values, (uni and sub) which is correct anyway. Net will always be 0
        if self.is_simplified:
            self.universe = put_in_range(universe, 0, 255, False)
        else:
            self.universe = put_in_range(universe, 0, 15, False)
        self.make_header()

    def set_subnet(self, sub):
        """Setter for subnet address (0 - 15).

        Set simplify to false to use
        """
        self.subnet = put_in_range(sub, 0, 15, False)
        self.make_header()

    def set_net(self, net):
        """Setter for net address (0 - 127).

        Set simplify to false to use
        """
        self.net = put_in_range(net, 0, 127, False)
        self.make_header()

    def set_packet_size(self, packet_size):
        """Setter for packet size (2 - 512, even only)."""
        self.packet_size = put_in_range(packet_size, 2, 512, self.make_even)
        self.make_header()
            
    
    
"""Provides common functions byte objects."""


def shift_this(number, high_first=True):
    """Utility method: extracts MSB and LSB from number.

    Args:
    number - number to shift
    high_first - MSB or LSB first (true / false)

    Returns:
    (high, low) - tuple with shifted values

    """
    low = (number & 0xFF)
    high = ((number >> 8) & 0xFF)
    if high_first:
        return((high, low))
    return((low, high))


def clamp(number, min_val, max_val):
    """Utility method: sets number in defined range.

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number

    Returns:
    number - number in correct range
    """
    return max(min_val, min(number, max_val))


def set_even(number):
    """Utility method: ensures number is even by adding.

    Args:
    number - number to make even

    Returns:
    number - even number
    """
    if number % 2 != 0:
        number += 1
    return number


def put_in_range(number, range_min, range_max, make_even=True):
    """Utility method: sets number in defined range.
    DEPRECATED: this will be removed from the library

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number
    make_even - should number be made even

    Returns:
    number - number in correct range

    """
    number = clamp(number, range_min, range_max)
    if make_even:
        number = set_even(number)
    return number


def make_address_mask(universe, sub=0, net=0, is_simplified=True):
    """Returns the address bytes for a given universe, subnet and net.

    Args:
    universe - Universe to listen
    sub - Subnet to listen
    net - Net to listen
    is_simplified - Whether to use nets and subnet or universe only,
    see User Guide page 5 (Universe Addressing)

    Returns:
    bytes - byte mask for given address

    """
    address_mask = bytearray()

    if is_simplified:
        # Ensure data is in right range
        universe = clamp(universe, 0, 32767)

        # Make mask
        msb, lsb = shift_this(universe)  # convert to MSB / LSB
        address_mask.append(lsb)
        address_mask.append(msb)
    else:
        # Ensure data is in right range
        universe = clamp(universe, 0, 15)
        sub = clamp(sub, 0, 15)
        net = clamp(net, 0, 127)

        # Make mask
        address_mask.append(sub << 4 | universe)
        address_mask.append(net & 0xFF)

    return address_mask
