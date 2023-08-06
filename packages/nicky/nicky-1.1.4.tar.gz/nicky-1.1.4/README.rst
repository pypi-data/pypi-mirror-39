Nicky
-------------
.. image:: https://badge.fury.io/py/nicky.svg
    :target: https://badge.fury.io/py/nicky


Nicky is the nicknamer. You can make funny nickname with nicky!

How to use
==============

1. with pip
^^^^^^^^^^^^

.. code::

    # install local env
    pip install nicky

    # or install globally.
    pip install --user nicky

    nicky name
    > 향긋한 까치

    nicky name 5
    > 신성한 스콘
    > 똘망똘망한 오미자차
    > 향긋한 스테이크
    > 활기찬 사탕
    > 엄청난 순대
..

2. with code
^^^^^^^^^^^^

.. code::

    git clone git@github.com:joyongjin/Nicky.git
    cd Nicky

    python3 ./nicky-cli name
    > 향긋한 까치

    python3 ./nicky-cli name 5
    > 신성한 스콘
    > 똘망똘망한 오미자차
    > 향긋한 스테이크
    > 활기찬 사탕
    > 엄청난 순대
..

If you want more, just type :code:`nicky [command] --help`


Localization and more nicknames
-----------------------------------

Folk and clone this project. and add your language code folder in :code:`nicky/nicknames`

After then, you can use :code:`nicky-cli.py` to add your nickname prefix and suffix.

.. code::

    python3 nicky-cli.py add [prefix|suffix|pre|suf|p|s] {values} [-l|--lang] {language}
..

    You can add multiple values. Separate your values with comma like :code:`a,b,c`. Remember, there's no space.

**example)**

.. code::

    python3 nicky-cli.py add pre melon,potato,tomato --lang en
..

After all, pull requests to master branch.