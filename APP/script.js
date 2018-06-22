document.addEventListener("DOMContentLoaded", () => {
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		console.log(e.target.value);
		// GET data from server for rendering
	})
})
