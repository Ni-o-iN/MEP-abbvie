//Graphen Bereiche
const bgcolors = ['rgba(0, 158, 0, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(255, 0, 0, 0.6)'];
const statusTracker = {
    id: 'statusTracker',
    beforeDatasetsDraw(chart, args, pluginOptions) {
        const { ctx, chartArea: { top, bottom, left, right, width, height }, scales: { x, y } } = chart;
        ctx.save();

        drawLines(30, bgcolors[0]);
        drawLines(50, bgcolors[1]);
        drawLines(55, bgcolors[2]);
        function drawLines(yValue, color) {
            ctx.beginPath();
            ctx.lineWidth = 5;
            ctx.strokeStyle = color;
            ctx.moveTo(left, y.getPixelForValue(yValue));
            ctx.lineTo(right, y.getPixelForValue(yValue));
            ctx.stroke();
            ctx.closePath();
            ctx.restore();
        }
    }
}

//GRAPHEN
const woche = document.getElementById('graph-fuer-woche');
Chart.defaults.font.size = 18;
const myChart = new Chart(woche, {
    type: 'line',
    data: {
        labels: ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [{
            label: 'Montag',
            borderColor: 'rgba(255, 215, 230, 1)',
            backgroundColor: 'rgba(255, 215, 230, 1)',
            data: [35, 39, 42, 48, 53, 50, 57, 60, 58, 55],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Dienstag',
            borderColor: 'rgba(125, 0, 224, 1)',
            backgroundColor: 'rgba(125, 0, 224, 1)',
            data: [30, 34, 40, 49, 56, 60, 55, 62, 54, 56],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Mittwoch',
            borderColor: 'rgba(255, 204, 0, 1)',
            backgroundColor: 'rgba(255, 204, 0, 1)',
            data: [33, 36, 48, 60, 53, 50, 57, 50, 54, 51],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Donnerstag',
            borderColor: 'rgba(125, 252, 255, 1)',
            backgroundColor: 'rgba(125, 252, 255, 1)',
            data: [37, 41, 42, 53, 61, 60, 55, 63, 55, 57],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Freitag',
            borderColor: 'rgba(199, 148, 203, 1)',
            backgroundColor: 'rgba(199, 148, 203, 1)',
            data: [34, 36, 40, 53, 55, 48, 50, 54, 48, 41],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                min: 30,
                position: 'right',
                title: {
                    display: true,
                    color: 'black',
                    text: 'Dezibel',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
                    color: 'black',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                grid: {
                    display: false // Raster für y-Achse ausblenden
                }
            },
            x: {
                title: {
                    display: true,
                    color: 'black',
                    text: 'Uhrzeit',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
                    color: 'black',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                grid: {
                    display: false // Raster für y-Achse ausblenden
                }
            }
        }
    },
    plugins: [statusTracker]
});

const week = document.getElementById('graph-for-week');
Chart.defaults.font.size = 18;
const myChartE = new Chart(week, {
    type: 'line',
    data: {
        labels: ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [{
            label: 'Monday',
            borderColor: 'rgba(255, 215, 230, 1)',
            backgroundColor: 'rgba(255, 215, 230, 1)',
            data: [35, 39, 42, 48, 53, 50, 57, 60, 58, 55],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Tuesday',
            borderColor: 'rgba(125, 0, 224, 1)',
            backgroundColor: 'rgba(125, 0, 224, 1)',
            data: [30, 34, 40, 49, 56, 52, 55, 62, 54, 56],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Wednesday',
            borderColor: 'rgba(255, 204, 0, 1)',
            backgroundColor: 'rgba(255, 204, 0, 1)',
            data: [33, 36, 48, 60, 53, 50, 57, 50, 54, 51],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Thursday',
            borderColor: 'rgba(125, 252, 255, 1)',
            backgroundColor: 'rgba(125, 252, 255, 1)',
            data: [37, 41, 42, 53, 61, 60, 55, 63, 55, 57],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        },
        {
            label: 'Friday',
            borderColor: 'rgba(199, 148, 203, 1)',
            backgroundColor: 'rgba(199, 148, 203, 1)',
            data: [34, 36, 40, 53, 55, 48, 50, 54, 48, 41],
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                min: 30,
                position: 'right',
                title: {
                    display: true,
                    color: 'black',
                    text: 'Decibel',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
                    color: 'black',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                grid: {
                    display: false // Raster für y-Achse ausblenden
                }
            },
            x: {
                title: {
                    display: true,
                    color: 'black',
                    text: 'Time',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
                    color: 'black',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                grid: {
                    display: false // Raster für y-Achse ausblenden
                }
            }
        }
    },
    plugins: [statusTracker]
});

const legendColors = ['rgba(255, 215, 230, 1)', 'rgba(125, 0, 224, 1)', 'rgba(255, 204, 0, 1)', 'rgba(125, 252, 255, 1)', 'rgba(199, 148, 203, 1)']
const shortDays = ['Mo', 'Di', 'Mi', 'Do', 'Fr']
const longDays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

//Legt Hintergrundfarbe der Legende dynamisch an
document.getElementById('mo').style.backgroundColor = myChart.data.datasets[0].backgroundColor;
document.getElementById('di').style.backgroundColor = myChart.data.datasets[1].backgroundColor;
document.getElementById('mi').style.backgroundColor = myChart.data.datasets[2].backgroundColor;
document.getElementById('do').style.backgroundColor = myChart.data.datasets[3].backgroundColor;
document.getElementById('fr').style.backgroundColor = myChart.data.datasets[4].backgroundColor;


//Entfernen oder hinzufügen einer Linie bei Deutsch
function toggleData(value, buttonId, day, short) {
    const visibiltyData = myChart.isDatasetVisible(value);
    var textElement = document.getElementById(buttonId + "Text");
    if (visibiltyData === true) {
        myChart.hide(value);
        textElement.classList.add("strikethrough");
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = 'grey';
    }
    else {
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = legendColors[value];
    }
    if (visibiltyData === false) {
        myChart.show(value);
        textElement.classList.remove("strikethrough");
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = legendColors[value];
    }
}


var mondayButton = document.getElementById("button1Text");
var tuesdayButton = document.getElementById("button2Text");
var wednesdayButton = document.getElementById("button3Text");
var thursdayButton = document.getElementById("button4Text");
var fridayButton = document.getElementById("button5Text");

function updateButtonContent() {
  var windowWidth = window.innerWidth;

  if (windowWidth < 1300) {
    mondayButton.textContent = "Mo";
    tuesdayButton.textContent = "Di";
    wednesdayButton.textContent = "Mi";
    thursdayButton.textContent = "Do";
    fridayButton.textContent = "Fr";
  } else {
    mondayButton.textContent = "Montag";
    tuesdayButton.textContent = "Dienstag";
    wednesdayButton.textContent = "Mittwoch";
    thursdayButton.textContent = "Donnerstag";
    fridayButton.textContent = "Freitag";
  }
}

window.addEventListener("resize", updateButtonContent);
updateButtonContent();




//Entfernen oder hinzufügen einer Linie bei Englsich
function toggleDataE(value, buttonId, day) {
    const visibiltyData = myChartE.isDatasetVisible(value);
    var textElement = document.getElementById(buttonId + "Text");
    if (visibiltyData === true) {
        myChartE.hide(value);
        textElement.classList.add("strikethrough");
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = 'grey';
    }
    else {
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = legendColors[value];
    }
    if (visibiltyData === false) {
        myChartE.show(value);
        textElement.classList.remove("strikethrough");
        document.getElementById(day).style.backgroundColor = myChart.data.datasets[value].backgroundColor = legendColors[value];
    }
}


//DROP DOWN MENÜS
function updateSecondDropdown() {
    const firstDropdown = document.getElementById('firstDropdown');
    const secondDropdown = document.getElementById('secondDropdown');

    // Optionen im zweiten Dropdown-Menü basierend auf Auswahl im ersten Dropdown aktualisieren
    if (firstDropdown.value === 'floor1') {
        secondDropdown.innerHTML = `
        <option value="" disabled selected hidden></option>
        <option value="area-a">A</option>
        <option value="area-b">B</option>
        <option value="area-c">C</option>
      `;
    } else if (firstDropdown.value === 'floor2') {
        secondDropdown.innerHTML = `
        <option value="" disabled selected hidden></option>
        <option value="area-d">D</option>
        <option value="area-e">E</option>
        <option value="area-f">F</option>
        <option value="area-g">G</option>
        <option value="area-h">H</option>
      `;
    }
    // Aktiviere das zweite Dropdown-Menü, falls eine Option ausgewählt wurde
    secondDropdown.disabled = firstDropdown.value === '';
}

//STOCKWERK UND BEREICH SICHTBAR MACHEN
function checkSelectionWeek() {
    const firstDropdown = document.getElementById('firstDropdown');
    const secondDropdown = document.getElementById('secondDropdown');
    const week = document.getElementsByClassName('today-week-month-display');

    if (firstDropdown.value !== '' && secondDropdown.value !== '') {
        for (let i = 0; i < week.length; i++) {
            week[i].style.display = 'flex';
        }
    } else {
        for (let i = 0; i < week.length; i++) {
            week[i].style.display = 'none';
        }
    }
}

//FLAGGE
function showOtherFlag() {
    const otherFlag = document.querySelector('.other-language');
    otherFlag.style.display = 'inline';
}
function hideOtherFlag() {
    const otherFlag = document.querySelector('.other-language');
    otherFlag.style.display = 'none';
}

//Info
// Wenn der Info-Button geklickt wird, öffnet sich das Hilfe-Fenster
document.getElementById("infoButton").addEventListener("click", function () {
    document.getElementById("infoModal").style.display = "block";
});

// Wenn das Schließen-Symbol oder der Hintergrund des Info-Fensters geklickt wird, wird es geschlossen
document.getElementsByClassName("close")[0].addEventListener("click", function () {
    document.getElementById("infoModal").style.display = "none";
});

window.onclick = function (event) {
    if (event.target == document.getElementById("infoModal")) {
        document.getElementById("infoModal").style.display = "none";
    }
};

//Hamburger Menü
function toggleMenu() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('open');
}

window.addEventListener('resize', function () {
    const menu = document.querySelector('.menu');
    if (window.innerWidth > 700) {
        menu.classList.remove('open');
    }
});
