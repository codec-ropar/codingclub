var url = 'https://docs.google.com/spreadsheets/d/1KbvLXThlUEhoPrzYyD8gmLIi974UsBTv7tC-KwKdQOo/export?format=tsv&gid=834916002';
document.getElementById('loading').style.display = 'flex';

async function getGoogleSheetData(url) {
    let data = await fetch(url)
        .then(response => response.text())
        .then(data => {
            let result = [];
            let rows = data.split('\n');

            for (let i = 0; i < rows.length; i++) {
                if (rows[i].trim() == '') continue;
                let cell = rows[i].split('\t');
                for (let j = 0; j < cell.length; j++) {
                    cell[j] = cell[j].trim();
                }
                result.push(cell);
            }
            return result;
        });
    return data;
}

async function main() {
    let data = await getGoogleSheetData(url);
    document.getElementById('loading').style.display = 'none';
    const contentElement = document.getElementById('content');
    contentElement.style.display = 'flex';
    contentElement.style.flexDirection = 'column';

    if (data.length > 0) {
        for (let i = 1; i < data.length; i++) {
            if (data[i][0] == '-') {
                all_event = document.createElement('div');
                all_event.className = 'all_event';
                all_event.innerHTML = `
                <div class="heading glow-text" style="color:white;">
                <h1>${data[i][1]}</h1>
                </div>`;
                i++;

                events = document.createElement('div');
                events.className = 'events';
                while (i < data.length) {
                    if (data[i][0] == '-') break;
                    if (data[i][0] == '') {
                        i++;
                        continue;
                    }
                    events_block = document.createElement('div');
                    events_block.innerHTML = `
                    <div class="event-image">
                        <img src="https://raw.githubusercontent.com/codec-ropar/codingclub/main/static/images/events/${data[i][5]}">
                    </div>
                    <div class="event-details">
                        <h2>${data[i][0]}</h2>
                        <p style="font-size=0.9rem;">${data[i][1]}</p>
                        <br>
                        <p><strong>${data[0][2]}:</strong> <span class="regular-text">${data[i][2]}</span></p>
                        <br>
                        <p><strong>${data[0][3]}:</strong> <span class="regular-text">${data[i][3]}</span></p>
                        <br>
                        <p><strong>${data[0][4]}:</strong> <span class="regular-text">${data[i][4]}</span></p>                                                          
                    </div>
                    `;
                    events_block.className = 'event-block';
                    events.appendChild(events_block);
                    i++;
                }
                all_event.appendChild(events);
                const verticalSpace = document.createElement("div");
                verticalSpace.style.width = "100vw";
                verticalSpace.style.height = "60px";
                all_event.appendChild(verticalSpace);

                content = document.querySelector('#main > content');
                content.appendChild(all_event);
                i--;
            }
        }
    } else {
        contentElement.innerHTML = '<div class="no-data-message"><img class="no-data-logo" src="static/images/no-data.png" alt="OOPs"><p>No data found</p></div>';
    }
}

main();
