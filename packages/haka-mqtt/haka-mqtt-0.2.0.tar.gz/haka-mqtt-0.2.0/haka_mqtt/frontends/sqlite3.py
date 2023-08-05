class SqliteMqttClient(object):
    def __init__(self, reactor):
        """

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        """
        self.__queue = []
        self.__reactor = reactor
        self.__reactor.on_connect_fail = self.__on_connect_fail
        self.__reactor.on_disconnect = self.__on_disconnect
        self.__reactor.on_connack = self.__on_connack
        self.__reactor.on_pubrec = self.__on_pubrec
        self.__reactor.on_pubcomp = self.__on_pubcomp
        self.__reactor.on_suback = self.__on_suback
        self.__reactor.on_unsuback = self.__on_unsuback
        self.__reactor.on_publish = self.__on_publish
        self.__reactor.on_puback = self.__on_puback
        self.__reactor.on_pubrel = self.__on_pubrel

    # Connection Callbacks
    def __on_connect_fail(self, reactor):
        """

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        """
        self.on_connect_fail(self)

    def __on_disconnect(self, reactor):
        """

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        """
        self.on_disconnect(self)

    def __on_connack(self, reactor, connack):
        """Called immediately upon receiving a `MqttConnack` packet from
        the remote.  The `reactor.state` will be `ReactorState.started`
        or `ReactorState.stopping` if the reactor is shutting down.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        connack: MqttConnack
        """
        self.on_connack(self, connack)

    # Send path
    def __on_pubrec(self, reactor, pubrec):
        """Called immediately upon receiving a `MqttPubrec` packet from
        the remote.  This is part of the QoS=2 message send path.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        pubrec: MqttPubrec
        """
        self.on_pubrec(self, pubrec)
        # save to database

    def __on_pubcomp(self, reactor, pubcomp):
        """Called immediately upon receiving a `MqttPubcomp` packet
        from the remote.  This is part of the QoS=2 message send path.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        pubcomp: MqttPubcomp
        """
        self.on_pubcomp(self, pubcomp)
        # delete from database.

    def __on_puback(self, reactor, puback):
        """Called immediately upon receiving a `MqttPuback` packet from
        the remote.  This method is part of the QoS=1 message send path.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        puback: MqttPuback
        """
        self.on_puback(self, puback)
        # delete from database.

    # Subscribe path
    def __on_suback(self, reactor, suback):
        """Called immediately upon receiving a `MqttSuback` packet from
        the remote.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        suback: MqttSuback
        """
        pass

    def __on_unsuback(self, reactor, unsuback):
        """Called immediately upon receiving a `MqttUnsuback` packet
        from the remote.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        unsuback: MqttUnsuback
        """
        pass

    # Receive path
    def __on_publish(self, reactor, publish):
        """Called immediately upon receiving a `MqttSuback` packet from
        the remote.  This is part of the QoS=0, 1, and 2 message receive
        paths.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        publish: MqttPublish
        """
        self.on_publish(self, publish)
        # save to database.

    def __on_pubrel(self, reactor, pubrel):
        """Called immediately upon receiving a `MqttPubrel` packet from
        the remote.  This is part of the QoS=2 message receive path.

        Parameters
        ----------
        reactor: haka_mqtt.reactor.Reactor
        pubrel: MqttPubrel
        """
        self.on_pubrel(self, pubrel)
        # save to database.

    # Connection Callbacks
    def on_connect_fail(self, reactor):
        """

        Parameters
        ----------
        reactor: Reactor
        """
        pass

    def on_disconnect(self, reactor):
        """

        Parameters
        ----------
        reactor: Reactor
        """
        pass

    def on_connack(self, reactor, connack):
        """Called immediately upon receiving a `MqttConnack` packet from
        the remote.  The `reactor.state` will be `ReactorState.started`
        or `ReactorState.stopping` if the reactor is shutting down.

        Parameters
        ----------
        reactor: Reactor
        connack: MqttConnack
        """
        pass

    # Send path
    def on_pubrec(self, reactor, pubrec):
        """Called immediately upon receiving a `MqttPubrec` packet from
        the remote.  This is part of the QoS=2 message send path.

        Parameters
        ----------
        reactor: Reactor
        pubrec: MqttPubrec
        """

    def on_pubcomp(self, reactor, pubcomp):
        """Called immediately upon receiving a `MqttPubcomp` packet
        from the remote.  This is part of the QoS=2 message send path.

        Parameters
        ----------
        reactor: Reactor
        pubcomp: MqttPubcomp
        """
        pass

    def on_puback(self, reactor, puback):
        """Called immediately upon receiving a `MqttPuback` packet from
        the remote.  This method is part of the QoS=1 message send path.

        Parameters
        ----------
        reactor: Reactor
        puback: MqttPuback
        """
        pass

    # Subscribe path
    def on_suback(self, reactor, suback):
        """Called immediately upon receiving a `MqttSuback` packet from
        the remote.

        Parameters
        ----------
        reactor: Reactor
        suback: MqttSuback
        """
        pass

    def on_unsuback(self, reactor, unsuback):
        """Called immediately upon receiving a `MqttUnsuback` packet
        from the remote.

        Parameters
        ----------
        reactor: Reactor
        unsuback: MqttUnsuback
        """
        pass

    # Receive path
    def on_publish(self, reactor, publish):
        """Called immediately upon receiving a `MqttSuback` packet from
        the remote.  This is part of the QoS=0, 1, and 2 message receive
        paths.

        Parameters
        ----------
        reactor: Reactor
        publish: MqttPublish
        """
        pass

    def on_pubrel(self, reactor, pubrel):
        """Called immediately upon receiving a `MqttPubrel` packet from
        the remote.  This is part of the QoS=2 message receive path.

        Parameters
        ----------
        reactor: Reactor
        pubrel: MqttPubrel
        """
        pass

    # Interface.
    def publish(self, topic, payload, qos, retain=False):
        """Places a publish packet on the preflight queue.  The reactor
        will make best effort to launch packets from the preflight queue
        and send them to the server.

        Parameters
        -----------
        topic: str
        payload: bytes
        qos: int
            0 <= qos <= 2
        retain: bool

        Raises
        ------
        haka_mqtt.exception.PacketIdReactorException
            Raised when there are no free packet ids to create a
            `MqttPublish` packet with.

        Return
        -------
        MqttPublishTicket
            A publish ticket.  The returned object will satisfy
            `ticket.status is MqttPublishStatus.preflight`.
        """
        # QoS = 0: Do not save to database.
        # QoS = 1: Save to database.
        # QoS = 2: Save to database.
        pass

    def start(self):
        pass
