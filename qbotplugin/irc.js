(function() {
  module.exports = function(content, send, robot, message) {
      return robot.request.get({
        url: "http://localhost:12125/send?msg=" + content,
        json: true
      }, function(data) {
        console.log(data.success);
      });
  };
}).call(this);
