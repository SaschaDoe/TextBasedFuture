Technical:
- Python
- PySide6
- PyTest

# Functional
- Start:
    [x] There should be a "New" and a "Exit" button at the "Start Screen".
    [x] New should lead to a "Civilisation Generation" screen.
    [ ] All random table data should be loaded at start.

- Civilisation Generation:    
    [ ] The "Civilisation Generation" screen should consists of a single button "Generate" at the start. When the data of the civilisation is there the labels and list should show.
    [ ] The Civilisation should consists of a name, civilisation_age, event_history, leader, backgrounds, philosophy, understood technology
    [ ] The leader name should be also a button that can be clicked an lead to the "Leader Screen"
    [ ] The civilisation backgrounds should be randomly chosen from the tables: elements, general_professions, modern_cultures, social_classes.
    Every civilisation has 1-4 backgrounds with probability 10%: 1, 60%: 2, 20%: 3, 10%: 4
    [ ] A button should lead to the start of the game

- Leader Screen:
    [ ] Shows name, event history, quote of own civilisation, his attributes (willpower, charisma, intelligence, intuition, strengh, constitution, dexterity, manual-dexterity).
    [ ] The leader name should be generated with a llm api considering the background and philosophies of the civilisation
    [ ] A button should lead back to "Civilisation Generation"

- The Game
    [ ] Turn based. Every turn there are 3 Choices to make for your civilisation
    [ ] Every turn has following phases 1. Optional event 2. Optional event response 3. Info 4. Command phase 5. optional battle phase
    [ ] 1. With the event chance (default 10%) there is a event from the list of events that are possible (could be changed over time what is possible)
    [ ] 2. When the event was called sometimes events can have responses mostly also 3 choices to make.
    [ ] 3. Description phase gives the optional outcome of the event, also other outcomes from last round like battles etc. 
    [ ] 4. In command you have 3 options presented to you and can also make standart commands like attack other civilisations etc.
    [ ] 5. Battle phase consists of choices for battle. mostly 3 and that 3 times.
    [ ] The game ends if you have made war victory, tranzsendence victory or cultural victory or when another player has made this victory, or all players are destroyed (could be though events).
    [ ] Every civilisation has bases (minimum 1 if none than it is destroyed) where it lives, bases that it owns, and cultural pressure from other civilisations and cultural pressure to other civilisations
    

# Non-Functional
    - Under a second waits for UI operations 
    - Load/store in paralel