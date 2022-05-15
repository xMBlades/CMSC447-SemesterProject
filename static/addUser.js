
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
var onField = 0;
var dupeUsr = false;
// var eobj = null;
function unAjaxCheck(data, evntobj){
    console.log(data);
          if (data.includes("false")){
              dupeUsr = false;
              moveToNextPage(evntobj);
              return true;
            //   return nextClick();
              
          }
          else{
              
              dupeUsr = true;
              return false;
            //   return nextClick();
          }
}
var numLangs = 0;
var langs = [];

$("#langSelectorButton").click(function(event){
		 event.preventDefault();
   $(".langList").append( "<div id = 'lang"+ numLangs +"'' class = 'adtnlLang'>" + $("#langSelectBox").val() + "</div>" );
     langs.push($("#langSelectBox").val());
   $("#lang"+ numLangs).click(function(event){
     event.preventDefault();
     // event.target.hide();
      event.target.style.display = "none";
     
      let v = event.target.innerHTML;
     let i = langs.indexOf(v);
     console.log(i);
      if (i > -1) {
        langs.splice(i, 1);
      }
     
       console.log(langs);
     
     // console.log("help!  " + event.target.style.display);
   });
  console.log(langs);
  numLangs++;
 });


function nextClick(evntobj){
    if(animating) return false;
  if (onField === 0){
    if($('#pass'). val() === undefined || $('#cpass'). val() === undefined || $('#email'). val() === undefined || $('#usrname'). val() === undefined){
      
       $('#emptyFieldAlert').show();
      return false;
    }
    var passA = $('#pass'). val();
    var passB = $('#cpass'). val();
    
    
    
    //console.log(passA);
    if (passA != passB || passA === ''){
      $('#wrongPassAlert').show();
      return false;
    }
    
    if (passA.length < 6){
      $('#shortPassAlert').show();
      return false;
    }
    
    // $.ajax({
    //       type: 'POST',
    //       url: "https://xarodispatch.com/dispatcher/z810ij53sc/userExists.php",
    //       data: {username :  $('#usrname'). val()},
    //       async:false
    //     }).done(function( data ) {
    //             unAjaxCheck(data, evntobj);
    //         });
    
    
    
    // if (dupeUsr){
    //     $('#dupeUserAlert').show();
    //     ajaxChecked = false;
    //     dupeUsr = false;
    //     return false;
    // }
    moveToNextPage(evntobj);
    
  }
  else{
      moveToNextPage(evntobj);
  }
  
}

function moveToNextPage(evntobj){
    	animating = true;
	$('#emptyFieldAlert').hide();
  $('#wrongPassAlert').hide();
   $('#dupeUserAlert').hide();
	current_fs = $(evntobj).parent();
	next_fs = $(evntobj).parent().next();
	onField++;
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
}


$(".next").click(function(){
	nextClick(this);
});






$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	onField--;
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});



function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#imageUpload").change(function() {
    readURL(this);
});


