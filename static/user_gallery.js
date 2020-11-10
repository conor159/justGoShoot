$(function (){
    $("#folderOptions").hide();
    //need to use thumnails
    //need a download high res thing
    //need a click on image thing with the socals

    $.getJSON("/fin_projects_json", function(listOfEnteries){
        if( listOfEnteries.length >1  ){
            $("#folderSelect").show();
            $("#folderOptions").show();
            $.each(listOfEnteries, function(inc, dict){
                $folderName = dict["folderName"];
                if(!inc){ $("#folderSelect").append("<option selected='selected' value='" + inc + "'>" + $folderName + "</option>"); }

                else{  $("#folderSelect").append("<option value='" + inc + "'>" + $folderName + "</option>");}

            });
        }

        //when dorpdown selected cnange listOfenterys and run each again with  clear screen
        firstFolder = listOfEnteries[0];
        $folderName = firstFolder["folderName"];
        $listOfFiles = firstFolder["files"];


        var rowCount = 0;
        var colCount = 0;
        $.each($listOfFiles , function(inc , fileName){
            //in here put in images put that in 3 times before the new row 
            
            // probs need to limit col count to somthing like 50 and then create a new page yay
            if(  colCount % 3 == 0){
                rowCount++;
                $("#imageCollection").append($("<div id='row"+rowCount + "'" + " class='row'></div>"));
            }
            var path = "/uploaded_images/" + $folderName + "/" + fileName ;
            $("#" + "row" + rowCount).append( "<div id ="+ inc +" class = 'col'> </div>");
            $("#" + inc  ).append($('<img>',{id: fileName ,src: path, class: "lazy"}))
            colCount++;

        });
    });
});
