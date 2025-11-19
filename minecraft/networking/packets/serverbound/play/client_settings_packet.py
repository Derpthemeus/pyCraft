import operator

from minecraft.networking.packets import Packet
from minecraft.networking.types import (
    String, Byte, VarInt, Boolean, UnsignedByte, Enum, BitFieldEnum,
    AbsoluteHand
)
from minecraft.utility import attribute_transform


class ClientSettingsPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x0D if context.protocol_later_eq(773) else \
               0x05 if context.protocol_later_eq(464) else \
               0x04 if context.protocol_later_eq(389) else \
               0x03 if context.protocol_later_eq(343) else \
               0x04 if context.protocol_later_eq(336) else \
               0x05 if context.protocol_later_eq(318) else \
               0x04 if context.protocol_later_eq(94) else \
               0x15

    packet_name = 'client settings'

    @staticmethod
    def get_definition(context):
        return [
            {'locale': String},
            {'view_distance': Byte},
            {'chat_mode': VarInt if context.protocol_later(47) else Byte},
            {'chat_colors': Boolean},
            {'displayed_skin_parts': UnsignedByte},
            {'main_hand': VarInt} if context.protocol_later(49) else {},

            {'enable_text_filtering': Boolean}
            if context.protocol_later_eq(757) else
            {'disable_text_filtering': Boolean}
            if (context.protocol_later_eq(755) and not context.protocol_later_eq(773)) else {},

            {'allow_server_listings': Boolean}
            if context.protocol_later_eq(755) else {},

            {'particle_status': VarInt}
            if context.protocol_later_eq(773) else {},
        ]


    field_enum = classmethod(
        lambda cls, field, context: {
            'chat_mode': cls.ChatMode,
            'displayed_skin_parts': cls.SkinParts,
            'main_hand': AbsoluteHand,
        }.get(field))

    class ChatMode(Enum):
        FULL = 0    # Receive all types of chat messages.
        SYSTEM = 1  # Receive only command results and game information.
        NONE = 2    # Receive only game information.

    class SkinParts(BitFieldEnum):
        CAPE = 0x01
        JACKET = 0x02
        LEFT_SLEEVE = 0x04
        RIGHT_SLEEVE = 0x08
        LEFT_PANTS_LEG = 0x10
        RIGHT_PANTS_LEG = 0x20
        HAT = 0x40

        ALL = 0x7F
        NONE = 0x00

    # This class alias is retained for backward compatibility.
    Hand = AbsoluteHand
