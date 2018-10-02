/*
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
 */
function get(url) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function () {
        if (http.readyState == 4) {
            var data = JSON.parse(http.responseText);
            var elm, tm;

            if ('elements' in data) {
                for (var id in data['elements']) {
                    if (!data['elements'].hasOwnProperty(id)) continue;
                    var text = data['elements'][id];
                    elm = document.getElementById(id);
                    if (elm) {
                        if (elm.tagName.toLowerCase() == "input") {
                            elm.value = text;
                        } else {
                            elm.innerText = text;
                        }
                    }
                }
            }

            elm = document.getElementById("message-success");
            if (elm) {
                clearTimeout(parseInt(elm.getAttribute("data-tm")));
                elm.remove();
            }
            if ('message' in data) {
                elm = document.createElement("h3");
                elm.id = "message-success";
                elm.className = "alert";
                elm.style.color = "#37BC9B";
                elm.innerText = data['message'];
                tm = setTimeout(function () {
                    document.getElementById("message-success").remove();
                }, 15 * 1000);
                elm.setAttribute("data-tm", tm);
                document.body.insertBefore(elm, document.body.children[1]);
            }

            elm = document.getElementById("message-error");
            if (elm) {
                clearTimeout(parseInt(elm.getAttribute("data-tm")));
                elm.remove();
            }
            if ('error' in data) {
                elm = document.createElement("h3");
                elm.id = "message-error";
                elm.className = "alert";
                elm.style.color = "#DA4453";
                elm.innerText = data['error'];
                tm = setTimeout(function () {
                    document.getElementById("message-error").remove();
                }, 15 * 1000);
                elm.setAttribute("data-tm", tm);
                document.body.insertBefore(elm, document.body.children[1]);
            }
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
            console.log(elm.getAttribute("data-no-reload"));
            if (elm.getAttribute("data-no-reload") !== null) get(elm.getAttribute("href"));
            else window.location = elm.getAttribute("href");
            return false
        }, true);
    });
})();