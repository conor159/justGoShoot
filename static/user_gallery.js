$(function (){

    $("#folderOptions").hide();

    $.getJSON("/fin_projects_json", function(listOfEnteries){
        if( listOfEnteries.length >1  ){
               //unhide dropdown
            $("#folderSelect").show();
            $("#folderOptions").show();
            $.each(listOfEnteries, function(inc, dict){
                $folderName = dict["folderName"];
                if(!inc){ $("#folderSelect").append("<option selected='selected' value='" + $folderName + "'>" + $folderName + "</option>"); }

                else{  $("#folderSelect").append("<option value='" + $folderName + "'>" + $folderName + "</option>");}

            });
        }

        firstFolder = listOfEnteries[0];
        $folderName = firstFolder["folderName"];
        $listOfFiles = firstFolder["files"];


        $.each($listOfFiles , function(inc , fileName){
            console.log(fileName);
            var rowCount = 1;
            var colCount = 1;
            //in here put in images put that in 3 times before the new row 
            if(  colCount % 3 == 0){
                $("#imageCollection").append($("<div class='row'></div>"));
            }

            var path =    "/uploaded_images/" + $folderName + "/" + fileName ;
            //leading slash important 
            //imageHtml = '<div class="col"> <img class = "lazy" data-src='  + path + ' id="' + fileName  + '></img> </div>';

            $('.row').prepend( "<div class = 'col'> </div>");
            $('.col').append($('<img>',{id: fileName ,src: path}))
            /// <img class="lazy" data-src="uploaded_images/testFolder1/Screenshot_from_2020-10-15_16-25-35.png" id="Screenshot_from_2020-10-15_16-25-35.png"> 
            colCount++;

        });






/* 
        $.each(listOfEnteries, function(inc, dict){
            $folderName = dict["folderName"];
            $listOfFiles = dict["files"];
            //eh right need to put in a select at the top and then 
            // fill in 50 images in grid thing 
            // bootstrap page thing
            du usefull command 

            });

*/

    });
});
