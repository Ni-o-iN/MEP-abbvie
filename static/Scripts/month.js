//GRAPHEN
const monat = document.getElementById('graph-fuer-monat');
Chart.defaults.font.size = 18;
new Chart(monat, {
    type: 'line',
    data: {
        labels: ['01.', '05.', '10.', '15.', '20.', '25.', '30.'],
        datasets: [{
            borderColor: 'rgba(253, 151, 64, 1)',
            data: [65, 63, 68, 61, 72, 75, 66, 68, 60, 73],
            tension: 0.3
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
                position: 'right',
                title: {
                    display: true,
                    text: 'Dezibel'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Tag'
                }
            }
        }
    }
});
const month = document.getElementById('graph-for-month');
Chart.defaults.font.size = 18;
new Chart(month, {
    type: 'line',
    data: {
        labels: ['01.', '05.', '10.', '15.', '20.', '25.', '30.'],
        datasets: [{
            borderColor: 'rgba(253, 151, 64, 1)',
            data: [65, 63, 68, 61, 72, 75, 66, 68, 60, 73],
            tension: 0.3
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
                position: 'right',
                title: {
                    display: true,
                    text: 'Decibel'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Day'
                }
            }
        }
    }
});

//DROP DOWN MENÜS
function updateSecondDropdown() {
    const firstDropdown = document.getElementById('firstDropdown');
    const secondDropdown = document.getElementById('secondDropdown');

    // Optionen im zweiten Dropdown-Menü basierend auf Auswahl im ersten Dropdown aktualisieren
    if (firstDropdown.value === 'floor1') {
        secondDropdown.innerHTML = `
        <option value="" disabled selected hidden></option>
        <option value="A">A</option>
        <option value="B">B</option>
        <option value="C">C</option>
      `;
    } else if (firstDropdown.value === 'floor2') {
        secondDropdown.innerHTML = `
        <option value="" disabled selected hidden></option>
        <option value="D">D</option>
        <option value="E">E</option>
        <option value="F">F</option>
        <option value="G">G</option>
        <option value="H">H</option>
      `;
    }
    // Aktiviere das zweite Dropdown-Menü, falls eine Option ausgewählt wurde
    secondDropdown.disabled = firstDropdown.value === '';
}

//STOCKWERK UND BEREICH SICHTBAR MACHEN
function checkSelectionMonth() {
    const firstDropdown = document.getElementById('month_selection');
    const secondDropdown = document.getElementById('secondDropdown');
    const month = document.getElementsByClassName('today-week-month-display');


    if (firstDropdown.value !== '' && secondDropdown.value !== '') {
        for (let i = 0; i < month.length; i++) {
            console.log('Geht ins Console.log')
            month[i].style.display = 'flex';
        }
    } else {
        for (let i = 0; i < month.length; i++) {
            month[i].style.display = 'none';
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
  
  window.addEventListener('resize', function() {
    const menu = document.querySelector('.menu');
    if (window.innerWidth > 700) {
      menu.classList.remove('open');
    }
  });