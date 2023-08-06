.. image:: https://travis-ci.org/madedotcom/striemann.svg?branch=master
    :target: https://travis-ci.org/madedotcom/striemann
.. image:: https://readthedocs.org/projects/striemann/badge/?version=latest
    :target: http://striemann.readthedocs.io/en/latest/

Striemann provides a developer friendly interface for sending metrics to the Riemann_ monitoring system. It's heavily inspired by statsd.
It aims to provide a strongly opinionated way for developers to record metrics from their applications.

Installation
------------

Striemann is available on the `cheese shop`_.

:code:`pip install striemann`

Documentation is available on `Read the Docs`_

Basic Usage
-----------

.. code-block:: python

        from striemann import RiemannTransport, Metrics

        # Transports are responsible for sending metrics to an endpoint
        transport = RiemannTransport("localhost", 5555)

        # the Metrics class is the entrypoint for the library
        metrics = Metrics(transport)

        # Counters keep track of how often a thing happens.
        # They send the sum of their metrics when flushed.
        metrics.incrementCounter("Burgers sold")
        metrics.incrementCounter("Burgers sold")

        metrics.incrementCounter("Days without an incident", value=2)
        metrics.decrementCounter("Days without an incident", value=2)

        # Gauges track a single value. They send the most recent value
        # when flushed.
        metrics.recordGauge("Awesomeness", value=10)
        metrics.recordGauge("Awesomeness", value=100)

        # Timers record how long it takes a thing to happen.
        # They send the min, max, mean, and count of their recorded values when flushed
        with metrics.time("Do a slow thing"):
            time.sleep(5)


        # periodically you should flush metrics
        metrics.flush()

.. _cheese shop: https://pypi.org/project/striemann/
.. _Riemann: http://riemann.io
.. _read the docs: http://striemann.readthedocs.io/ 
