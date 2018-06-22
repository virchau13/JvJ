$(document).ready(() => {
	let searchbar = $("#search")
	searchbar.on("change",(e) => {
		console.log(e.target.value)
		// GET data from server for rendering
	})
})