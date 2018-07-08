document.addEventListener("DOMContentLoaded", () => {
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		if(e.which === 13)
			console.log(e.target.value);
		// GET data from server for rendering
	})
})
