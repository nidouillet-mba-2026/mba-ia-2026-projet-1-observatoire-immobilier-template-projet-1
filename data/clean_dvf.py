import csv

# Fichier source
INPUT_FILE = "data/dvf_toulon.csv"
# Fichier de sortie
OUTPUT_FILE = "data/dvf_toulon_clean.csv"

def convertir_en_float(valeur):
    """
    Convertit une valeur texte en float et retourne None si la conversion est impossible
    """
    if valeur is None or valeur == "":
        return None

    valeur = str(valeur).replace(",", ".").strip()

    try:
        return float(valeur)
    except ValueError:
        return None


def nettoyer_dvf():
    """
    Lit le fichier DVF Toulon, supprime les lignes invalides ou aberrantes, puis retourne une liste propre.
    """
    resultats = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Convertit les colonnes numériques
            prix = convertir_en_float(row.get("valeur_fonciere"))
            surface = convertir_en_float(row.get("surface_reelle_bati"))
            prix_m2 = convertir_en_float(row.get("prix_m2"))

            # Ignore les lignes inexploitables
            if prix is None or surface is None or prix_m2 is None:
                continue

            if prix <= 0 or surface <= 0:
                continue

            # On enlève les valeurs aberrantes de prix au m²
            if prix_m2 < 500 or prix_m2 > 20000:
                continue

            # On enlève les biens trop petits ou trop grands (couple de deux personnes)
            if surface < 10 or surface > 500:
                continue

            # On garde la ligne nettoyée
            resultats.append({
                "date_mutation": row.get("date_mutation"),
                "commune": row.get("commune"),
                "type_local": row.get("type_local"),
                "surface_reelle_bati": round(surface, 2),
                "valeur_fonciere": round(prix, 2),
                "prix_m2": round(prix_m2, 2)
            })

    return resultats


def ecrire_csv(resultats):
    """
    Écrit les résultats nettoyés dans un nouveau fichier CSV.
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

    print(f"Fichier nettoyé créé : {OUTPUT_FILE}")


def main():
    resultats = nettoyer_dvf()
    print(f"Nombre de transactions après nettoyage : {len(resultats)}")
    ecrire_csv(resultats)


if __name__ == "__main__":
    main()