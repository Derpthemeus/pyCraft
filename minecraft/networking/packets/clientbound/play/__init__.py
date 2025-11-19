from minecraft import PRE
from minecraft.networking.packets import (
    Packet, AbstractKeepAlivePacket, AbstractPluginMessagePacket
)

from minecraft.networking.types import (
    FixedPoint, Integer, Angle, UnsignedByte, Byte, Boolean, UUID, Short,
    VarInt, Double, Float, String, Enum, Difficulty, Long, Vector, Direction,
    PositionAndLook, multi_attribute_alias, attribute_transform,
)



# Formerly known as state_playing_clientbound.
def get_packets(context):
    packets = {
        KeepAlivePacket,
        ChatMessagePacket,
        DisconnectPacket,
        SpawnPlayerPacket,
        PluginMessagePacket,
    }

    if context.protocol_earlier_eq(47):
        packets |= {
            SetCompressionPacket,
        }

    return packets


class KeepAlivePacket(AbstractKeepAlivePacket):
    @staticmethod
    def get_id(context):
        return 0x2B if context.protocol_later_eq(773) else \
               0x1F if context.protocol_later_eq(741) else \
               0x20 if context.protocol_later_eq(721) else \
               0x21 if context.protocol_later_eq(550) else \
               0x20 if context.protocol_later_eq(471) else \
               0x21 if context.protocol_later_eq(389) else \
               0x20 if context.protocol_later_eq(345) else \
               0x1F if context.protocol_later_eq(332) else \
               0x20 if context.protocol_later_eq(318) else \
               0x1F if context.protocol_later_eq(107) else \
               0x00


class ChatMessagePacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x0F if context.protocol_later_eq(755) else \
               0x0E if context.protocol_later_eq(721) else \
               0x0F if context.protocol_later_eq(550) else \
               0x0E if context.protocol_later_eq(343) else \
               0x0F if context.protocol_later_eq(332) else \
               0x10 if context.protocol_later_eq(317) else \
               0x0F if context.protocol_later_eq(107) else \
               0x02

    packet_name = "chat message"
    get_definition = staticmethod(lambda context: [
        {'json_data': String},
        {'position': Byte},
        {'sender': UUID} if context.protocol_later_eq(718) else {},
    ])

    class Position(Enum):
        CHAT = 0       # A player-initiated chat message.
        SYSTEM = 1     # The result of running a command.
        GAME_INFO = 2  # Displayed above the hotbar in vanilla clients.


class DisconnectPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x1A if context.protocol_later_eq(755) else \
               0x19 if context.protocol_later_eq(741) else \
               0x1A if context.protocol_later_eq(721) else \
               0x1B if context.protocol_later_eq(550) else \
               0x1A if context.protocol_later_eq(471) else \
               0x1B if context.protocol_later_eq(345) else \
               0x1A if context.protocol_later_eq(332) else \
               0x1B if context.protocol_later_eq(318) else \
               0x1A if context.protocol_later_eq(107) else \
               0x40

    packet_name = "disconnect"

    definition = [
        {'json_data': String}]


class SetCompressionPacket(Packet):
    # Note: removed between protocol versions 47 and 107.
    @staticmethod
    def get_id(context):
        return 0x03 if context.protocol_later_eq(755) else \
               0x46

    packet_name = "set compression"
    definition = [
        {'threshold': VarInt}]


class SpawnPlayerPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x04 if context.protocol_later_eq(721) else \
               0x05 if context.protocol_later_eq(67) else \
               0x0C

    packet_name = 'spawn player'
    get_definition = staticmethod(lambda context: [
        {'entity_id': VarInt},
        {'player_UUID': UUID},
        {'x': Double} if context.protocol_later_eq(100)
        else {'x': FixedPoint(Integer)},
        {'y': Double} if context.protocol_later_eq(100)
        else {'y': FixedPoint(Integer)},
        {'z': Double} if context.protocol_later_eq(100)
        else {'z': FixedPoint(Integer)},
        {'yaw': Angle},
        {'pitch': Angle},
        {'current_item': Short} if context.protocol_earlier_eq(49) else {},
        # TODO: read entity metadata (protocol < 550)
    ])

    # Access the 'x', 'y', 'z' fields as a Vector tuple.
    position = multi_attribute_alias(Vector, 'x', 'y', 'z')

    # Access the 'yaw', 'pitch' fields as a Direction tuple.
    look = multi_attribute_alias(Direction, 'yaw', 'pitch')

    # Access the 'x', 'y', 'z', 'yaw', 'pitch' fields as a PositionAndLook.
    # NOTE: modifying the object retrieved from this property will not change
    # the packet; it can only be changed by attribute or property assignment.
    position_and_look = multi_attribute_alias(
        PositionAndLook, 'x', 'y', 'z', 'yaw', 'pitch')

class PluginMessagePacket(AbstractPluginMessagePacket):
    @staticmethod
    def get_id(context):
        return 0x18 if context.protocol_later_eq(755) else \
               0x17 if context.protocol_later_eq(741) else \
               0x18 if context.protocol_later_eq(721) else \
               0x19 if context.protocol_later_eq(550) else \
               0x18 if context.protocol_later_eq(471) else \
               0x19 if context.protocol_later_eq(345) else \
               0x18 if context.protocol_later_eq(332) else \
               0x19 if context.protocol_later_eq(318) else \
               0x18 if context.protocol_later_eq(70) else \
               0x3F


