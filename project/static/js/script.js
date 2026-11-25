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
