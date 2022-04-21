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
let index = 0;

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
            document.getElementById("removeProfile").removeAttribute("hidden"),
            document.getElementById("getNewChallenge").setAttribute("hidden", "")) :
        (document.getElementById("profile").setAttribute("hidden", ""),
            0 !== challenges.length &&
            document
            .getElementById("challenge-" + challenges[index])
            .removeAttribute("hidden"),
            document.getElementById("next").removeAttribute("hidden"),
            document.getElementById("previous").removeAttribute("hidden"),
            hideNextChallengeButton(),
            document.getElementById("removeProfile").setAttribute("hidden", ""),
            document.getElementById("getProfile").removeAttribute("hidden"),
            document.getElementById("getNewChallenge").removeAttribute("hidden"));
}
let clear,
    fileList = [];

function newChallenge(e) {
    1 === e ?
        (0 !== challenges.length &&
            document
            .getElementById("challenge-" + challenges[index])
            .setAttribute("hidden", ""),
            document.getElementById("next").setAttribute("hidden", ""),
            document.getElementById("previous").setAttribute("hidden", ""),
            document.getElementById("new-challenge").removeAttribute("hidden"),
            document.getElementById("getNewChallenge").setAttribute("hidden", ""),
            document.getElementById("removeNewChallenge").removeAttribute("hidden"),
            document.getElementById("getProfile").setAttribute("hidden", "")) :
        (document.getElementById("new-challenge").setAttribute("hidden", ""),
            0 !== challenges.length &&
            document
            .getElementById("challenge-" + challenges[index])
            .removeAttribute("hidden"),
            document.getElementById("next").removeAttribute("hidden"),
            document.getElementById("previous").removeAttribute("hidden"),
            hideNextChallengeButton(),
            document.getElementById("removeNewChallenge").setAttribute("hidden", ""),
            document.getElementById("getNewChallenge").removeAttribute("hidden"),
            document.getElementById("getProfile").removeAttribute("hidden"));
}

function readImage() {
    let e = new XMLHttpRequest();
    e.open("POST", "/challenge", !0),
        e.setRequestHeader("Content-Type", "application/json"),
        (e.onreadystatechange = function() {
            if (4 === this.readyState) {
                let t = JSON.parse(e.responseText);
                200 === e.status ?
                    (render("success", t.message), (document.location.href = "/")) :
                    render("danger", t.error);
            }
        });
    let t = document.getElementsByClassName("newChallengeInput"),
        n = "",
        s = "";
    if (0 !== fileList.length) {
        if ((s = fileList[0]).type && !s.type.startsWith("image/"))
            return void render(
                "danger",
                "This is not one of the following type of image : PNG, JPEG, GIF, BMP"
            );
        n = fileList[0].name;
        const d = new FileReader();
        d.addEventListener("load", (d) => {
                s = d.target.result;
                let i = JSON.stringify({
                    challenge_name: t[0].value,
                    image_name: n,
                    image: s,
                    starting_number: t[2].value,
                    evolution_step: t[3].value,
                });
                e.send(i);
            }),
            d.readAsDataURL(s);
    } else {
        let d = JSON.stringify({
            challenge_name: t[0].value,
            image_name: n,
            image: s,
            starting_number: t[2].value,
            evolution_step: t[3].value,
        });
        e.send(d);
    }
}

function disable(e = !0) {
    let t = document.getElementById("challenge-select").value,
        n = new XMLHttpRequest();
    n.open(null == e ? "DELETE" : "UPDATE", "/challenge", !0),
        n.setRequestHeader("Content-Type", "application/json"),
        (n.onreadystatechange = function() {
            if (4 === this.readyState) {
                let e = JSON.parse(n.responseText);
                200 === n.status ?
                    (render("success", e.message), (document.location.href = "/")) :
                    render("danger", e.error);
            }
        }),
        n.send(JSON.stringify({ id: t, disabled: e }));
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