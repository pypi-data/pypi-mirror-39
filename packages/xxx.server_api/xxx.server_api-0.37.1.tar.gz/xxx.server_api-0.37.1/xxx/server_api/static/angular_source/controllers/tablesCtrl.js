module.exports = function(myModule) {
    myModule.controller('tablesCtrl',[
      '$scope', '$http', '$rootScope', '$cookies',  'CouchdbService', 'WebappService',
      function ($scope, $http, $rootScope, $cookies, CouchdbService, WebappService) {
           // check if user is logged in
           if($cookies.get('contactNumber')){$rootScope.contactNumber = $cookies.get('contactNumber')};

           $scope.numberOfPages=function(){
                   return Math.ceil($rootScope.numbersCount/$scope.pageSize);
                }
           $rootScope.pageSizes = [10, 20, 50, 100, 500];

           if($cookies.get('pageSize')){
               $rootScope.pageSize = parseInt($cookies.get('pageSize'));
           } else {
               $rootScope.pageSize = 10;
           }
           if($cookies.get('currentPage')){
               $scope.currentPage = parseInt($cookies.get('currentPage'));
           } else {
               $scope.currentPage = 0;
           }
           $scope.updateNumbersBlock = function(page_number1){

               var expDatePageSize = new Date();
               expDatePageSize.setDate(expDatePageSize.getDate() + 90);
               // Setting a cookie
               $cookies.put('pageSize', $scope.pageSize, {'expires': expDatePageSize});
               CouchdbService.getNumbersBlock(page_number1, $scope.pageSize, function (numbers){
                   $scope.numbers = numbers;
               });
           };

           CouchdbService.getNumbersBlock($scope.currentPage, $scope.pageSize, function (numbers){
                $scope.numbers = numbers;
                $scope.back_up_numbers = numbers;
           });

           $scope.incrPageNumber = function(jump){
               $scope.currentPage = $scope.currentPage + jump;
               CouchdbService.getNumbersBlock($scope.currentPage, $scope.pageSize, function (numbers){
                   $scope.numbers = numbers;
               });
           };

           $scope.decrPageNumber = function(jump){
               $scope.currentPage = $scope.currentPage - jump;
               CouchdbService.getNumbersBlock($scope.currentPage, $scope.pageSize, function (numbers){
                   $scope.numbers = numbers;
               });
           };

    //     for sorting
           $scope.sortColumn = "value.last_post_date";
           $scope.reverseSort = false;
           $scope.sortData = function(column){
              $scope.reverseSort = ($scope.sortColumn == column) ? !$scope.reverseSort : false ;
              $scope.sortColumn = column;
           };
           $scope.getSortClass = function(column){
              if ($scope.sortColumn == column){
                  return $scope.reverseSort ? "arrow-down" : "arrow-up";
              }
              return '';
           };

           // for elastic search
           $scope.elasticsearch = function(){
              if($scope.elasticSearchText){
                WebappService.getNumbersIdsByText($scope.elasticSearchText,
                 function (hits){
                    $scope.hits = hits['hits']['hits'];
                    if ($scope.hits){
                        var hits_ids = [];
                        for (i=0; i<$scope.hits.length; i++){
                            hits_ids.push($scope.hits[i]['_id']);
                        }
                        var new_numbers = [];
                        for (i=0; i<$scope.back_up_numbers.length; i++){
                            if(hits_ids.includes($scope.back_up_numbers[i].id)){
                                new_numbers.push($scope.back_up_numbers[i]);
                            }
                        }
                        $scope.numbers = new_numbers;
                     } else {
                         $scope.numbers = $scope.back_up_numbers;
                     }
                });
              } else {
                  $scope.numbers = $scope.back_up_numbers;

              }
           };

    }]);
}
