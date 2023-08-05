module.exports = function(myModule) {
    myModule.service('WebappService', [
    '$http', '$rootScope', '$location', '$cookies', 'NumbersConfig',
     function($http, $rootScope, $location, $cookies, NumbersConfig) {

        var target_url = NumbersConfig.remote_webapp + '/webapp_';

        function registerNewUser(contactNumber, hashed_password, name,
         age, height, weight, city, callback) {
            var payload = {'contact_number': contactNumber,
                           'hashed_password': hashed_password,
                            'name': name,
                            'age': age,
                            'height': height,
                            'weight': weight,
                            'city': city};
            var promise = $http.post(target_url+'register', payload).then(function (response) {
                cp = response.data;
                console.log('cp');
                console.log(cp);
                if(response.status === 200){
                    alert('Registration was successful, now you may login.');
                    $location.path('/login');

                }else{
                    alert('Error during registration.');
                    callback(cp);
                }
            });
        }

        function login(contactNumber, hashed_password, callback) {
            var payload = {'contact_number': contactNumber,
                           'hashed_password': hashed_password};
            var promise = $http.post(target_url+'login', payload).then(function (response) {
                cp = response.data;

                if(cp['data']['status'] === 200){
                    var expDatePageSize = new Date();
                    expDatePageSize.setDate(expDatePageSize.getDate() + 7);
                    $cookies.put('contactNumber', contactNumber, {'expires': expDatePageSize});
//                    $cookies.put('savePassword', true);
//                    if(savePassword){
//                        $cookies.put('hashed_password', hashed_password, {'expires': expDatePageSize});
//                        $rootScope.hashed_password = hashed_password;
//                    }
                    $rootScope.contactNumber = contactNumber;
//                    $rootScope.savePassword = savePassword;
                    $location.path('/index');
                }else{
                    alert('Error during login. User doesnt exist or password in not correct.');
                    callback(cp);
                }
            });
        }

        function add_post(contactNumber, title, description, callback) {
                    var payload = {'contact_number': contactNumber,
                                   'title': title,
                                   'description': description,
                                   'session': $cookies.get('session')};

                    var promise = $http.post(target_url+'add_post', payload).then(
                        function (response) {
                            cp = response.data;
                            console.log('cp');
                            console.log(cp);
                            if(cp['data']['status'] === 200){
                            alert('Post was successfully added');
                               console.log('response is 200');
                               $location.path('/mypage/' + contactNumber);
                            }else{
                                alert('Error during adding post.');
                                callback(cp);
                            }
                        }
                    );
                }

//     curl -X GET "localhost:9200/_search"
//     -H 'Content-Type: application/json'
//     -d'{"query":{"multi_match":
//     {"query": "seatch_text_here"}},
//      "_source": ["_id"]}'

        function getNumbersIdsByText(searchText, callback){
            var query_url = NumbersConfig.remote_webapp +'/webapp_search?text='+searchText;

            var promise = $http.get(query_url).then(function (response) {
                callback(response.data.data);
            });
        }

        return {
            registerNewUser:registerNewUser,
            login:login,
            add_post:add_post,
            getNumbersIdsByText:getNumbersIdsByText,
        }
    }]);
}
