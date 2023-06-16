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

//Graphen
const tag = document.getElementById('graph-fuer-tag');
Chart.defaults.font.size = 18;
new Chart(tag, {
    type: 'line',
    data: {
        labels: ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [{
            borderColor: 'rgba(255, 215, 230, 1)',
            backgroundColor: 'rgba(255, 215, 230, 1)',
            data: [35, 39, 42, 48, 53, 50, 57, 60, 58, 55],
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
                min: 40,
                max: 90,
                position: 'right',
                title: {
                    display: true,
                    text: 'Dezibel',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
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
                    text: 'Uhrzeit',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
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
const day = document.getElementById('graph-for-today');
Chart.defaults.font.size = 18;
new Chart(day, {
    type: 'line',
    data: {
        labels: ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [{
            borderColor: 'rgba(255, 215, 230, 1)',
            backgroundColor: 'rgba(255, 215, 230, 1)',
            data: [35, 39, 42, 48, 53, 50, 57, 60, 58, 55],
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
                min: 40,
                max: 90,
                position: 'right',
                title: {
                    display: true,
                    text: 'Decibel',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
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
                    text: 'Time',
                    font: {
                        family: "'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif",
                        size: 20
                    }
                },
                ticks: {
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

    // Aktiviere oder deaktiviere das zweite Dropdown-Menü basierend auf der Auswahl im ersten Dropdown
    secondDropdown.disabled = firstDropdown.value === '';
}

//STOCKWERK UND BEREICH SICHTBAR MACHEN
function checkSelectionDay() {
    const firstDropdown = document.getElementById('firstDropdown');
    const secondDropdown = document.getElementById('secondDropdown');
    const day = document.getElementsByClassName('today-week-month-display');

    if (firstDropdown.value !== '' && secondDropdown.value !== '') {
        for (let i = 0; i < day.length; i++) {
            day[i].style.display = 'flex';
        }
    } else {
        for (let i = 0; i < day.length; i++) {
            day[i].style.display = 'none';
        }
    }
}

// Code zur Vorbelegung der Dropdown-Menüs basierend auf den URL-Parametern
window.addEventListener('DOMContentLoaded', (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    const stockwerk = urlParams.get('stockwerk');
    const bereich = urlParams.get('bereich');

    if (stockwerk && bereich) {
        const firstDropdown = document.getElementById('firstDropdown');
        const secondDropdown = document.getElementById('secondDropdown');

        // Wähle die entsprechenden Optionen in den Dropdown-Menüs aus
        firstDropdown.value = stockwerk;
        updateSecondDropdown(); // Aktualisiere das zweite Dropdown-Menü basierend auf dem ausgewählten Stockwerk
        secondDropdown.value = bereich;
        secondDropdown.disabled = false; // Aktiviere das zweite Dropdown-Menü
    }

    checkSelectionDay();
});

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