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


        $.each($listOfFiles , function(inc , item){
            //eh right need to fill in the images one at  time

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
