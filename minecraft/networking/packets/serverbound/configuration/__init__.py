from minecraft.networking.packets import Packet
from minecraft.networking.types import (
    VarInt, Integer, Boolean, String, TrailingByteArray, Byte, UnsignedByte, Long
)


def get_packets(context):
    return {
        ClientInformationPacket,
        ServerBoundPluginMessagePacket,
        AcknowledgeFinishConfigurationPacket,
        KeepAlivePacket,
        PongPacket,
        ServerBoundKnownPacksPacket,
    }


class ClientInformationPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x00

    def __init__(self, context=None, **field_values):
        super(ClientInformationPacket, self).__init__(context)
        self.locale = field_values.get('locale', "en_US")
        self.view_distance = field_values.get('view_distance', 2)
        self.chat_mode = field_values.get('chat_mode', 0)
        self.chat_colors = field_values.get('chat_colors', True)
        self.displayed_skin_parts = field_values.get('displayed_skin_parts', 0)
        self.main_hand = field_values.get('main_hand', 1)
        self.enable_text_filtering = field_values.get('enable_text_filtering', False)
        self.allow_server_listings = field_values.get('allow_server_listings', True)
        self.particle_status = field_values.get('particle_status', 2)

    packet_name = "client information"
    definition = [
        {'locale': String},
        {'view_distance': Byte},
        {'chat_mode': VarInt},
        {'chat_colors': Boolean},
        {'displayed_skin_parts': UnsignedByte},
        {'main_hand': VarInt},
        {'enable_text_filtering': Boolean},
        {'allow_server_listings': Boolean},
        {'particle_status': VarInt}
    ]


class ServerBoundPluginMessagePacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x02

    packet_name = "serverbound plugin message (configuration)"
    definition = [
        {'channel': String},
        {'data': TrailingByteArray}
    ]


class AcknowledgeFinishConfigurationPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x03

    packet_name = "acknowledge finish configuration"
    definition = []


class KeepAlivePacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x04

    packet_name = "keep alive (configuration)"
    definition = [{'keep_alive_id': Long}]


class PongPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x05

    packet_name = "pong (configuration)"
    definition = [{'id': Integer}]


class ServerBoundKnownPacksPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x07

    packet_name = "serverbound known packs"

    def __init__(self, context=None, **field_values):
        super(ServerBoundKnownPacksPacket, self).__init__(context)
        self.known_packs = field_values.get('known_packs', [])

    def write_fields(self, packet_buffer):
        VarInt.send(len(self.known_packs), packet_buffer)
        for pack in self.known_packs:
            String.send(pack['namespace'], packet_buffer)
            String.send(pack['id'], packet_buffer)
            String.send(pack['version'], packet_buffer)
