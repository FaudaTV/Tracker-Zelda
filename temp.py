# Nom du fichier de sortie
output_file = "items_zelda.txt"

# Structure du template avec des placeholders {i}
html_template = """<div class="item-wrapper">
    <img src="../images/ZeldaBOTW/t{i}.png" class="item" id="zbotw-f-t{i}" onclick="toggleItem('zbotw-f-t{i}')">
</div>"""

with open(output_file, "w", encoding="utf-8") as f:
    # On boucle de 1 à 107 inclus
    for i in range(1, 108):
        f.write(html_template.format(i=i) + "\n")

print(f"Terminé ! Le code a été généré dans {output_file}")