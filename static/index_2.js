var days = 0;
var hours = 0;
var minutes = 0;
var second = 0;
var distance = 0;

const mainTable = document.querySelector("#main_table > tbody");

function clearTable() {
    while (mainTable.firstChild) {
      mainTable.removeChild(mainTable.firstChild);
    }
}
function populateTable(json) {

  Object.keys(json).forEach(key => {
    const tr = document.createElement("tr");

    var td = document.createElement("td");

    tr.innerHTML = '<td>' + key + '</td>' +
            '<td>' + json[key][0]+ '</td>' +
            '<td>' + printtime(json[key][1]) + '</td>';
    
            mainTable.appendChild(tr);

  //console.log(key + ' - ' + json[key]) // key - value
  })

  const blank = document.createElement("tr");
  blank.innerHTML = '<td id="blank">' +' '+ '</tb>' + 
                    '<td id="blank">' +' '+ '</tb>' + 
                    '<td id="blank">' +' '+ '</tb>';
  mainTable.appendChild(blank);
}

              
// calculate hours mins etc
function calctime() {
    days = Math.floor(distance / (1000 * 60 * 60 * 24));
    hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    seconds = Math.floor((distance % (1000 * 60)) / 1000);
}
    
// print time on screen
function printtime(refTime) {
    distance = new Date(refTime).getTime()  - new Date().getTime();
    calctime();

    output = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    // If the count down is over, write some text 
    if (distance < 0) {
        //clearInterval(x);
        output  = "Exam finished!!";
    }
    return output;
}