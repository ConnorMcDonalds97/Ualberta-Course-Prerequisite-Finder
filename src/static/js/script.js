let course = ""

function encodeJSONData(course)
{
    // JSON Encode the data
    data = {name: course}

    console.log(data)

    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            data
        })
        .catch(error => console.error('Error:', error));
}

function changeGraph() {
    const myDiagram = go.Diagram.fromDiv('myDiagramDiv');
    fetch('../static/js/JSON/diagramData.json')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      console.log(data[0][0]["key"]);
      if (data[0][0]["key"] == "I") {
        console.log("SAME");
        data[0] = [{key:"Invalid Course ID", level: 0}]
      }
      myDiagram.model = new go.GraphLinksModel(
        data[0], data[1]
      );
    })
    .catch(error => console.error('Error loading file:', error));
  }

function loadingGraph() {
  const myDiagram = go.Diagram.fromDiv('myDiagramDiv');
  myDiagram.model = new go.GraphLinksModel([{key:"Loading", level:0, catalog:""},{key:"dot.", level:1, catalog:""},{key:"dot..", level:2, catalog:""},{key:"dot...", level:3, catalog:""}], [{from:"Loading", to:"dot."}, {from:"dot.", to:"dot.."}, {from:"dot..", to:"dot..."}]);
}


function sendData(course) {
    console.log(course);
    loadingGraph();
    fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: course })  // Send the message as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.reply);
        changeGraph();
    })
    .catch(error => console.error('Error:', error));
}

const body = document.querySelector("body");
body.setAttribute("style", "width: 100%; height: 100%;display: flex; flex-direction: column; align-items: center; justify-content: flex-start; margin: 0; padding: 0; overflow-y:auto; overflow-x:hidden;");


///
/// Banner
///
const banner = document.createElement("div");
banner.setAttribute("class", "banner main-header")

banner.textContent = "Course Prerequisite Finder"
body.appendChild(banner);

const inputs = document.createElement("div")
inputs.setAttribute("style", "display: flex; align-items: center")

const userInput = document.createElement("input")
userInput.setAttribute("style","margin:16px; height: 32px; width: 200px;")
userInput.setAttribute("id", "userInput")
userInput.setAttribute("type","text")
userInput.setAttribute("placeholder", "Example: 'CMPUT 101'")
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        course = document.getElementById("userInput").value
        console.log(course)

        sendData(course)
    }
  });

const button = document.createElement("button")
button.setAttribute("style", "width: 64px; height: 32px; color: white")
button.setAttribute("class", "box-div theme-color")
button.setAttribute("id", "submit")
button.addEventListener("click", function(){
    course = document.getElementById("userInput").value
    console.log(course)

    sendData(course)
})
button.textContent = "Submit"


const secondRowAll = document.createElement("div")
secondRowAll.setAttribute("style", "width: 100%")

const secondRow = document.createElement("div")
secondRow.setAttribute("style", "display: flex; justify-content: center; align-items: center")

const legend = document.createElement("div")
legend.setAttribute("class", "theme-color legend")
legend.setAttribute("style", `
  position: relative;
  white-space: pre-wrap;
  height: 50%;
  width: 50%;
  display: flex;
  flex-direction: column;
  margin: 4px 16px 0 16px;
  font-size: 100%;
  word-wrap: break-word;
  line-height:1.5;
`);
legend.innerHTML = 'TIPS:\n1. Classes connected with the same colour line are equivalent. You can do either one.\n2. Use the level selector to make it easier to view the prerequisites.\n3. You can pinch to zoom in and out on the map on mobile!\nPlease fill out our google form below and tell us how we can do better! <a id="googleform" href="https://docs.google.com/forms/d/e/1FAIpQLScO6nL14NhmvNW-diiLTFdZJnFgiDLey2pYIyfZPHmTrB7DxQ/viewform" rel="noopener noreferrer" target="_blank">Google Form</a>'

secondRow.appendChild(userInput)
secondRow.appendChild(button)
secondRowAll.appendChild(secondRow)

body.appendChild(secondRowAll)

  // Container for theme and levels
  const container = document.createElement("div");
  container.setAttribute(
      "style",
      "display: flex; flex-direction: row; gap: 20px; margin: 0 16px 0 16px;"
  );

  // Theme selector
  const themeDiv = document.createElement("div");
  themeDiv.setAttribute("class", "box-div theme-color");
  themeDiv.setAttribute("style", "margin-bottom: 20px;");

  const themeLabel = document.createElement("p");
  themeLabel.setAttribute("class", "select");
  themeLabel.textContent = "Theme: ";
  themeDiv.appendChild(themeLabel);

  const themeSelect = document.createElement("select");
  themeSelect.setAttribute("class", "select-box");
  themeSelect.setAttribute("id", "theme");
  themeSelect.setAttribute("onchange", "changeTheme(), changeMainTheme()");

  const themeOptions = [
      { value: "base", text: "Base", selected: true },
      { value: "pretty", text: "Pretty", selected: false },
  ];
  themeOptions.forEach((optionData) => {
      const option = document.createElement("option");
      option.value = optionData.value;
      option.textContent = optionData.text;
      if (optionData.selected) option.setAttribute("selected", "");
      themeSelect.appendChild(option);
  });

  themeDiv.appendChild(themeSelect);

  // Levels selector
  const levelsDiv = document.createElement("div");
  levelsDiv.setAttribute("class", "box-div theme-color");
  levelsDiv.setAttribute("style", "margin-bottom: 20px;");

  const levelsLabel = document.createElement("p");
  levelsLabel.setAttribute("class", "select");
  levelsLabel.textContent = "Visible Levels: ";
  levelsDiv.appendChild(levelsLabel);

  const levelsSelect = document.createElement("select");
  levelsSelect.setAttribute("class", "select-box");
  levelsSelect.setAttribute("id", "level-chooser");
  levelsSelect.setAttribute("onchange", "changeLevelView()");

  const levelOptions = [
      { value: "1", text: "Level 1" },
      { value: "2", text: "Level 2" },
      { value: "3", text: "Level 3" },
      { value: "4", text: "Level 4" },
      { value: "100", text: "All Levels", selected: true },
  ];
  levelOptions.forEach((optionData) => {
      const option = document.createElement("option");
      option.value = optionData.value;
      option.textContent = optionData.text;
      if (optionData.selected) option.setAttribute("selected", "");
      levelsSelect.appendChild(option);
  });

  levelsDiv.appendChild(levelsSelect);

  // Append both divs to the container
  container.appendChild(themeDiv);
  container.appendChild(levelsDiv);

  // Append the container to the body
  body.insertBefore(container, document.getElementById("myDiagramDiv"));
;

body.appendChild(legend)

//theme build
theme_colors = {
  "base":"#285D39",
  "pretty":"#DD70A9"
}

//make variable theme
function changeMainTheme() {
  banner.style.backgroundColor = theme_colors[document.getElementById('theme').value];

  // box-div elements
  const elements = document.querySelectorAll(".theme-color");

  elements.forEach(element => {
      element.style.backgroundColor = theme_colors[document.getElementById('theme').value];;
  });
}
// Create the myDiagramDiv element
const myDiagramDiv = document.createElement("div");
myDiagramDiv.setAttribute("id", "myDiagramDiv");
myDiagramDiv.setAttribute(
  "style",
  "width: 95%; height: 600px; background-color: #DAE4E4; border-radius: 20px; border-style: solid; border-color: #285D39"
);

// Append the myDiagramDiv element to the body
body.appendChild(myDiagramDiv);

////////////////////////////////////////////////
// FOOTER     //////////////////////////////////
////////////////////////////////////////////////

const footer = document.createElement("div")
footer.setAttribute("id", "footer")
footer.setAttribute("style", "padding: 16px; margin: 16px 16px 0px 16px; width: 100%; background-color: #285D39; color: white; font-size: 16px; font-family: Verdana; display: flex; flex-direction: column; align-items: center; justify-content: center;")
footer.setAttribute("class", "box-div theme-color")

// Information
const about = document.createElement("div")
about.setAttribute("style", "display: flex; flex-direction: column; align-items: center")

const aboutTitle = document.createElement("h1")
aboutTitle.setAttribute("class", "main-header")
aboutTitle.setAttribute("style", "font-size: 36px")
aboutTitle.textContent = "About"
about.appendChild(aboutTitle);

const aboutInformation = document.createElement("p")
aboutInformation.setAttribute("style", "color: white; font-family: Verdana; width: 40%; text-align: center; line-height: 2")
aboutInformation.setAttribute("class", "basic-link")
aboutInformation.innerHTML = `
This project <strong>WON</strong> the <a href="https://hackedbeta2024.devpost.com" target="_blank">HackED Beta</a> 24-hour hackathon hosted by the Computer Engineering Club of the University of Alberta.
The inspiration was to create a clean looking flow diagram that displayed course requirements to save time when deciding which courses to take.
The project files can be viewed on <a href="https://github.com/ConnorMcDonalds97/Ualberta-Course-Prerequisite-Finder/tree/main" target="_blank">Github</a>,
and the project portfolio can be viewed on <a href="https://devpost.com/software/ualberta-course-prereq-helper?ref_content=my-projects-tab&ref_feature=my_projects" target="_blank">DevPost</a>.
Have fun looking at the monstrous courses or take some time
to look into some of the courses you are interested in to see how to achieve your desired schedule. (Note that UofA catalog sometimes makes prerequisites general
and without any specific courses so make sure to click on View Catalog to verify the courses you will need) :D
`
about.appendChild(aboutInformation)


footer.appendChild(about);


// Plug

const plugMessage = document.createElement("div")
plugMessage.setAttribute("style", "margin-top: 40px; color: white; font-family: Verdana; text-decoration: underline")
plugMessage.textContent = "Check out our github profiles by clicking our names below!"
footer.appendChild(plugMessage)

// MEMBER LIST
const members = document.createElement("div");
members.setAttribute("style", "width: 100%; margin-bottom: 20px; display:flex; gap: 30px; justify-content:center; align-items: center");

// Member data array
const memberData = [
  { name: "Ben Bui", url: "https://github.com/maggiSauce" },
  { name: "Olivia Cai", url: "https://github.com/olivecai" },
  { name: "Kevin Cao", url: "https://github.com/ConnorMcDonalds97" },
  { name: "James Cote", url: "https://github.com/James-Cote" },
  { name: "Vinson Lou", url: "https://github.com/Enagarii" }
];

// Loop through member data and create elements
memberData.forEach(member => {
  const anchor = document.createElement("a");
  anchor.setAttribute("class", "github-link");
  anchor.setAttribute("href", member.url);
  anchor.setAttribute("style", "cursor: pointer;");
  anchor.setAttribute("target", "_blank");
  anchor.setAttribute("rel", "noopener noreferrer");
  anchor.textContent = member.name;

  members.appendChild(anchor);
});

// Append the member list to the document
document.body.appendChild(members);

footer.appendChild(members)

body.appendChild(footer)