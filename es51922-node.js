var express = require('express'),
  dgram = require("dgram");

var app = express(),
  udpserver = dgram.createSocket("udp4"),
  server = app.listen(8080, function() { console.log('Listening on port %d', server.address().port);});

var last_message = "DIGIT3A DIGIT3B DIGIT3C DIGIT3D DIGIT3E DIGIT3F DIGIT2A DIGIT2E DIGIT2F DIGIT2G DIGIT1A DIGIT1E DIGIT1F DIGIT1G" 

var io = require('socket.io').listen(server);

io.sockets.on('connection', function (socket) {
  socket.emit('new state', last_message);
  //socket.emit('news', { hello: 'world' });
  //socket.on('my other event', function (data) {
  //  console.log(data);
  //});
});

app.use(express.static(__dirname+'/static'));

udpserver.on("error", function (err) {
  console.log("server error:\n" + err.stack);
  udpserver.close();
});

udpserver.on("message", function (msg, rinfo) {
  console.log("server got: " + msg + " from " +
    rinfo.address + ":" + rinfo.port);
  io.sockets.emit('new state', msg.toString());
  last_message = msg.toString();
});

udpserver.on("listening", function () {
  var address = udpserver.address();
  console.log("server listening " +
      address.address + ":" + address.port);
});

udpserver.bind(5005);

// Push notification with JSON via socket.io: http://www.gianlucaguarini.com/blog/nodejs-and-a-simple-push-notification-server/
// UDP with dgram and websockets with socket.io: http://stackoverflow.com/a/9545426/183995
// How to use socket.io with Express 3: https://gist.github.com/dbainbridge/2424055

