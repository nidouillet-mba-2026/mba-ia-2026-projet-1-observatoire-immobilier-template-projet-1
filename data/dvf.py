import csv

# Fichiers source DVF
FILES = [
    "data/raw/ValeursFoncieres-2023.txt",
    "data/raw/ValeursFoncieres-2024.txt",
    "data/raw/ValeursFoncieres-2025-S1.txt"
]

# Fichier de sortie
OUTPUT_FILE = "data/dvf_toulon.csv"

# Code de Toulon dans DVF
TOULON_DEPARTEMENT = "83"
TOULON_COMMUNE = "137"

# Types de biens autorisés
VALID_TYPES = ["Maison", "Appartement"]


def convertir_en_float(valeur):
    """
    Convertit une valeur texte en float.
    Retourne None si la conversion est impossible.
    """
    if valeur is None or valeur == "":
        return None

    valeur = valeur.replace(",", ".").strip()

    try:
        return float(valeur)
    except ValueError:
        return None


def lire_et_filtrer_dvf():
    """
    Lit les fichiers DVF, filtre Toulon + Maison/Appartement,
    calcule le prix au m², puis retourne une liste de dictionnaires.
    """
    resultats = []

    for fichier in FILES:
        print(f"Lecture du fichier : {fichier}")

        with open(fichier, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="|")

            for row in reader:
                # On garde seulement les lignes du département 83
                if row.get("Code departement") != TOULON_DEPARTEMENT:
                    continue

                # On garde seulement la commune 137 = Toulon
                if row.get("Code commune") != TOULON_COMMUNE:
                    continue

                # On garde seulement Maison / Appartement
                if row.get("Type local") not in VALID_TYPES:
                    continue

                # On doit convertir le prix et la surface
                prix = convertir_en_float(row.get("Valeur fonciere"))
                surface = convertir_en_float(row.get("Surface reelle bati"))

                # On ignore les lignes inexploitables
                if prix is None or surface is None:
                    continue

                if surface <= 0:
                    continue

                # Calcul du prix au m²
                prix_m2 = prix / surface

                # Ajout de la ligne au propre
                resultats.append({
                    "date_mutation": row.get("Date mutation"),
                    "commune": row.get("Commune"),
                    "type_local": row.get("Type local"),
                    "surface_reelle_bati": round(surface, 2),
                    "valeur_fonciere": round(prix, 2),
                    "prix_m2": round(prix_m2, 2)
                })

    return resultats


def ecrire_csv(resultats):
    """
    Écrit les résultats dans le fichier CSV final.
    """
    colonnes = [
        "date_mutation",
        "commune",
        "type_local",
        "surface_reelle_bati",
        "valeur_fonciere",
        "prix_m2"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(resultats)

    print(f"Fichier créé : {OUTPUT_FILE}")


def main():
    resultats = lire_et_filtrer_dvf()
    print(f"Nombre de transactions gardées : {len(resultats)}")
    ecrire_csv(resultats)


if __name__ == "__main__":
    main()