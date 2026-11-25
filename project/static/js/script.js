async function displayConcreteIterations() {
    try {
        let res = await fetch("/pastUploads");
        let files = await res.json()
        console.log(files)
        files.forEach((filename, i) => {
            placeConcreteIterations(filename, i)
        });
        placeNewConcreteIteration(files[-1]); // not reading... change this to fetch a copy?

    } catch (err) {
        console.log(err)
    }
}

function placeConcreteIterations(filename, i) {
    const url = `/static/uploads/${filename}`;
    // display previous files on timeline
    const img = document.createElement("img")
    img.src = url;
    document.body.appendChild(img)
    console.log("here")
};

function placeNewConcreteIteration(filename) {
    const url = `/static/uploads/${filename}`; // change this for location of most recent, or name of most recent
    // display most recent file on homepage
    const recent = document.createElement("recent")
    recent.src = url;
    document.body.appendChild(recent)
    console.log("here")
    console.log(filename)
};

window.onload = function () {
    console.log("js is up and running");
    displayConcreteIterations();
}

// send an event to flask; flask adds one to this visitor's session counter
async function log(event) {
    await fetch("/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event: event }),
        keepalive: true
    });
}

// count clicks
addEventListener("click", () => log("clicks"));

// count tab leaves
document.addEventListener("visibilitychange", () => {
    if (document.hidden) log("tab_leaves");
});

// Refresh the visitor's location and network details on every page load.
async () => {
    const d = await (await fetch("https://ipwho.is/")).json();
    await fetch("/location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            city: d.city,
            region: d.region,
            org: d.connection?.org
        })
    });
};