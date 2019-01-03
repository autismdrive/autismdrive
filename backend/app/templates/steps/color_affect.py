from app.model.questionnaire import StarStep, StarFieldGroup, StarFieldText, StarFieldSelect

@StarStep
class ColorAffectCorrelation():
    title = "How does color affect your mood?"
    description = "These questions will change the way you think by getting you to think about a particular color."
    fields = [
        StarFieldText({
            prompt_text: "What's the first word that comes to mind when you think of the color blue?",
            help_text: "Enter any old word here. Don't think too hard about it.",
            placeholder_text: "Your word here."
        }),
        StarFieldText({
            prompt_text: "Write a few sentences about how the color orange makes you feel",
            help_text: "It's okay if you can't think of anything in particular. Just write whatever comes to mind.",
            placeholder_text: "Write 2-3 sentences here."
        }),
        StarFieldSelect({
            prompt_text: "How are you feeling today?",
            options: [
                "Terrible",
                "Just okay",
                "Awesome"
            ]
        })
        StarFieldGroup([
          title: "Address",
          StarFieldText({
              prompt_text: "Street Address",
          }),
          StarFieldText({
              prompt_text: "City",
          }),
          StarFieldText({
              prompt_text: "State",
          }),
          StarFieldText({
              prompt_text: "Zip",
          }),
        ])
    ]