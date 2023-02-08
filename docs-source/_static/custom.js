console.log("custom.js loaded");

function addNotebookLinks() {
    const gitRoot = "https://github.com/adelphi-ed-tech/nycschools/blob/main/docs-source";
    const colabRoot = "https://colab.research.google.com/github/adelphi-ed-tech/nycschools/blob/main/docs-source";
    const gitIcon = "../../_static/github.png";
    const colabIcon = "../../_static/colab.png";

    let path = window.location.pathname;
    let index = path.indexOf("/nb/");
    if (index > -1) {
        path = path.slice(index);
        let github = gitRoot + path;

        let colab = colabRoot + path;
        console.log("github: " + github);
        console.log("colab: " + colab);
        // finds the first h1 element on the page and then inserts an < a > element as the last child
        const makeLink = (href, imgSrc  , alt) => {
            let link = document.createElement("a");
            link.setAttribute("href", href);
            link.title = alt;
            link.style = "padding-left: .25em;"
            let img = new Image();
            img.src = imgSrc    ;
            img.setAttribute("alt", alt);

            link.appendChild(img);
            return link;
        }
        let header = document.querySelector("h1");
        header.appendChild(makeLink(github, gitIcon, "open on github"));
        header.appendChild(makeLink(colab, colabIcon, "open on colab"));

    }
}


window.addEventListener("load", addNotebookLinks);