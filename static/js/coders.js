function getRatingsColorClass(ratings) {
  if (ratings < 1200) return "newbie";
  if (ratings < 1400) return "pupil";
  if (ratings < 1600) return "specialist";
  if (ratings < 1900) return "expert";
  if (ratings < 2100) return "candidate-master";
  if (ratings < 2300) return "master";
  if (ratings < 2400) return "international-master";
  return "grandmaster";
}

function createBox(rank, name, handle, ratings, score) {
  if (ratings === -1 && score === -1) {
    let noDataDiv = document.createElement("div");
    noDataDiv.classList.add("no-data-message");
    let img = document.createElement("img");
    img.classList.add("no-data-logo");
    img.setAttribute("src", "static/images/no-data.png");
    img.setAttribute("alt", "OOPs");
    noDataDiv.appendChild(img);
    noDataDiv.innerHTML += `<p>No data found</p>`;
    return noDataDiv;
  } else {
    let box = document.createElement("div");
    box.classList.add("box");

    box.addEventListener("click", () => {
      window.open(`https://codeforces.com/profile/${handle}`, "_blank");
    });

    let rankDiv = document.createElement("div");
    rankDiv.classList.add("rank");

    if (rank == 1) {
      box.classList.add("first", "extra");
      let img = document.createElement("img");
      img.setAttribute("src", "/static/images/gold-medal.png");
      img.setAttribute("alt", "1st");
      rankDiv.appendChild(img);
    } else if (rank == 2) {
      box.classList.add("second", "extra");
      let img = document.createElement("img");
      img.setAttribute("src", "/static/images/silver-medal.png");
      img.setAttribute("alt", "2nd");
      rankDiv.appendChild(img);
    } else if (rank == 3) {
      box.classList.add("third", "extra");
      let img = document.createElement("img");
      img.setAttribute("src", "/static/images/bronze-medal.png");
      img.setAttribute("alt", "3rd");
      rankDiv.appendChild(img);
    } else {
      let rankText = document.createElement("p");
      rankText.innerText = rank;
      rankDiv.appendChild(rankText);
    }
    box.appendChild(rankDiv);

    let color = getRatingsColorClass(ratings);
    box.innerHTML += `<div class="name"><p class="${color}">${name}</p></div>
        <div class="handle"><a class="${color}" href="https://codeforces.com/profile/${handle}">${handle}</a></div>
        <div class="score"><p>${score}%ile</p></div>`;

    return box;
  }
}

let tabHeader = document.getElementsByClassName("tab-header")[0];
let tabIndicator = document.getElementsByClassName("tab-indicator")[0];
let ranking = document.getElementsByClassName("rankings")[0];
let rankingPane = ranking.querySelectorAll("div");
let tabsPane = tabHeader.getElementsByTagName("div");

for (let i = 1; i <= 4; i++) {
  let wrapper = document.createElement("div");
  wrapper.classList.add("wrapper");
  let year = i.toString();
  let coderList = data[year];
  if (coderList.length === 0) {
    let box = createBox(1, "", "", -1, -1);
    wrapper.appendChild(box);
  } else {
    for (let j = 0; j < Math.min(coderList.length, 50); j++) {
      let box = createBox(j + 1, coderList[j].name, coderList[j].handle, coderList[j].ratings, coderList[j].score);
      wrapper.appendChild(box);
    }
  }
  rankingPane[i - 1].appendChild(wrapper);
}

for (let i = 0; i < tabsPane.length; i++) {
  tabsPane[i].addEventListener("click", () => {
    tabHeader.getElementsByClassName("active")[0].classList.remove("active");
    tabsPane[i].classList.add("active");
    ranking.getElementsByClassName("active")[0].classList.remove("active");
    rankingPane[i].classList.add("active");
    tabIndicator.style.left = `calc(calc(100%/4)*${i})`;
  });
}
