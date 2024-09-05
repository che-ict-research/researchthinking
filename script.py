from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Raamwerken en hun stappen
frameworks = {
    "Design Thinking": ["Empathize", "Define", "Ideate", "Prototype", "Test"],
    "Computational Thinking": ["Decomposition", "Pattern Recognition", "Abstraction", "Algorithm Design"],
    "Scientific Thinking": ["Vraag", "Hypothese", "Experiment", "Resultaten", "Conclusie"]
}

# Uitleg voor de theorie-oefening
theory_explanations = {
    "Empathize": "Het begrijpen van de behoeften van gebruikers door observatie en interactie.",
    "Define": "Het specificeren van het probleem of de uitdaging die moet worden opgelost.",
    "Ideate": "Het bedenken van verschillende creatieve oplossingen voor het probleem.",
    "Prototype": "Het maken van een eenvoudig model of versie van de oplossing om te testen.",
    "Test": "Het evalueren van de oplossing door gebruikersfeedback en aanpassingen.",
    "Decomposition": "Het splitsen van een groot probleem in kleinere, beter beheersbare stukken.",
    "Pattern Recognition": "Het herkennen van terugkerende patronen in data of problemen.",
    "Abstraction": "Het vereenvoudigen van een probleem door alleen de essentiële onderdelen te overwegen.",
    "Algorithm Design": "Het ontwerpen van een reeks stappen of procedures om een probleem op te lossen.",
    "Vraag": "Het formuleren van een onderzoeksvraag om een probleem te onderzoeken.",
    "Hypothese": "Een veronderstelling doen over wat de uitkomst van het experiment zou kunnen zijn.",
    "Experiment": "Het uitvoeren van een test om de hypothese te onderzoeken.",
    "Resultaten": "Het verzamelen en analyseren van gegevens die voortkomen uit het experiment.",
    "Conclusie": "Het trekken van een conclusie op basis van de resultaten en het bevestigen of weerleggen van de hypothese."
}

# Praktijkvoorbeelden uit de casus voor de toegepaste oefening
case_examples = {
    "Empathize": "Onderzoek naar hoe huishoudens hun waterverbruik monitoren en welke uitdagingen zij ervaren.",
    "Define": "Het vaststellen van het probleem: Gebruikers hebben moeite om hun waterverbruik real-time te monitoren.",
    "Ideate": "Het brainstormen over mogelijke oplossingen, zoals een app die waterverbruik in real-time toont.",
    "Prototype": "Het maken van een eenvoudige wireframe van de mobiele app om feedback te verzamelen van potentiële gebruikers.",
    "Test": "Een testgroep gebruikers de app laten gebruiken en hun feedback verzamelen om verbeteringen door te voeren.",
    "Decomposition": "Het opsplitsen van het probleem in kleinere componenten: datacollectie, real-time verwerking, en gebruikersinterface.",
    "Pattern Recognition": "Herkenning van patronen in waterverbruik, zoals piekmomenten tijdens het ochtendgebruik of specifieke apparaten die veel water verbruiken.",
    "Abstraction": "Het abstraheren van het probleem door alleen te focussen op de belangrijkste variabelen: tijd, waterverbruik en locatie.",
    "Algorithm Design": "Het ontwerpen van een algoritme dat waterverbruik voorspelt op basis van historische data en real-time inputs.",
    "Vraag": "Hoe kan een mobiele app bijdragen aan het verminderen van waterverbruik in huishoudens?",
    "Hypothese": "Als gebruikers real-time inzicht krijgen in hun waterverbruik, zullen ze bewuster omgaan met watergebruik en minder verbruiken.",
    "Experiment": "Een groep huishoudens gebruikt de app voor een maand, terwijl een controlegroep de app niet gebruikt.",
    "Resultaten": "De data wordt verzameld en vergeleken: de gebruikers van de app verbruiken gemiddeld 10% minder water dan de controlegroep.",
    "Conclusie": "De hypothese wordt bevestigd: real-time feedback over waterverbruik draagt bij aan vermindering van waterverbruik."
}

# Correcte antwoorden voor de theorie-oefening
theory_correct_answers = {
    "Design Thinking": {
        "Empathize": theory_explanations["Empathize"],
        "Define": theory_explanations["Define"],
        "Ideate": theory_explanations["Ideate"],
        "Prototype": theory_explanations["Prototype"],
        "Test": theory_explanations["Test"]
    },
    "Computational Thinking": {
        "Decomposition": theory_explanations["Decomposition"],
        "Pattern Recognition": theory_explanations["Pattern Recognition"],
        "Abstraction": theory_explanations["Abstraction"],
        "Algorithm Design": theory_explanations["Algorithm Design"]
    },
    "Scientific Thinking": {
        "Vraag": theory_explanations["Vraag"],
        "Hypothese": theory_explanations["Hypothese"],
        "Experiment": theory_explanations["Experiment"],
        "Resultaten": theory_explanations["Resultaten"],
        "Conclusie": theory_explanations["Conclusie"]
    }
}

# Correcte antwoorden voor de casus-oefening
case_correct_answers = {
    "Design Thinking": {
        "Empathize": case_examples["Empathize"],
        "Define": case_examples["Define"],
        "Ideate": case_examples["Ideate"],
        "Prototype": case_examples["Prototype"],
        "Test": case_examples["Test"]
    },
    "Computational Thinking": {
        "Decomposition": case_examples["Decomposition"],
        "Pattern Recognition": case_examples["Pattern Recognition"],
        "Abstraction": case_examples["Abstraction"],
        "Algorithm Design": case_examples["Algorithm Design"]
    },
    "Scientific Thinking": {
        "Vraag": case_examples["Vraag"],
        "Hypothese": case_examples["Hypothese"],
        "Experiment": case_examples["Experiment"],
        "Resultaten": case_examples["Resultaten"],
        "Conclusie": case_examples["Conclusie"]
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/theory", methods=["GET", "POST"])
def theory():
    if request.method == "POST":
        submitted_answers = {}
        score = 0
        total = 0
        feedback = {}

        for framework, steps in frameworks.items():
            submitted_answers[framework] = {}
            for step in steps:
                explanation = request.form.get(f"{framework}_{step}")
                submitted_answers[framework][step] = explanation

                total += 1
                if explanation == theory_correct_answers[framework][step]:
                    score += 1
                    feedback[f"{framework} - {step}"] = "Correct"
                else:
                    feedback[f"{framework} - {step}"] = f"Incorrect, het juiste antwoord is: {theory_correct_answers[framework][step]}"

        return render_template("result.html", score=score, total=total, feedback=feedback)

    return render_template("theory.html", frameworks=frameworks, explanations=theory_explanations)

@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "POST":
        submitted_answers = {}
        score = 0
        total = 0
        feedback = {}

        for framework, steps in frameworks.items():
            submitted_answers[framework] = {}
            for step in steps:
                case_example = request.form.get(f"{framework}_{step}")
                submitted_answers[framework][step] = case_example

                total += 1
                if case_example == case_correct_answers[framework][step]:
                    score += 1
                    feedback[f"{framework} - {step}"] = "Correct"
                else:
                    feedback[f"{framework} - {step}"] = f"Incorrect, het juiste antwoord is: {case_correct_answers[framework][step]}"

        return render_template("result.html", score=score, total=total, feedback=feedback)

    return render_template("case.html", frameworks=frameworks, case_examples=case_examples)

if __name__ == "__main__":
    app.run(debug=True)
