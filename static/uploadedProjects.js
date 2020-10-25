$(function () {
    //used to pop in user detales 

   $.getJSON("/user_data_json", function(users){
       var checkBoxID = 0;

        $.each(users, function(user, values){
            $thumbnail = values["files"][0];
            $userName = values["userName"];
            $folderName = values["folderName"];
            $pubDate = values["pubDate"];
            $published = values["published"];

            var date = new Date($pubDate * 1000);
            var day = date.getDay();
            var month = date.getMonth();
            var year = date.getFullYear();
            dateStr = day + '/' + month + "/" +  year;

            var checkBox = '<td><input type="checkbox" id="pubCb' + String(checkBoxID++) + '"/></td>';
            userText = '<td > ' + $userName + '</td >' +  ' <td> '+ dateStr +'</td> '  + '<td>' + $folderName + "</td>" ;
            //userText = '<span class="userName"> ' + $userName + '</span >' +  ' <span class="date"> '+ dateStr +'</span> '  + '<span class="folderName">' + $folderName ;

            //$('<div class="user"> <img   src=' +"uploaded_images/"+ $folderName + '/' + $thumbnail +  '> ' + userText +   checkBox + '  </div>').insertAfter('.insideScroll');

            $('<tr>  <td><img   src=' +"uploaded_images/"+ $folderName + '/' + $thumbnail +  '></td>   ' + userText +   checkBox + '  </tr>').appendTo('table , #uploadsTable');
        });

    });

   
});