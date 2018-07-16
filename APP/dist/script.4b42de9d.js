// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

// eslint-disable-next-line no-global-assign
parcelRequire = (function (modules, cache, entry) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  // Override the current require with this new one
  return newRequire;
})({5:[function(require,module,exports) {
function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
        if (!mutation.addedNodes) return;
        for (var i = 0; i < mutation.addedNodes.length; i++) {
            if ([].concat(_toConsumableArray(document.querySelectorAll('text'))).filter(function (e) {
                return e.parentNode.nodeName === 'g';
            }).length === 101) {
                [].concat(_toConsumableArray(document.querySelectorAll('text'))).forEach(function (e) {
                    return e.addEventListener('click', textfly);
                });
            }
        }
    });
});

throw 'this is an error';
function textfly(e) {
    [].concat(_toConsumableArray(document.querySelectorAll('text'))).filter(function (x) {
        return x !== e.target;
    }).forEach(function (e) {
        e.style.animation = 'moveoffscreen 4s forwards';
    });
    document.getElementById('cloud-container').appendChild(Object.assign(document.createElement('canvas'), { id: 'chart-occurence' }));
    document.getElementById('cloud-container').appendChild(Object.assign(document.createElement('canvas'), { id: 'chart-frequency' }));
    document.getElementById('cloud-container').innerHTML += '<button class="btn btn-primary" onclick="cloud(Object.entries(data.tfidf).sort((a,b)=>b[1]-a[1]).slice(0, 100 + 1).map(e=>{return{\'key\': e[0], \'value\': e[1]}}))" style="position: absolute; top: 75px; left: 50px; width: 200px; height: 200px;">Back to Wordcloud </button>';
    e.target.setAttribute('transform', 'translate(0,0)rotate(0)');
    fetch('http://127.0.0.1:5000/relatedWords?querystring=' + last_searched + '&wordSearch=' + e.target.innerHTML).then(function (res) {
        return res.ok ? res.json() : console.error('http error ' + res.status);
    }).then(function (obj) {
        return document.getElementById('websites').innerHTML = '<div id="related-words">' + Array(obj.length).fill(null).map(function (x, i) {
            return '<p>' + obj[i] + '</p>';
        }).join('') + '</div>' + document.getElementById('websites').innerHTML;
    });
    delete window.onresize;
    console.log(e.target);
    window.chartOccurence = new Chart(document.getElementById('chart-occurence').getContext('2d'), {
        type: 'doughnut',
        data: {
            datasets: [{
                data: Object.entries(data.specifics).filter(function (x) {
                    return x[1].data[e.target.innerHTML];
                }).map(function (x) {
                    return x[1].data[e.target.innerHTML];
                }),
                backgroundColor: Array(Object.entries(data.specifics).filter(function (x) {
                    return x[1].data[e.target.innerHTML];
                }).length).fill(undefined).map(function (x) {
                    return '#' + function co(lor) {
                        return (lor += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f'][Math.floor(Math.random() * 16)]) && lor.length == 6 ? lor : co(lor);
                    }('');
                })
            }],
            labels: Object.entries(data.specifics).filter(function (x) {
                return x[1].data[e.target.innerHTML];
            }).map(function (x) {
                return x[1].title;
            })
        },
        options: {
            responsive: false
        }
    });
    window.chartFrequency = new Chart(document.getElementById('chart-frequency').getContext('2d'), {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [data.tfidf[e.target.innerHTML], Object.values(data.tfidf).reduce(function (p, n) {
                    return p + n;
                })],
                backgroundColor: Array(2).fill(undefined).map(function (x) {
                    return '#' + function co(lor) {
                        return (lor += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f'][Math.floor(Math.random() * 16)]) && lor.length == 6 ? lor : co(lor);
                    }('');
                })
            }],
            labels: [e.target.innerHTML, 'the rest of the data']
        },
        options: {
            responsive: false
        }
    });
}

function fetcherror(str) {
    // TODO: add UI of error
    alert(str);
}

var searchtopbar = Object.assign(document.createElement('input'), { id: 'searchtopbar' });
searchtopbar.addEventListener('keypress', search);
searchtopbar.setAttribute('placeholder', 'Enter search here...');

function about() {
    document.getElementById('root-container').innerHTML = 'THE DATA REFINERY, a project to make information more easily accessible and usable.\n    <br>\n    Credits: virchau13, junyynyyn, JustATin555<br>\n    Version: v1.0.0<br>\n    Installation: You\'re already here!<br>';
    topbar.appendChild(searchtopbar);
}

function search(e) {
    if (e.which === 13) {
        window.last_searched = e.target.value;
        if (!document.getElementById('searchbar')) {
            document.getElementById('root-container').innerHTML = '<div id="searchbar">\n        <div id="loader" style="border: 8px solid #f3f3f3; \n        border-top: 8px solid #555;\n        border-radius: 50%;\n        width: 50px;\n        height: 50px;\n        margin-left: 30%;\n        animation: spin 2s linear infinite;"></div><br><p> Loading search results... </p>\n    </div>\n    <div id="cloud-container">\t\n    </div>';
        } else {
            // make loading bar
            document.getElementById('searchbar').innerHTML = '<div id="loader" style="border: 8px solid #f3f3f3; \n        border-top: 8px solid #555;\n        border-radius: 50%;\n        width: 50px;\n        height: 50px;\n        margin-left: 30%;\n        animation: spin 2s linear infinite;"></div><br><p> Loading search results... </p>';
        }
        // GET data from server for rendering
        fetch("http://127.0.0.1:5000/scrape?querystring=" + e.target.value).then(function (res) {
            return res.ok ? res.json() : fetcherror('ERROR fetching from 192.168.1.81:5000/?query=' + e.target.value + '. HTTP Response code is ' + res.status);
        }).then(function (data) {
            topbar.appendChild(searchtopbar);
            window.data = data;
            if (document.getElementById('searchbar')) {
                document.getElementById('root-container').removeChild(document.getElementById('searchbar'));
            }
            console.log(data);
            website_display(data.specifics);
            cloud(Object.entries(data.tfidf).sort(function (a, b) {
                return b[1] - a[1];
            }).slice(0, 100 + 1).map(function (e) {
                return { 'key': e[0], 'value': e[1] };
            }));
        });
    }
}

function descriptionControl(e) {
    document.getElementById('description-box').innerHTML = data.specifics[e.target.getAttribute('href')].description;
}

function website_display(links) {
    document.body.innerHTML += '<div id="websites"></div><div id="description-box"></div>';
    l = [];
    for (var link in links) {
        l.push('<a href="' + link + '">' + links[link].title + '</a>');
    }
    Object.keys(links).reduce(function (prev, next) {
        return next.length > prev.length;
    });
    document.getElementById('websites').innerHTML = l.join('<br>');
    [].concat(_toConsumableArray(document.getElementById('websites').childNodes)).forEach(function (e) {
        return e.addEventListener("mouseover", descriptionControl);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // searchbar controls
    var searchbar = document.getElementById("search");
    searchbar.addEventListener("keypress", search);
});

function cloud(tags) {
    console.log('hey! i ran cloud!');
    if (document.getElementById('related-words')) {
        document.getElementById('related-words').parentNode.removeChild(document.getElementById('related-words'));
    }
    document.getElementById('cloud-container').innerHTML = '';
    observer.observe(document.getElementById('cloud-container'), {
        childList: true,
        subtree: true,
        attributes: false,
        characterData: false
    });

    function update() {
        console.log('update cloud was called');
        layout.font('impact').spiral('archimedean');
        fontSize = d3.scale['sqrt']().range([10, 100]);
        if (tags.length) {
            fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
        }
        layout.stop().words(tags).start();
    }

    var fill = d3.scale.category20b();

    var w = window.innerWidth,
        h = window.innerHeight;

    var max, fontSize;

    var layout = d3.layout.cloud().timeInterval(Infinity).size([w, h]).fontSize(function (d) {
        return fontSize(+d.value);
    }).text(function (d) {
        return d.key;
    }).on("end", draw);

    var svg = d3.select("#cloud-container").append("svg").attr("width", w).attr("height", h);

    var vis = svg.append("g").attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

    window.onresize = function () {
        update();
    };

    function draw(data, bounds) {
        console.log('draw');
        var w = window.innerWidth,
            h = window.innerHeight;
        console.log(w, h);
        svg.attr("width", w).attr("height", h);

        scale = bounds ? Math.min(w / Math.abs(bounds[1].x - w / 2), w / Math.abs(bounds[0].x - w / 2), h / Math.abs(bounds[1].y - h / 2), h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;

        var text = vis.selectAll("text").data(data, function (d) {
            return d.text.toLowerCase();
        });
        text.transition().duration(1000).attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        }).style("font-size", function (d) {
            return d.size + "px";
        });
        text.enter().append("text").attr("text-anchor", "middle").attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        }).style("font-size", function (d) {
            return d.size + "px";
        }).style("opacity", 1e-6).transition().duration(1000).style("opacity", 1);
        text.style("font-family", function (d) {
            return d.font;
        }).style("fill", function (d) {
            return fill(d.text.toLowerCase());
        }).text(function (d) {
            return d.text;
        });

        vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
    }

    update();
}
},{}],15:[function(require,module,exports) {

var OVERLAY_ID = '__parcel__error__overlay__';

var global = (1, eval)('this');
var OldModule = module.bundle.Module;

function Module(moduleName) {
  OldModule.call(this, moduleName);
  this.hot = {
    data: module.bundle.hotData,
    _acceptCallbacks: [],
    _disposeCallbacks: [],
    accept: function (fn) {
      this._acceptCallbacks.push(fn || function () {});
    },
    dispose: function (fn) {
      this._disposeCallbacks.push(fn);
    }
  };

  module.bundle.hotData = null;
}

module.bundle.Module = Module;

var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
  var hostname = '' || location.hostname;
  var protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  var ws = new WebSocket(protocol + '://' + hostname + ':' + '53930' + '/');
  ws.onmessage = function (event) {
    var data = JSON.parse(event.data);

    if (data.type === 'update') {
      data.assets.forEach(function (asset) {
        hmrApply(global.parcelRequire, asset);
      });

      data.assets.forEach(function (asset) {
        if (!asset.isNew) {
          hmrAccept(global.parcelRequire, asset.id);
        }
      });
    }

    if (data.type === 'reload') {
      ws.close();
      ws.onclose = function () {
        location.reload();
      };
    }

    if (data.type === 'error-resolved') {
      console.log('[parcel] ✨ Error resolved');

      removeErrorOverlay();
    }

    if (data.type === 'error') {
      console.error('[parcel] 🚨  ' + data.error.message + '\n' + data.error.stack);

      removeErrorOverlay();

      var overlay = createErrorOverlay(data);
      document.body.appendChild(overlay);
    }
  };
}

function removeErrorOverlay() {
  var overlay = document.getElementById(OVERLAY_ID);
  if (overlay) {
    overlay.remove();
  }
}

function createErrorOverlay(data) {
  var overlay = document.createElement('div');
  overlay.id = OVERLAY_ID;

  // html encode message and stack trace
  var message = document.createElement('div');
  var stackTrace = document.createElement('pre');
  message.innerText = data.error.message;
  stackTrace.innerText = data.error.stack;

  overlay.innerHTML = '<div style="background: black; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; opacity: 0.85; font-family: Menlo, Consolas, monospace; z-index: 9999;">' + '<span style="background: red; padding: 2px 4px; border-radius: 2px;">ERROR</span>' + '<span style="top: 2px; margin-left: 5px; position: relative;">🚨</span>' + '<div style="font-size: 18px; font-weight: bold; margin-top: 20px;">' + message.innerHTML + '</div>' + '<pre>' + stackTrace.innerHTML + '</pre>' + '</div>';

  return overlay;
}

function getParents(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return [];
  }

  var parents = [];
  var k, d, dep;

  for (k in modules) {
    for (d in modules[k][1]) {
      dep = modules[k][1][d];
      if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) {
        parents.push(+k);
      }
    }
  }

  if (bundle.parent) {
    parents = parents.concat(getParents(bundle.parent, id));
  }

  return parents;
}

function hmrApply(bundle, asset) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }

  if (modules[asset.id] || !bundle.parent) {
    var fn = new Function('require', 'module', 'exports', asset.generated.js);
    asset.isNew = !modules[asset.id];
    modules[asset.id] = [fn, asset.deps];
  } else if (bundle.parent) {
    hmrApply(bundle.parent, asset);
  }
}

function hmrAccept(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }

  if (!modules[id] && bundle.parent) {
    return hmrAccept(bundle.parent, id);
  }

  var cached = bundle.cache[id];
  bundle.hotData = {};
  if (cached) {
    cached.hot.data = bundle.hotData;
  }

  if (cached && cached.hot && cached.hot._disposeCallbacks.length) {
    cached.hot._disposeCallbacks.forEach(function (cb) {
      cb(bundle.hotData);
    });
  }

  delete bundle.cache[id];
  bundle(id);

  cached = bundle.cache[id];
  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    cached.hot._acceptCallbacks.forEach(function (cb) {
      cb();
    });
    return true;
  }

  return getParents(global.parcelRequire, id).some(function (id) {
    return hmrAccept(global.parcelRequire, id);
  });
}
},{}]},{},[15,5])
//# sourceMappingURL=/script.4b42de9d.map