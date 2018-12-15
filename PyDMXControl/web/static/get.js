/*
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
 */
function getMessageHandle(idBase, dataBase, data) {
    var elm = document.getElementById("message-" + idBase);
    if (elm) {
        clearTimeout(parseInt(elm.getAttribute("data-tm"), 10));
        elm.remove();
    }
    if (dataBase in data) {
        elm = document.createElement("h3");
        elm.id = "message-" + idBase;
        elm.className = "alert";
        elm.style.color = (idBase === "error" ? "#DA4453" : "#37BC9B");
        elm.innerText = data[dataBase];
        var tm = setTimeout(function () {
            document.getElementById("message-" + idBase).remove();
        }, 15 * 1000);
        elm.setAttribute("data-tm", tm.toString(10));
        document.body.insertBefore(elm, document.body.children[1]);
    }
}

function get(url) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function () {
        if (http.readyState === 4) {
            var data = JSON.parse(http.responseText);
            var elm;

            if ("elements" in data) {
                for (var id in data["elements"]) {
                    if (!data["elements"].hasOwnProperty(id)) {
                        continue;
                    }
                    var text = data["elements"][id];
                    elm = document.getElementById(id);
                    if (!elm) {
                        continue;
                    }
                    if (elm.tagName.toLowerCase() === "input") {
                        elm.value = text;
                    } else {
                        elm.innerText = text;
                    }
                    if ("createEvent" in document) {
                        var evt = document.createEvent("HTMLEvents");
                        evt.initEvent("change", false, true);
                        elm.dispatchEvent(evt);
                    } else {
                        elm.fireEvent("onchange");
                    }
                }
            }

            getMessageHandle("success", "message", data);
            getMessageHandle("error", "error", data);
        }
    };
    http.open("GET", url);
    http.send();
}

(function () {
    var elms = [].slice.call(document.getElementsByTagName("a")); // NodeList to Array
    elms.forEach(function (elm) {
        elm.addEventListener("click", function (e) {
            e.preventDefault();
            if (elm.getAttribute("data-no-reload") !== null) {
                get(elm.getAttribute("href"));
            } else {
                window.location = elm.getAttribute("href");
            }
            return false;
        }, true);
    });
}());