let ipaddr = '0.0.0.0';

function fetcherror(str){
	// TODO: add UI of error
	alert(str)
}

document.addEventListener("DOMContentLoaded", () => {
	// searchbar controls
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		if(e.which === 13){
			// make loading bar
			document.getElementById('searchbar').innerHTML = `<div id="loader" style="border: 8px solid #f3f3f3; 
			border-top: 8px solid #555;
			border-radius: 50%;
			width: 50px;
			height: 50px;
			margin-left: 30%;
			animation: spin 2s linear infinite;"></div><br><p> Loading search results... </p>`
			// GET data from server for rendering
			fetch("http://" + ipaddr + ":5000/scrape?querystring=" + e.target.value)
			.then((res) => res.ok ? res.json() : fetcherror('ERROR fetching from 192.168.1.81:5000/?query=' + e.target.value + '. HTTP Response code is ' + res.status))
			.then((data) => {document.body.removeChild(document.getElementById('searchbar')); console.log(data); tags = Object.entries(data).sort((a,b)=>b[1]-a[1]).slice(0, 100 + 1).map(e=>{return{'key': e[0], 'value': e[1]}}); update();
			
			});
		}
	})

	
})


var tags;

var fill = d3.scale.category20b();

var w = window.innerWidth,
        h = window.innerHeight;

var max,
        fontSize;

var layout = d3.layout.cloud()
        .timeInterval(Infinity)
        .size([w, h])
        .fontSize(function(d) {
            return fontSize(+d.value);
        })
        .text(function(d) {
            return d.key;
        })
        .on("end", draw);

var svg = d3.select("#cloud-container").append("svg")
        .attr("width", w)
        .attr("height", h);

var vis = svg.append("g").attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

window.onresize = function(event) {
    update();
};

function draw(data, bounds) {
    var w = window.innerWidth,
        h = window.innerHeight;

    svg.attr("width", w).attr("height", h);

    scale = bounds ? Math.min(
            w / Math.abs(bounds[1].x - w / 2),
            w / Math.abs(bounds[0].x - w / 2),
            h / Math.abs(bounds[1].y - h / 2),
            h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;

    var text = vis.selectAll("text")
            .data(data, function(d) {
                return d.text.toLowerCase();
            });
    text.transition()
            .duration(1000)
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            });
    text.enter().append("text")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            })
            .style("opacity", 1e-6)
            .transition()
            .duration(1000)
            .style("opacity", 1);
    text.style("font-family", function(d) {
        return d.font;
    })
            .style("fill", function(d) {
                return fill(d.text.toLowerCase());
            })
            .text(function(d) {
                return d.text;
            });

    vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
}

function update() {
    layout.font('impact').spiral('archimedean');
    fontSize = d3.scale['sqrt']().range([10, 100]);
    if (tags.length){
        fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
    }
    layout.stop().words(tags).start();
}
