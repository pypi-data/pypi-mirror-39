Swarm-Bus
=========

Client side implementation of an ESB via Amazon SQS.

Simple Usage
------------

::

    uri = 'sqs://LOGIN:PASSWORD@'
    transport = {
        'region': 'eu-west-1',
        'exchange': 'swarm',
        'queue_name_prefix': 'dev-%(hostname)s-',
        'office_hours': False,
        'use_priorities': True,
        'priorities': ['low', 'high']
    }
    queues = {
      'my_queue': {
          'route': 'my.queue.route',  # Specific route
          'sleep': 60,                # Seconds before next call to SQS
          'visibility': 1800,         # Visibility message in queue
          'wait': 10                  # Long polling seconds
      },
      'my_second_queue': {}           # Will be automaticaly filled/completed
    }

    bus = AMQP(uri, transport, queues)
    bus.connect()

    # We purge a known queue
    bus.purge_queue('my_queue')

    # Now we add a new queue on the fly
    bus.register_queue('new_queue', {'wait': 20})

    bus.close()


Using as a producer
-------------------

::

    with AMQP(uri, transport, queues) as producer:
        producer.publish(
            'my_queue',
            {'id': 42},
            1  # Optional, specify 'high' priority queue
        )


Using as a consumer
-------------------

::

    def print_routing_key(body, message):
        id_ = body['id']
        rk = message.delivery_info['routing_key']
        print("[x] %r:%r" % (rk, id_))

    def ack_message(body, message):
        message.ack()

    def error_handler(body, message):
        raise ValueError('Error while processing message')

    with AMQP(uri, transport, queues) as consumer:
        consumer.consume(
            'my_queue',
            [print_routing_key, ack_message],
            error_handler
        )
