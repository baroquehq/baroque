Baroque: events made easy
=========================

Hi, welcome to Baroque's documentation!

**Baroque is a convenient event broker and an extensible framework for building
event-driven applications.**

The best way to get started is to explore some real life scenarios in which
Baroque may help you with:

  - you want to keep in sync the values of two different properties of different
    software objects (as they change)
  - you want to log each and only deletion in a database table
  - you want to send a push notification to your devices every time an
    exception is raised in your super-critical production web applications
  - you want a selected pool of persons in the marketing division of your
    company to get an e-mail whenever somebody places a post on your company's
    blog and that post contains specific words

...and so forth!

Baroque allows you to **build higher level abstractions on the fundamental messaging pattern** it implements: Publish-Subscribe_


.. _Publish-Subscribe: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern

That's because you don't have to think about it - Baroque does the job for you
and you're free to focus on building valuable software that leverages the
pattern

Baroque behaviour can be easily configured through a YAML file.

Read on and get more details in the next sections

Guides
======

.. toctree::
   :maxdepth: 1

   usage
   examples
   configuration
   persistence

Baroque API documentation
=========================

.. toctree::
   :maxdepth: 1

   baroque


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`