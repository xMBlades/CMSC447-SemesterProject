var bubbles = document.getElementsByClassName("bbl");
for (i = 0; i < bubbles.length; i += 1){
	let bbl = bubbles[i];
	// bbl.classList.add("popped");
	bbl.addEventListener("animationend", function() 	{
		bbl.classList.remove("popped");
		
	});
	bbl.addEventListener("click", function() {
		bbl.classList.add("popped");
		// style.animation="spin2 4s linear infinite"
	});
}