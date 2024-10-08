// Vragen voor de quiz per pagina
const questionsByPage = [
    // Pagina 1: Design Thinking
    [
        { "action": "Het interviewen van dorpsbewoners om hun waterbehoeften te begrijpen.", "step": "Empathize (Design Thinking)" },
        { "action": "Het definiëren van het probleem: hoe kan een betaalbare en duurzame waterfilter worden ontworpen?", "step": "Define (Design Thinking)" },
        { "action": "Het brainstormen van ideeën voor waterfilters met lokaal beschikbare materialen.", "step": "Ideate (Design Thinking)" },
        { "action": "Het bouwen van verschillende waterfilterprototypes.", "step": "Prototype (Design Thinking)" },
        { "action": "Het testen van de prototypes door dorpsbewoners.", "step": "Test (Design Thinking)" }
    ],
    // Pagina 2: Computational Thinking
    [
        { "action": "Het opdelen van het probleem in verschillende componenten, zoals sedimentverwijdering en bacterie-eliminatie.", "step": "Decompose (Computational Thinking)" },
        { "action": "Het analyseren van bestaande filtersystemen en het herkennen van patronen in de watervervuiling.", "step": "Pattern Recognition (Computational Thinking)" },
        { "action": "Het isoleren van de essentiële kenmerken van een waterfilter en weglaten van irrelevante details.", "step": "Abstraction (Computational Thinking)" },
        { "action": "Het ontwerpen van een algoritme om het filterontwerp aan te passen op basis van verontreinigingen.", "step": "Algorithm Design (Computational Thinking)" }
    ],
    // Pagina 3: Scientific Thinking
    [
        { "action": "Hoe effectief zijn lokaal beschikbare materialen voor waterfiltratie?", "step": "Question (Scientific Thinking)" },
        { "action": "Een waterfilter van lokaal zand en koolstof vermindert verontreinigingen tot een veilig niveau.", "step": "Hypothesis (Scientific Thinking)" },
        { "action": "Experimenten uitvoeren met verschillende waterfilters en waterkwaliteit testen.", "step": "Experiment (Scientific Thinking)" },
        { "action": "Documenteren van de effectiviteit van elk filter.", "step": "Results (Scientific Thinking)" },
        { "action": "Conclusies trekken over welke materialen en ontwerpen het meest effectief zijn.", "step": "Conclusion (Scientific Thinking)" }
    ],
    // Pagina 4: Extra info
    [
        {"info": "Dit is tekst" 
        }],
        [
            {"info": "Dit is tekst2" 
            }]
];


// Functie om de antwoorden te controleren
function checkAnswers() {
    const currentPage = getCurrentPage();
    const currentQuestions = questionsByPage[currentPage - 1];

    let correct = 0;

    currentQuestions.forEach((question, index) => {
        const stepElement = document.querySelector(`#drop${index + 1}`);
        const optionElement = stepElement.querySelector('.draggable'); // Zoek de gesleepte actie

        // Reset de achtergrondkleur van de stap-elementen
        stepElement.classList.remove('bg-green-200', 'bg-red-200');

        if (optionElement && optionElement.innerHTML === question.action) {
            correct++;
            stepElement.classList.add('bg-green-200');  // Markeer correct antwoord groen
        } else {
            stepElement.classList.add('bg-red-200');    // Markeer fout antwoord rood
        }
    });
}


// Functie om de huidige pagina op te halen
function getCurrentPage() {
    return parseInt(document.body.getAttribute("data-page")) || 1;
}



// Functies voor drag-and-drop functionaliteit
function allowDrop(ev) {
    ev.preventDefault();

    // Sta droppen alleen toe in droppable zones of de optieslijst
    if (!ev.target.classList.contains('droppable') && ev.target.id !== 'action-list') {
        return;
    }
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    // Houd de referentie van het huidige gesleepte element
    ev.dataTransfer.effectAllowed = "move"; // Optioneel: aangeef dat het element verplaatst wordt

    // Voeg een extra class toe om de styling aan te passen tijdens het slepen
    const draggedElement = ev.target;
    draggedElement.classList.add('dragging'); // Voeg een class toe voor de sleeptijd styling
}

// Functie om de styling te verwijderen als het slepen is voltooid
function dragEnd(ev) {
    const draggedElement = ev.target;
    draggedElement.classList.remove('dragging'); // Verwijder de sleeptijd styling
}


function drop(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text");
    const draggedElement = document.getElementById(data);
    const target = ev.target;

    // Controleer of het doel een droppable element is
    if (target.classList.contains('droppable')) {
        const existingElement = target.querySelector('.draggable');

        if (existingElement) {
            // Als er al een actie in de droppable zone is, verwissel ze
            const sourceParent = draggedElement.parentNode;
            sourceParent.appendChild(existingElement); // Zet de bestaande actie terug naar de vorige plek
        }

        // Voeg de gesleepte actie toe aan de droppable zone
        target.appendChild(draggedElement);
    } else if (target.classList.contains('draggable')) {
        // Wissel de gesleepte actie met de bestaande actie
        const existingParent = target.parentNode;
        existingParent.appendChild(draggedElement); // Zet de gesleepte actie op de plek van de bestaande actie
        target.parentNode.appendChild(target); // Zet de andere actie terug naar de vorige plek
    } else if (target.id === 'action-list') {
        // Als de gesleepte actie wordt teruggesleept naar de optieslijst
        target.appendChild(draggedElement);
    }
}


function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function loadQuestions(page) {
    const totalPages = questionsByPage.length;

    // Check of we voorbij de laatste vraagpagina zijn (conclusiepagina)
    if (page > totalPages) {
        loadConclusionPage();
        return;
    }

    const currentQuestions = questionsByPage[page - 1];

    const optionsContainer = document.querySelector(".options");
    const stepsContainer = document.querySelector(".steps");
    const quizText = document.getElementById("quiz-text");
    
  
    optionsContainer.innerHTML = ""; // Wis de opties
    stepsContainer.innerHTML = "";   // Wis de denkstappen
    

    // Controleer of de huidige pagina gewoon tekst bevat (bijvoorbeeld pagina 4)
    if (currentQuestions[0].info) {
        // Voeg alleen de info tekst toe zonder "action" en "step" koppen

        quizText.innerHTML = ``;
        const infoElement = document.createElement('p');
        infoElement.textContent = currentQuestions[0].info;
       
        quizText.appendChild(infoElement);  // Voeg het element toe aan de container

        // Verberg de opties en stappen containers
        
        document.querySelector(".steps").style.display = "none";
        document.getElementById("questions").style.display = "none";

        // Verberg de 'Controleer Antwoorden' knop, want er zijn geen vragen
        document.querySelector("button[onclick='checkAnswers()']").style.display = 'none';

    } else {
        // Zorg ervoor dat de opties en stappen containers zichtbaar zijn
        optionsContainer.style.display = "block";
        stepsContainer.style.display = "block";

        // Voeg de stappen en acties toe aan de container
        currentQuestions.forEach((question, index) => {
            // Voeg de stap toe (step)
            const stepElement = document.createElement('div');
            stepElement.id = `drop${index + 1}`;
            stepElement.classList.add('droppable', 'bg-gray-200', 'p-4', 'rounded-md', 'shadow-md', 'mb-2');
            stepElement.ondrop = drop;
            stepElement.ondragover = allowDrop;
            stepElement.innerHTML = question.step;
            stepsContainer.appendChild(stepElement);

            // Voeg de actie toe (action)
            const optionElement = document.createElement('div');
            optionElement.id = `option${index + 1}`;
            optionElement.classList.add('draggable', 'bg-gray-100', 'p-4', 'rounded-md', 'shadow-md', 'mb-2');
            optionElement.draggable = true;
            optionElement.ondragstart = drag;
            optionElement.ondragend = dragEnd;
            optionElement.innerHTML = question.action;
            optionsContainer.appendChild(optionElement);
        });

        // Toon de 'Controleer Antwoorden' knop
        document.querySelector("button[onclick='checkAnswers()']").style.display = 'inline-block';
    }
}




function loadConclusionPage() {
    // Verberg de vraag-sectie en toon de conclusie-tekst
    const quizContent = document.getElementById("quiz-content");
    document.querySelector(".options").style.display = "none";
    document.querySelector(".steps").style.display = "none";
    document.getElementById("questions").style.display = "none";
    const quizText = document.getElementById("quiz-text");
    quizText.innerHTML = ``;

    quizContent.innerHTML = `
        <h2 class="text-xl font-semibold mb-4">Conclusie</h2>
        <p class="text-lg mb-6">Je hebt de oefening voltooid. Tijdens deze oefening heb je de belangrijkste principes van Design Thinking, Computational Thinking, en Wetenschappelijk Denken toegepast.</p>
        <p class="text-lg mb-6">Je hebt geleerd hoe je problemen kunt analyseren, ideeën kunt genereren, oplossingen kunt testen en een wetenschappelijk onderzoek kunt uitvoeren. Deze denkwijzen zullen je helpen bij het ontwikkelen van innovatieve en duurzame oplossingen.</p>
    `;
    // Verberg de 'Controleer Antwoorden' knop
    document.querySelector("button[onclick='checkAnswers()']").style.display = 'none';

    // Verberg de navigatieknoppen
    document.getElementById("prevPage").style.display = 'none';
    document.getElementById("nextPage").style.display = 'none';
}


function changePage(newPage) {
    const totalPages = questionsByPage.length;

    if (newPage > 0 && newPage <= totalPages + 1) { // +1 om de conclusiepagina mee te tellen
        if (newPage === totalPages + 1) { // Controleer of de conclusiepagina moet worden geladen
            loadConclusionPage();
        } else {
            loadQuestions(newPage);
            document.body.setAttribute("data-page", newPage); // Bewaar de huidige pagina

            // Update het paginanummer in de <span>
            document.getElementById("page-number").textContent = newPage;

            // Zorg dat de 'Vorige' knop verdwijnt op de eerste pagina
            if (newPage === 1) {
                // Hier stel je de onclick functie in om naar de intro-pagina te navigeren
                document.getElementById("prevPage").onclick = function() {
                    window.location.href = introUrl; // Verwijs naar de intro pagina
                };
            }      

            // Verberg de 'Volgende' knop alleen op de conclusiepagina (na laatste pagina)
            if (newPage === totalPages) {
                document.getElementById("nextPage").textContent = ">";
            } else {
                document.getElementById("nextPage").style.display = "inline-block";
                document.getElementById("nextPage").textContent = ">";
            }
        }
    }
}



// Zorg dat de opties in willekeurige volgorde staan bij het laden van de pagina
document.addEventListener("DOMContentLoaded", function () {
    const currentPage = getCurrentPage();
    loadQuestions(currentPage);

    // Event listener voor de "Volgende" knop
    document.querySelector("#nextPage").addEventListener("click", function () {
        const currentPage = getCurrentPage();
        const totalPages = questionsByPage.length;

        if (currentPage < totalPages) {
            changePage(currentPage + 1);
        } else {
            loadConclusionPage(); // Toon conclusie als de laatste pagina is bereikt
        }
    });

    // Event listener voor de "Vorige" knop
    document.querySelector("#prevPage").addEventListener("click", function () {
        const currentPage = getCurrentPage();
        
         // Zorg ervoor dat we niet verder teruggaan dan de eerste pagina
         if (currentPage > 1) {
            changePage(currentPage - 1);
        } else {
            window.location.href = introUrl; // Ga naar de intro-pagina als we op pagina 1 zijn
        }
    });
});

