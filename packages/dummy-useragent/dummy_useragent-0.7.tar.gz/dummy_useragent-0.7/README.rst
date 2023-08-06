dummy_useragent
---------------
random usergent for china python developer

dummy_useragent vs faker_useragent
----------------
faker_useragent  will download useragent from [useragentstring.com] when it initialize,dummy_useragent has built-in useragents,and dummy_useragent can refresh useragent from [useragentstring.com]


Install
--------------
.. code-block:: python

    pip install dummy_useragent


Usage
----------------
just like faker_useragent

.. code-block:: python

    >>from dummy_useragent import UserAgent
    >>UserAgent().random()
    'Mozilla/5.0 (X11; U; Linux i686; rv:1.7.3) Gecko/20041020 Firefox/0.10.1'

get special browser agent
.. code-block:: python

    >>chrome = UserAgent().Chrome
    >>chrome.choice()
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

