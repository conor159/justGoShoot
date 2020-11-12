var imageCount = 0;
var pageNumber = 1;
var imagesPerPage = 9;

var listOfFinProjGb;
$(function (){
    $("#folderOptions").hide();
    $("#prev").hide();
    //need to use thumnails
    //need a download high res thing
    //need a click on image thing with the socals

    $.getJSON("/fin_projects_json", function(listOfFinProj){
        listOfFinProjGb = listOfFinProj;
        if( listOfFinProj.length >1  ){
            $("#folderSelect").show();
            $.each(listOfFinProj, function(inc, dict){
                $folderName = dict["folderName"];
                if(!inc){ $("#folderSelect").append("<option selected='selected' value='" + inc + "'>" + $folderName + "</option>"); }

                else{  $("#folderSelect").append("<option value='" + inc + "'>" + $folderName + "</option>");}

            });
        }

        //need to wait untill json has loaded you idiot
        firstNImages(brakePoint = imagesPerPage, selFolderVal = 0);
    });


    $("#folderSelect").change(function(){
        $('#gallery').empty();
        imageCount=0;
        rowCount=0;
        firstNImages(brakePoint = imagesPerPage, selFolderVal = $(this).val() );
    });



    $("#prev").on("click", function () {
        $('#gallery').empty();
        pageNumber--;
        imageCount =  imageCount- (colCount + imagesPerPage)

        brakePoint = imagesPerPage * pageNumber;

        if( imageCount < imagesPerPage ||pageNumber == 1){
            firstNImages(brakePoint , selFolderVal = $('#folderSelect').val() );
            //console.log("imagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount + " colCount: "  + colCount + " imageCount: " + imageCount);
        }
        else{
            firstNImages(brakePoint , selFolderVal = $('#folderSelect').val() );
        }
    });

    $("#next").on("click", function () {
        $('#gallery').empty();
        pageNumber += 1;
        brakePoint = imagesPerPage * pageNumber;
        //console.log("imagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount +  " imageCount: " + imageCount + " listOfFiles: " + listOfFiles.length );
        firstNImages(brakePoint , selFolderVal = $('#folderSelect').val() );
    });
});





function firstNImages(brakePoint, selFolderVal){
    rowCount=0;
    colCount=0;
    selFolder = listOfFinProjGb[selFolderVal];
    folderName = selFolder["folderName"];
    listOfFiles = selFolder["files"];


    if(brakePoint >= imageCount ){
        $("#next").hide();
        $("#prev").show();
    }


    if(listOfFiles.length > brakePoint ){
        $("#next").show();
    }

    if(pageNumber == 1 ){
        $("#prev").hide();
    }

    if( pageNumber > 1 ){
        $("#prev").show();
    }

    //console.log("ImagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount +  " imageCount: " + imageCount + " listOfFiles: " + listOfFiles.length );
    while( imageCount < brakePoint && imageCount < listOfFiles.length ){
        fileName = listOfFiles[imageCount];
        //col width of 3 
        //I need to rewrite this weid stuff with rows going missing on image per page 10 
        console.log(imageCount % 3);
        if(  imageCount % 3 == 0){
            console.log("createing a new row :" +  imageCount % 3);
            rowCount++;
            $("#gallery").append($("<div id='row"+rowCount + "'" + " class='row'></div>"));
        }

        var path = "/uploaded_images/" + folderName + "/" + fileName ;
        console.log(path + " " + pageNumber);
        $("#" + "row" + rowCount).append( "<div id ="+ imageCount +" class = 'col'> </div>");
        $("#" + imageCount  ).append($('<img>',{id: fileName ,src: path, class: "lazy"}))
        imageCount++
        colCount ++

    }
    console.log("ImagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount +  " imageCount: " + imageCount + " listOfFiles: " + listOfFiles.length + " colCount: " + colCount);
};


//need to 
//on click plus incement image count by breakpoint * page number and then clear and reset page-->
