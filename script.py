from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zorg ervoor dat je een veilige sleutel gebruikt

# Frameworks met stappen (voorbeelddata)
frameworks = {
    'Design Thinking': ['Empathize', 'Define', 'Ideate', 'Prototype', 'Test'],
    'Computational Thinking': ['Decomposition', 'Pattern Recognition', 'Abstraction', 'Algorithm Design'],
    'Scientific Thinking': ['Question', 'Hypothesis', 'Experiment', 'Results', 'Conclusion']
}

# Voorbeeld uitleggen (theorie)
explanations = {
    'Empathize': 'Inleven in de gebruiker',
    'Define': 'Het probleem duidelijk omschrijven',
    'Ideate': 'Creatieve oplossingen bedenken',
    'Prototype': 'Een prototype bouwen',
    'Test': 'Het prototype testen',
    'Decomposition': 'Het probleem opdelen in kleinere stukken',
    'Pattern Recognition': 'Herkennen van patronen in de gegevens',
    'Abstraction': 'Essentiële informatie identificeren',
    'Algorithm Design': 'Een stapsgewijze oplossing ontwerpen',
    'Question': 'Stel een onderzoeksvraag',
    'Hypothesis': 'Formuleer een testbare hypothese',
    'Experiment': 'Voer een experiment uit',
    'Results': 'Verzamel en analyseer de resultaten',
    'Conclusion': 'Trek een conclusie op basis van de resultaten'
}

# Voorbeeld casusvoorbeelden (praktijk)
case_examples = {
    'Empathize': 'Het interviewen van gebruikers om hun behoeften te begrijpen',
    'Define': 'De inzichten uit het interview gebruiken om het probleem te definiëren',
    'Ideate': 'Brainstormen over mogelijke oplossingen op basis van het gedefinieerde probleem',
    'Prototype': 'Een eenvoudige versie van een oplossing creëren',
    'Test': 'Het prototype testen met gebruikers en feedback verzamelen',
    'Decomposition': 'Een groot programmeerprobleem splitsen in kleinere modules',
    'Pattern Recognition': 'Terugkerende problemen of patronen herkennen tijdens het ontwikkelen',
    'Abstraction': 'Onbelangrijke details weglaten en focussen op de kern van het probleem',
    'Algorithm Design': 'Een duidelijk stapsgewijs algoritme maken om het probleem op te lossen',
    'Question': 'Bepalen welke onderzoeksvraag je wilt beantwoorden',
    'Hypothesis': 'Voorspellen wat het resultaat van een experiment zal zijn',
    'Experiment': 'Een reeks tests uitvoeren om de hypothese te testen',
    'Results': 'De uitkomsten van het experiment analyseren',
    'Conclusion': 'Op basis van de resultaten een conclusie trekken'
}

@app.route('/')
def choose_quiz():
    return render_template('choose.html')

@app.route('/theory', methods=['GET', 'POST'])
def theory_quiz():
    if request.method == 'POST':
        answers = request.get_json()
        score = 0
        total = len(answers)
        feedback = {}

        # Controleer antwoorden en geef feedback
        for step, given_explanation in answers.items():
            correct_explanation = explanations.get(step)
            if given_explanation == correct_explanation:
                score += 1
                feedback[step] = {
                    'answer': given_explanation,
                    'correct': True
                }
            else:
                feedback[step] = {
                    'answer': given_explanation,
                    'correct': False
                }

        # Sla de resultaten op in de sessie
        session['theory_results'] = feedback
        session['frameworks'] = frameworks

        # Stuur de score en feedback terug naar de client
        return jsonify({'score': score, 'total': total, 'feedback': feedback})

    # Render de theorie oefening met de frameworks en uitleggen
    return render_template('theory.html', frameworks=frameworks, explanations=explanations)

@app.route('/case', methods=['GET', 'POST'])
def case_quiz():
    if request.method == 'POST':
        answers = request.get_json()  # Dit zijn de gegeven antwoorden
        score = 0
        total = len(answers)
        feedback = {}

        # Omgekeerde dictionary om antwoordopties te relateren aan hun juiste stap
        example_to_step = {v: k for k, v in case_examples.items()}

        # Debugging: Print de example_to_step en de antwoorden
        print(f"Example to step mapping: {example_to_step}")
        print(f"Received answers: {answers}")

        # Controleer de gegeven antwoorden en geef feedback
        for step, given_example in answers.items():
            # Zoek de juiste stap op basis van het gegeven antwoord (beschrijving)
            correct_step = example_to_step.get(given_example, None)  # Voeg default None toe als fallback

            # Debugging: Bekijk wat er gebeurt
            print(f"Given example: {given_example}, Correct step: {correct_step}, Question step: {step}")

            # Vergelijk de stap die hoort bij het gegeven antwoord met de vraagstap
            if correct_step == step:
                score += 1
                feedback[step] = {
                    'selected_answer': given_example,  # Ingevoerde antwoord opslaan
                    'correct': True,
                    'correct_step': correct_step  # Correcte stap
                }
            else:
                feedback[step] = {
                    'selected_answer': given_example,  # Ingevoerde antwoord opslaan
                    'correct': False,
                    'correct_step': correct_step  # Correcte stap
                }

        # Sla de resultaten op in de sessie
        session['case_results'] = feedback
        session['frameworks'] = frameworks

        # Stuur de score en feedback terug naar de client
        return jsonify({'score': score, 'total': total, 'feedback': feedback})

    # Render de casus oefening met frameworks en casusvoorbeelden
    return render_template('case.html', frameworks=frameworks, case_examples=case_examples)


@app.route('/result')
def result():
    # Verkrijg de resultaten en frameworks uit de sessie
    case_results = session.get('case_results', {})
    frameworks = session.get('frameworks', {})

    # Render de result-pagina met de resultaten en frameworks
    return render_template('result.html', results=case_results, frameworks=frameworks, case_examples=case_examples)

@app.route('/choose')
def choose():
    return redirect(url_for('choose_quiz'))

if __name__ == '__main__':
    app.run(debug=True)
