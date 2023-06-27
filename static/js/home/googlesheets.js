var url = 'https://docs.google.com/spreadsheets/d/1KbvLXThlUEhoPrzYyD8gmLIi974UsBTv7tC-KwKdQOo/export?format=tsv&gid=0'

async function getGoogleSheetData(url) {
    let data = await fetch(url)
        .then(response => response.text())
        .then(data => {
            let rows = data.split('\n');
            let result = [];
            for (let i = 1; i < rows.length; i++) {
                if (!rows[i].trim()) continue; // skip empty lines
                let cells = rows[i].split('\t');
                // Checking if the row is a separator or not
                // If it is a separator, then the first cell must be hyphen
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
    // console.log(data);
    return data;
}

// getGoogleSheetData(url);



function createTeamCard(name, position, batch, image, handle, cf_title, linkedin, github) {
    let card = document.createElement("div");
    card.classList.add("card");
    card.classList.add("rgb");
    card.innerHTML = `
    <div class="card-image" style="background: linear-gradient(#fff0 0%, #fff0 70%, #1d1d1d 100%),url('https://user-images.githubusercontent.com/69471106/233761893-8b1a29ef-3c3f-4e03-9d14-a4871d840fbe.png');"></div>
    <div class="card-text">
        <div class="fullname-text">Anant Prakash Singh</div>
        <p>Representative</p>
        <div class="social-media">
            <a href="#" class="fa fa-github-square github zoom-upon-hover" id="github"></a>
            <span class="date">Pupil</span>
            <a href="#" class="fa fa-linkedin zoom-upon-hover" id="linkedin"></a>
        </div>
    </div>`;

    return card;
}