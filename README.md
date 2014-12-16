ut61e-web
=========

A web interface for the display of a UNI-T UT61E digital multimeter
written as a node.js application with socket.io websocket support.

Start using:

    node es51922-node.js

and feed using live-data:

    he2325u_hidapi.py | ./es51922-to-lcd.py | while read x
    do
      echo "$x" | ncat -4u localhost 5005
    done

or using a pre-recorded data file:

    while true
    do
      cat testdata.txt | ./es51922-to-lcd.py | while read x
      do
        echo "$x" | ncat -4u localhost 5005
        sleep 0.495
      done
    done

### Requirements

You need Python and node.js
The Python module *ut61e* is required as well as the node.js modules
*socket.io* and *express*.

