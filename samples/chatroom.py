from baroque import Baroque
from chatroom.room import Room
from chatroom.peer import Peer
from chatroom.eventtypes import PeerJoinedEventType, PeerLeftEventType, \
    MessageEventType


brq = Baroque()
room_name = 'test_chatroom'
topic = brq.topics.new(room_name,
                       eventtypes=[MessageEventType(), PeerJoinedEventType(),
                                   PeerLeftEventType()],
                       description='chatroom events',
                       owner='me')

bob = Peer('Bob', brq, topic)
alice = Peer('Alice', brq, topic)
rudy = Peer('Rudy', brq, topic)
room = Room(room_name, brq, topic)
room.join_peers([bob, alice, rudy])
alice.send_message("Hi everybody!")
alice.send_message("How are you doing?")
rudy.send_message("Hello friend")
bob.send_message("sorry I am involved in too many chatrooms, quitting...")
room.remove_peer(bob)
