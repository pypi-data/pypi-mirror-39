redisGroupMsg redis Queue multicast broadcast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

redis  Broadcasting to multiple queues
========================================

 Recently, I'm going to do something like chat software. After a lot of testing, I've done this thing.

    Performance is 13 times faster than py direct circular transmission


install ::

    pip install redisGroupMsg



python::

    from redisGroupMsg import redisMessage

    r = redisMessage()

    if __name__ == '__main__':
        for a in range(1,10):
            e = "id:"+str(a)
            # add queue of group
            # r.addGroup("test",e)
            # send message in group queue
            # r.sendGroup("test",e)
            # remove queue on group
            r.removeGroup("test",e)
