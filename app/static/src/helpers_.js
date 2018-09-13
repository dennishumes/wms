keepForm = false;
$(function(){
	$(".amodule").bind("click",openSetModule);
	$(".aview").bind("click",openSetModuleView);
	$(".asection").bind("click",setModuleViewSection);
	$("#add_multi_bins").bind("click",intiMultiBins);
	$("input#name").bind("click",setMultiBinFlagToZero);
	$("input#name").bind("change",validateMultiBinsEntry);
	$("input#depth").bind("change",validateDepthEntry);

	if($("input#module_selc").val() > 0)
		reveilAccess();
	if($("input#multi").val() > 0)
		$("#add_multi_bins").click();
});

function validateDepthEntry(){
	var val = parseInt($(this).val());
	if(!Number.isInteger(val)){
		$("input#submit").attr("disabled",true);
		flash("Input Error: Invalid bin depth entry. bin depth should be an integer that indicates how many full pallets can hold in a bin.");
	}else{
		$("input#submit").attr("disabled",false);

	}
}

function setMultiBinFlagToZero(){
	$("input#multi").val(0);
}

function reveilAccess(){
	keepForm = true;

	var module = $("input#module_selc").val();
	var view = $("input#view_selc").val();
	var section = $("input#section_selc").val();
	var permission = $("input#permission_selc").val();
	$("#mod_"+module+".amodule").click();

	setTimeout(function(){
		$("#view_"+view+".aview").click();
		setTimeout(function(){
			$("#section_"+section+".asection").click();
			setTimeout(function(){
				$("input:radio[name='permission']:eq("+( permission - 1 )+")").click();
			},500);
		},500);
	},500);
	
	console.log("unveiling access....");
}

function intiMultiBins(){	
	if($(this).hasClass("active fa faa-shake animated")){
		$("input#name").attr("placeholder","2500A");
		$("input#multi").val(0);
		$("input#submit").attr("disabled",false);
	}else{
		$("input#name").attr("placeholder","Add Bins Separated by commas eg. 2500A,2500B,2500C...ect,ect.")
		$("input#depth").attr("placeholder","What is the depth of these Bins eg. 1")
		
		if($("input#multi").val() == 1){
			$("input#submit").attr("disabled",false);
		}else{
			$("input#submit").attr("disabled",true);
			$("input#multi").val(1);
		}
	}
	
	$(this).toggleClass("active fa faa-shake animated");
}

function validateMultiBinsEntry(){
	var bins = $(this).val().split(",");

	if($("#add_multi_bins").hasClass("active"))
		if(bins.length < 2){
			flash("Feature Error: Enter comma separated values to add multiple bins. If you are adding a single bin click the multi-bin button below.")
		}else{
			$("input#multi").val(1);
			$("input#submit").attr("disabled",false);
		}
	else{
		if(bins.length > 1){
			flash("Feature Error: Single bin mode. use the multi-bin function to add multiple bins.")
			$("input#submit").attr("disabled",true);

		}else{
			$("input#submit").attr("disabled",false);
		}
	}
}

function openSetModule(){
	$(this).toggleClass("highlight");
	$(this).siblings().removeClass("highlight");
	$(this).siblings().children().removeClass("highlight")
	$(this).siblings().children().children().removeClass("highlight")
	if(!keepForm)
		resetSelects();

	var module = $(this).attr("id");
	var module_val = $(this).attr("data");
	var module_view = $("#"+module+".views_");
	// close all active module views
	$(".views_").removeClass("active");
	// open this modules view
	module_view.toggleClass("active");
	// set module value to selected modules
	$("input#module_selc").val(0)
	if($(this).hasClass("highlight"))
		$("input#module_selc").val(module_val);
	else
		module_view.toggleClass("active");

	console.log("showing views for module.");
}

function openSetModuleView(){
	$(this).toggleClass("highlight");
	$(this).siblings().removeClass("highlight");
	var view = $(this).attr("id");
	var view_val = $(this).attr("data");
	var view_section = $("#"+view+".sections_");
	// close all active module views
	$(".sections_").removeClass("active");
	// open this modules view
	view_section.toggleClass("active");
	// set module value to selected modules
	$("input#view_selc").val(0)
	if($(this).hasClass("highlight"))
		$("input#view_selc").val(view_val);
	else
		view_section.toggleClass("active");

	console.log("showing sections for view.");
}

function setModuleViewSection(){
	$(this).toggleClass("highlight");
	$(this).siblings().removeClass("highlight");
	var section = $(this).attr("id");
	var section_val = $(this).attr("data");
	
	// set section value 
	$("input#section_selc").val(0);
	if($(this).hasClass("highlight"))
		$("input#section_selc").val(section_val);
	
	keepForm = false;
	console.log("setting section.");
}

function resetSelects(){
	$("input#module_selc").val(0)
	$("input#view_selc").val(0);
	$("input#section_selc").val(0);
	$("input:radio[name='permission']").attr('checked',false);
}

function flash(msg){
	$("div.content-section").prepend("<div id='flash_msg' class='alert alert-info' role='alert'>"+msg+"<span id='flash_msg_cls'></span></div>");
	$("#flash_msg_cls").click(function(){
		$(this).parent().remove();
	});
}