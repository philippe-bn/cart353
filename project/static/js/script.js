async function displayConcreteIterations() {
    try {
        let res = await fetch("/pastUploads");
        let files = await res.json()
        console.log(files)
        files.forEach((filename, i) => {
            placeConcreteIterations(filename, i)
        });

    } catch (err) {
        console.log(err)
    }
}

function placeConcreteIterations(filename, i) {
    const url = `/static/uploads/${filename}`;
    // display most recent file on homepage
    // display previous files on timeline
    const img = document.createElement("img")
    img.src = url;
    document.body.appendChild(img)
    console.log("here")
};

window.onload = function () {
    console.log("js is up and running");
    displayConcreteIterations();
}