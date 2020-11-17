$(function () {


   $.getJSON("/jsonOfImages", function(users){
       //fills in table on admin page 

        $.each(users, function(user, values){
            $imageName = values["files"]
            $userName = values["userName"];
            $folderName = values["folderName"];
            $pubDate = values["pubDate"];
            $published = values["published"];

            var date = new Date($pubDate * 1000);
            var day = date.getDay();
            var month = date.getMonth();
            var year = date.getFullYear();
            dateStr = day + '/' + month + "/" +  year;

            var checkBox = '<td><input type="checkbox"  class="pubCheckbox" id="pubCb_' + $folderName + '"/></td>';
            userText = '<td > ' + $userName + '</td >' +  ' <td> '+ dateStr +'</td> '  + '<td>' + $folderName + "</td>" ;


            $('<tr>  <td><img id=' + $folderName + '  src=' +"uploaded_images/"+ $folderName + '/thumbnail/' + $imageName +  '></td>   ' + userText +   checkBox + '  </tr>').appendTo('table , #uploadsTable');
            $("#pubCb_" + $folderName  ).prop('checked', Number( $published));

            if( $published == "1"){
                $("#pubCb_" + $folderName  ).prop('disabled', "readonly");
            }
        });

        userEmails = users.map(user => user.email);
        $('#autocomplete').autocomplete({
            lookup: userEmails,
            onSelect: function (suggestion) {
                console.log(userEmails);
            }
        });
    });
});





$(document).on( 'click', 'img', function () { 
    console.log(this.id);
    //gall go to page with args
});


$(document).on("change", ".pubCheckbox", function(){
    if( $(this).prop("checked") == true){
        var folderName = this.id.split("_")[1];
        cbID = this;
        $('#publishModal').modal('show');


        $("#pubCancel").click(function (e) { 
            $(cbID).prop( "checked", false);
        });

        $("#pubSubmit").click(function (e) { 
            $(cbID).prop('disabled', "readonly");
            $('#publishModal').modal('hide');
            $.post("/publish", {folder_name : folderName} );
        });
            
        

    }
});

/*
   $.getJSON("/get_users", function(users){
       // for autocomplete user email in upload 

        userEmails = users.map(user => user.email);
        $('#autocomplete').autocomplete({
            lookup: userEmails,
            onSelect: function (suggestion) {
                console.log(userEmails);
            }
        });
   });
*/
