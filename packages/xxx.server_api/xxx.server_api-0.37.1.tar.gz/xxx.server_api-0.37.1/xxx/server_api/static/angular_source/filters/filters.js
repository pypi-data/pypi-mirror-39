module.exports = function(myModule) {
     myModule.filter('startFrom', function() {
        return function(input, start) {
            start = +start; //parse to int
            return input.slice(start);
        }
     });
}
