var imageCount = 0;
var pageNumber = 1;
var rowSize = 4;
var imagesPerPage = rowSize * 2;


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

    // work out the number of pages needed then generate a image nav with required number of links 
    //$("#pageNum0").after('<li id="pageNum1" class="page-item"><a class="page-link" href="#"><span>2</span></a></li>');


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
        next();
    });



});

function genNavLinks( ){
    //folder select might not exist deal with later
    selFolder = listOfFinProjGb[ $('#folderSelect').val() ]; 
    listOfFiles = selFolder["files"];
    numOfPages =   Math.ceil( listOfFiles.length / imagesPerPage);
    for(var i = 1; i < numOfPages; i++){
        $("#pageNum" + i  ).remove();
    }

    for(var i = 1; i < numOfPages; i++){
        $("#numNav" ).before('<li id="pageNum' + i + '" class="page-item"><a class="page-link" href="#"><span>'+ (pageNumber + i -1 ) + '</span></a></li>');
    }
}

function next(){
    $('#gallery').empty();
    pageNumber += 1;
    brakePoint = imagesPerPage * pageNumber;
    //console.log("imagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount +  " imageCount: " + imageCount + " listOfFiles: " + listOfFiles.length );
    firstNImages(brakePoint , selFolderVal = $('#folderSelect').val() );

}




function firstNImages(brakePoint, selFolderVal){
    genNavLinks();

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
        if(  imageCount % rowSize == 0){
            rowCount++;
            $("#gallery").append($("<div id='row"+rowCount + "'" + " class='row'></div>"));
        }

        var path = "/uploaded_images/" + folderName + "/" + fileName ;
        //console.log(path + " " + pageNumber);
        $("#" + "row" + rowCount).append( "<div id ="+ imageCount +" class = 'col'> </div>");
        $("#" + imageCount  ).append($('<img>',{id: fileName ,src: path, class: "lazy"}))
        imageCount++
        colCount ++

    }
    //console.log("ImagesPerPage: " + imagesPerPage + " brakePoint: " +  brakePoint + " pageNumber: " +   pageNumber +  " rowCount: " + rowCount +  " imageCount: " + imageCount + " listOfFiles: " + listOfFiles.length + " colCount: " + colCount);
};


