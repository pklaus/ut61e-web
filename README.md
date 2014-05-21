ut61e-web
=========

A web interface for the display of a UNI-T UT61E digital multimeter.

Start using:

    ./webserver.py

and feed using live-data:

    he2325u_hidapi.py | while read x; do echo "$x" | ncat -4u localhost 5005; done

or using a pre-recorded data file:

    while read x; do sleep 0.49; echo "$x" | ncat -4u localhost 5005; done < testdata.txt

