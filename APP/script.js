var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (!mutation.addedNodes) return
      for (var i = 0; i < mutation.addedNodes.length; i++) {
        if([...document.querySelectorAll('text')].filter(e=>e.parentNode.nodeName==='g').length === 101){
            [...document.querySelectorAll('text')].forEach(e=>e.addEventListener('click', textfly))
        }
      }
    })
  })
  
function textfly(e){

    fetch('http://127.0.0.1:5000/relatedWords?querystring=' + last_searched + '&wordSearch=' + e.target.innerHTML)
    .then(res=>res.ok ? res.json() : console.error('http error ' + res.status))
    .then(obj=>{document.body.innerHTML += '<div><div id="related-words-fix"><b><u>Related Words</u></b><br>' + obj.join('<br>') + '</div></div>';

    [...document.querySelectorAll('text')].filter(x=>x.innerHTML!==e.target.innerHTML).forEach(e=>{e.style.animation = 'moveoffscreen 4s forwards'});
    document.getElementById('cloud-container').innerHTML += `<button onclick="cloud(Object.entries(data.tfidf).sort((a,b)=>b[1]-a[1]).slice(0, 100 + 1).map(e=>{return{'key': e[0], 'value': e[1]}}))" style="color: white; background-color: #007bff; border-color: #007bff; font-size: 1rem; border-radius: .25rem; position: absolute; top: 75px; left: 50px; width: 200px; height: 30px;">Back to Wordcloud </button>
    <button onclick="website_display('`+e.target.innerHTML+`')" style="color: white; background-color: #007bff; border-color: #007bff; font-size: 1rem; border-radius: .25rem; position: absolute; top: 110px; left: 50px; width: 200px; height: 60px;">Display websites with this word in them</button>`;
    document.getElementById('cloud-container').appendChild(Object.assign(document.createElement('div'), {id: 'chart-occurence-container'}));
    document.getElementById('cloud-container').appendChild(Object.assign(document.createElement('div'), {id: 'chart-frequency-container'}));
    document.getElementById('chart-occurence-container').appendChild(Object.assign(document.createElement('canvas'), {id: 'chart-occurence'}))
    document.getElementById('chart-frequency-container').appendChild(Object.assign(document.createElement('canvas'), {id: 'chart-frequency'}))
    // /[^\-\d]*([\-\d]+),\s?([\-\d]+)[^\-\d]*([\-\d]+)/gm.exec(e.target.getAttribute('transform'))
    window.chartOccurence = new Chart(document.getElementById('chart-occurence').getContext('2d'), {
        type: 'doughnut',
        data: {
            datasets: [{
                data: Object.entries(data.specifics).filter(x=>x[1].data[e.target.innerHTML]).map(x=>x[1].data[e.target.innerHTML]),
                backgroundColor: Array(Object.entries(data.specifics).filter(x=>x[1].data[e.target.innerHTML]).length).fill(undefined).map(x=>'#' + (function co(lor){   return (lor += [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f'][Math.floor(Math.random()*16)]) && (lor.length == 6) ?  lor : co(lor); })(''))
            }],
            labels: Object.entries(data.specifics).filter(x=>x[1].data[e.target.innerHTML]).map(x=>x[1].title)
        },
        options: {
            responsive: false
        }
    });
    window.chartFrequency = new Chart(document.getElementById('chart-frequency').getContext('2d'), {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [data.tfidf[e.target.innerHTML], Object.values(data.tfidf).reduce((p,n)=>p+n)],
                backgroundColor: Array(2).fill(undefined).map(x=>'#' + (function co(lor){   return (lor += [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f'][Math.floor(Math.random()*16)]) && (lor.length == 6) ?  lor : co(lor); })(''))
            }],
            labels: [e.target.innerHTML, 'the rest of the data']
        },
        options: {
            responsive: false
        }
    })
});
    delete window.onresize;
    
   
}

function fetcherror(str){
	// TODO: add UI of error
	alert(str)
}

function website_display(word){
    document.body.innerHTML += `<div id="greyout" onkeydown="if(event.which===27){document.getElementById('greyout').parentNode.removeChild(document.getElementById('greyout'))}" style="position:fixed;
    z-index: 2; /* above everything else */
    top:0; left:0; bottom:0; right:0;
    background:rgba(0,0,0,.5);
"> <div style="background-color: white; border-color: black; margin: auto; border-radius: 1rem; padding: 1rem 1rem 1rem 1rem; text-align: center;" ><u>Websites with this word in them, listed in order of occurence:</u><br>` + 
    Object.entries(data.specifics).filter(e=>e[1].data[word]).sort((a,b)=>b[1].data[word]-a[1].data[word]).map(e=>'<a href="'+e[0]+'">'+e[1].title+'</a>').join('<br>') + 
    `<br><button class="btn" onclick="document.getElementById('greyout').parentNode.removeChild(document.getElementById('greyout'))">Go Back</button></div></div>`
}

let searchtopbar;

function about(){
    document.getElementById('root-container').innerHTML = `THE DATA REFINERY, a project to make information more easily accessible and usable.
    <br>
    Credits: virchau13, junyynyyn, JustATin555<br>
    Version: v1.0.0<br>
    Installation: You're already here!<br>`
    topbar.appendChild(searchtopbar)
}

function search(e){
    if(e.which === 13){
        if(document.getElementById('websites')){
            document.getElementById('websites').parentNode.removeChild(document.getElementById('websites'));
        }
        window.last_searched = e.target.value;
        document.getElementById('root-container').innerHTML = `<div id="searchbar">
        <div id="loader" style="border: 8px solid #f3f3f3; 
        border-top: 8px solid #555;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin-left: 30%;
        animation: spin 2s linear infinite;"></div><br><p> Loading search results... </p>
    </div>
    <div id="cloud-container">	
    </div>`
        // GET data from server for rendering
        fetch("http://127.0.0.1:5000/scrape?querystring=" + e.target.value)
        .then((res) => res.ok ? res.json() : fetcherror('ERROR fetching from 127.0.0.1:5000/?query=' + e.target.value + '. HTTP Response code is ' + res.status))
        .then((data) => { 
            window.data = data; 
            if(document.getElementById('searchbar')){ 
                document.getElementById('root-container').removeChild(document.getElementById('searchbar'))
            }
            console.log(data); 
            cloud(Object.entries(data.tfidf).sort((a,b)=>b[1]-a[1]).slice(0, 100 + 1).map(e=>{return{'key': e[0], 'value': e[1]}}));
        });
    }
}

function descriptionControl(e){
    console.log('hover!')
    document.getElementById('description-box').innerHTML = data.specifics[e.target.getAttribute('href')].description;
}


document.addEventListener("DOMContentLoaded", () => {
    // search bar on top configuration
    searchtopbar = Object.assign(document.createElement('input'), {id: 'searchtopbar'})
    searchtopbar.addEventListener('keypress', search);
    searchtopbar.setAttribute('placeholder', 'Enter search here...');
    // searchbar controls
	let searchbar = document.getElementById("search");
    searchbar.addEventListener("keypress", search)
})

function cloud(tags){

topbar.appendChild(searchtopbar);

if(document.getElementById('related-words-fix')){
    document.getElementById('related-words-fix').parentNode.removeChild(document.getElementById('related-words-fix'));
}

document.getElementById('cloud-container').innerHTML = '';
observer.observe(document.getElementById('cloud-container'), {
    childList: true,
    subtree: true, 
    attributes: false, 
    characterData: false
});
    

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
        .attr("height", h)

var vis = svg.append("g").attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

window.onresize = function(){ update(); }

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

update();
}