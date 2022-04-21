function update(e) {
    let t = document.getElementById("number-" + e),
        n = parseInt(t.value, 10);
    if (((t.value = ""), !isNaN(n))) {
        let t = new XMLHttpRequest();
        t.open("UPDATE", "", !0),
            t.setRequestHeader("Content-Type", "application/json"),
            (t.onreadystatechange = function() {
                if (4 === this.readyState) {
                    let n = JSON.parse(t.responseText);
                    if (200 === t.status) {
                        render("success", n.message);
                        let t = n.status;
                        (document.getElementById("level-" + e).innerText =
                            "Level " + String(t[3])),
                        "True" === t[7] ?
                            (document.getElementById("progress-" + e).innerText =
                                "Completed") :
                            (document.getElementById("progress-" + e).innerText =
                                t[4] + " / " + t[6]);
                    } else render("danger", n.error);
                }
            }),
            t.send(JSON.stringify({ number: String(n), id: e }));
    }
}

function register() {
    let e = document.getElementsByClassName("input"),
        t = new XMLHttpRequest();
    t.open("POST", "/register", !0),
        t.setRequestHeader("Content-Type", "application/json"),
        (t.onreadystatechange = function() {
            if (4 === this.readyState) {
                let e = JSON.parse(t.responseText);
                200 === t.status ?
                    (render("success", e.message), (document.location.href = "/login")) :
                    render("danger", e.error);
            }
        });
    let n = JSON.stringify({
        username: e[0].value,
        password1: e[1].value,
        password2: e[2].value,
    });
    t.send(n);
}

function login() {
    let e = document.getElementsByClassName("input"),
        t = new XMLHttpRequest();
    t.open("POST", "/login", !0),
        t.setRequestHeader("Content-Type", "application/json"),
        (t.onreadystatechange = function() {
            if (4 === this.readyState) {
                let e = JSON.parse(t.responseText);
                200 === t.status ?
                    (render("success", e.message), (document.location.href = "/")) :
                    render("danger", e.error);
            }
        });
    let n = JSON.stringify({ username: e[0].value, password: e[1].value });
    t.send(n);
}
let clear,
    index = 0;

function nextChallenge(e) {
    document
        .getElementById("challenge-" + challenges[index])
        .setAttribute("hidden", ""),
        (index += e),
        document
        .getElementById("challenge-" + challenges[index])
        .removeAttribute("hidden"),
        hideNextChallengeButton();
}

function hideNextChallengeButton() {
    document.getElementById("next").classList.remove("disabled"),
        document.getElementById("previous").classList.remove("disabled"),
        (0 !== challenges.length && index !== challenges.length - 1) ||
        document.getElementById("next").classList.add("disabled"),
        0 === index &&
        document.getElementById("previous").classList.add("disabled");
}

function profile(e) {
    1 === e ?
        (0 !== challenges.length &&
            document
            .getElementById("challenge-" + challenges[index])
            .setAttribute("hidden", ""),
            document.getElementById("next").setAttribute("hidden", ""),
            document.getElementById("previous").setAttribute("hidden", ""),
            document.getElementById("profile").removeAttribute("hidden"),
            document.getElementById("getProfile").setAttribute("hidden", ""),
            document.getElementById("removeProfile").removeAttribute("hidden")) :
        (document.getElementById("profile").setAttribute("hidden", ""),
            0 !== challenges.length &&
            document
            .getElementById("challenge-" + challenges[index])
            .removeAttribute("hidden"),
            document.getElementById("next").removeAttribute("hidden"),
            document.getElementById("previous").removeAttribute("hidden"),
            hideNextChallengeButton(),
            document.getElementById("removeProfile").setAttribute("hidden", ""),
            document.getElementById("getProfile").removeAttribute("hidden"));
}
let msgDuration = 2e3,
    $msg = document.querySelector(".msg");

function render(e, t) {
    switch ((hide(), e)) {
        case "success":
            console.log($msg),
                $msg.classList.add("msg-success", "active"),
                ($msg.innerHTML = t);
            break;
        case "danger":
            $msg.classList.add("msg-danger", "active"), ($msg.innerHTML = t);
            break;
        case "warning":
            $msg.classList.add("msg-warning", "active"), ($msg.innerHTML = t);
            break;
        case "info":
            $msg.classList.add("msg-info", "active"), ($msg.innerHTML = t);
    }
}

function timer() {
    clearTimeout(clear),
        (clear = setTimeout(function() {
            hide();
        }, msgDuration));
}

function hide() {
    $msg.classList.remove("msg-success"),
        $msg.classList.remove("msg-danger"),
        $msg.classList.remove("msg-warning"),
        $msg.classList.remove("msg-info"),
        $msg.classList.remove("active");
}
$msg.addEventListener("transitionend", timer);