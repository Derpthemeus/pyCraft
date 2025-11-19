from minecraft.networking.packets import Packet
from minecraft.networking.types import (
    Integer, TrailingByteArray, Long
)


def get_packets(context):
    return {
        FinishConfigurationPacket,
        KeepAlivePacket,
        PingPacket,
        ClientBoundKnownPacksPacket,
    }


class FinishConfigurationPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x03

    packet_name = "finish configuration"
    definition = []


class KeepAlivePacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x04

    packet_name = "keep alive (configuration)"
    definition = [{'keep_alive_id': Long}]


class PingPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x05

    packet_name = "ping (configuration)"
    definition = [{'id': Integer}]


class ClientBoundKnownPacksPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x0E

    packet_name = "clientbound known packs"
    definition = [{'known_packs': TrailingByteArray}]
