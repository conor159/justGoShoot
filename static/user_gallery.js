var pageNumber = 1;
var rowSize = 3;
var imagesPerPage = rowSize * 2;
var selectedFolder = 0;


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
        drawGallery(pageNumber);
    });


    $("#folderSelect").change(function(){
        selectedFolder = $(this).val();
        pageNumber = 1;
        drawGallery( pageNumber);
    });

    $("#download").on("click", function(){
        folderName = $("#folderSelect :selected").text();
        window.location.replace( "download/" +  folderName );
        
        
        
    });

});

function genNavLinks(){
    prev = '<li onClick="drawGallery('+(pageNumber -1)+ ')"  class="page-item"> <a id = "prev" class="page-link" href="#" aria-label="Previous"> <span aria-hidden="true">&laquo;</span> <span class="sr-only">Previous</span> </a> </li>';
    next = '<li onClick="drawGallery('+(pageNumber +1)+ ')" id="nextLi"  class="page-item"> <a id = "next" class="page-link" href="#" aria-label="Next"> <span aria-hidden="true">&raquo;</span> <span class="sr-only">Next</span> </a> </li>';
    $('.pagination').empty();
    $('.pagination').prepend(prev);
    $('.pagination').append(next);

    var imageLiMax = 4;
    //folder select might not exist deal with later
    selFolder = listOfFinProjGb[ $('#folderSelect').val() ]; 
    listOfFiles = selFolder["files"];
    numOfPages =  Math.ceil( listOfFiles.length / imagesPerPage);
    lowerLimit = pageNumber - imageLiMax;
    var windowSlider = 0;

    if( lowerLimit < 1 ){ 
        windowSlider = lowerLimit * - 1;
        lowerLimit = 1;
    };

    upperLimit = pageNumber + imageLiMax; 
    if ( upperLimit >  numOfPages ){
         upperLimit =  numOfPages;
    };

    for(var i = lowerLimit; i <= upperLimit; i++ ){
        if(i == pageNumber){
            $("#nextLi").before('<li id="pageNum' + i + '" class="page-item active"><a onClick="drawGallery('+ i +')"  class="page-link" href="#"><span>'+  i  + '</span></a></li>');
        }
        else{
            $("#nextLi").before('<li id="pageNum' + i + '" class="page-item"><a onClick="drawGallery('+ i +')"  class="page-link" href="#"><span>'+  i  + '</span></a></li>');
        }
    }


    $("#prev").show(); 
    $("#next").show(); 
    if( pageNumber == 1){
        $("#prev").hide(); 
    }

    if( pageNumber == numOfPages){
        $("#next").hide(); 
    }


}




function drawGallery(requestPage){
    pageNumber = requestPage;
    pageNumber = requestPage;
    $('#gallery').empty();
    rowCount = 0; 

    selFolder = listOfFinProjGb[selectedFolder];
    folderName = selFolder["folderName"];
    listOfFiles = selFolder["files"];

    // starting point of where we start drawing images
    firstImage = (pageNumber-1) * imagesPerPage ;
    lastImage = pageNumber * imagesPerPage;
    imageIndex = firstImage;

    while( imageIndex < lastImage && imageIndex < listOfFiles.length ){
        fileName = listOfFiles[imageIndex];
        if(  imageIndex % rowSize == 0){
            rowCount++;
            $("#gallery").append($("<div id='row"+rowCount+ "'" + " class='row'></div>"));
        }

        var path = "/uploaded_images/" + folderName + "/" + fileName ;

        $("#" + "row" + rowCount).append( "<div id ="+ imageIndex +" class = 'col'> </div>");
        $("#" + imageIndex  ).append($('<img>',{id: fileName ,src: path, class: "lazy"}))
        imageIndex++
    }
    genNavLinks();
};


