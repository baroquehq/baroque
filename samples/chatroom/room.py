from baroque import Event
from .eventtypes import PeerJoinedEventType, PeerLeftEventType


class Room:
    def __init__(self, name, event_broker, events_topic):
        self.name = name
        self.peers = list()
        self.broker = event_broker
        self.topic = events_topic
        
    def join_peer(self, peer):
        if peer not in self.peers:
            self.peers.append(peer)
            
    def join_peers(self, peers_list):
        for p in peers_list:
            self.peers.append(p)
            self.broker.publish_on_topic(
                Event(PeerJoinedEventType,
                      payload=dict(peer=p.name),
                      owner=self.name),
                self.topic)
            
    def remove_peer(self, peer):
        if peer in self.peers:
            self.peers.remove(peer)
            self.broker.publish_on_topic(
                Event(PeerLeftEventType,
                      payload=dict(peer=peer.name),
                      owner=self.name),
                self.topic)
