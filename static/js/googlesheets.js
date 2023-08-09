var url = 'https://docs.google.com/spreadsheets/d/1KbvLXThlUEhoPrzYyD8gmLIi974UsBTv7tC-KwKdQOo/export?format=tsv&gid=0'

async function getGoogleSheetData(url) {
    let data = await fetch(url)
        .then(response => response.text())
        .then(data => {
            let rows = data.split('\n');
            let result = [];
            for (let i = 1; i < rows.length; i++) {
                // Skip empty lines
                if (!rows[i].trim()) {
                    continue;
                }

                // Checking whether the current row is a separator or not
                // The first cell must be a hyphen if it is a separator
                let cells = rows[i].split('\t');
                if (cells[0].trim() == '-') {
                    result.push([cells[1].trim()]);
                    continue;
                }

                result[result.length - 1].push({
                    name: cells[0].trim(),
                    position: cells[1].trim(),
                    batch: cells[2].trim(),
                    image: cells[3].trim(),
                    handle: cells[4].trim(),
                    cf_title: cells[5].trim(),
                    linkedin: cells[6].trim(),
                    github: cells[7].trim(),
                });
            }
            return result;
        });
    return data;
}

function createTeamCard(userData) {
    let name = userData.name, position = userData.position, batch = userData.batch, image = userData.image, handle = userData.handle, cf_title = userData.cf_title, linkedin = userData.linkedin, github = userData.github;
    let card = document.createElement("div");
    card.classList.add("card");
    card.classList.add("rgb");
    card.innerHTML = `
    <div class="card-image" style="background: linear-gradient(#fff0 0%, #fff0 70%, #1d1d1d 100%),url('https://raw.githubusercontent.com/codec-ropar/codingclub/main/static/images/profile/${image}'), black; background-position: top; background-size:cover;"></div>
    <div class="card-text">
        <div class="fullname-text">${name}</div>
        <p>${position}</p>
        <div class="social-media">
            <a href="https://codeforces.com/profile/${handle}" class="date ${cf_title.toLowerCase()}" target="_blank">${handle}</a>
            ${linkedin ? '<a href="' + linkedin + '" class="linkedin fa fa-linkedin zoom-upon-hover" target="_blank"></a>' : ''}
        </div>
    </div>`;
    return card;
}

function createHeading(text) {
    let heading = document.createElement("div");
    heading.classList.add("heading");
    heading.innerHTML = `<h1>${text}</h1>`;
    return heading;
}
