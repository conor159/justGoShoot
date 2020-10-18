$(function () {
    //$('#logo img').hide();
    //$('#logo img').fadeIn(1000);
    $('#logo img').hide();
    $('#imageCollection img').hide();
    $('#logo img').fadeIn(1000);

    var i=0;
    var imageList = [4,5,6,7,8,9,10];
    while(i < imageList.length){
        k=i+4;
        randNumber=Math.random() * 2000;
        $('#img'+k).attr('src', 'static/images/image'+imageList[i]+'.jpg').fadeIn(randNumber);
        i++;
    }

    //lazy loading images on gallery page to improve load times
    $('.lazy').Lazy();

});

