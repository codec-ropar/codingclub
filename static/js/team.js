document.getElementById('loading').style.display = 'flex';

async function populateTeam() {
    let dataArray = await getGoogleSheetData(url);

    try {
        if (dataArray.length > 0) {
            document.getElementById('loading').style.display = 'none';
            const contentElement = document.getElementById('content');
            contentElement.style.display = 'flex';

            for (let i = 0; i < dataArray.length; i++) {
                data = dataArray[i]; // dataArray[0] is the current team
                document.querySelector("#main > content").appendChild(createHeading(data[0]));

                if (data.length > 0) {
                    for (let j = 1; j < data.length; j++) {
                        document.querySelector("#main > content").appendChild(createTeamCard(data[j]));
                    }

                    VanillaTilt.init(document.querySelectorAll(".card"), {
                        max: 25,
                        speed: 400,
                        glare: true,
                        "max-glare": 0.5,
                    });

                    const verticalSpace = document.createElement("div");
                    verticalSpace.style.width = "100vw";
                    verticalSpace.style.height = "60px";
                    document.querySelector("#main > content").appendChild(verticalSpace);
                }
            }
        } else {
            contentElement.innerHTML = '<div class="no-data-message"><img class="no-data-logo" src="static/images/no-data.png" alt="OOPs"><p>No data found</p></div>';
        }
    } catch (e) {
        console.error('Error fetching data:', error);
        document.getElementById('loading').style.display = 'none';
    }
}

populateTeam();
