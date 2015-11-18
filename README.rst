Bouncer python client
=====================

A python client for the bouncer_ A/B testing and feature switching service.

.. _Bouncer: http://github.com/Memrise/bouncer

Getting started
---------------

    from bouncer import Bouncer

    bc = Bouncer(service_url='http://localhost:5000')  # default value

    # Get the current configuration
    bc.configured_experiments()
    bc.configured_features()
    bc.configured_groups()

    # Get service stats, load times etc
    bc.stats()

    # Participate in AB tests and get featured courses
    features, experiments, bc.paricipate("youruid")