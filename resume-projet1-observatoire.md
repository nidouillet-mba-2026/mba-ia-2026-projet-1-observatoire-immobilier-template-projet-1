# Résumé — Projet 1 : Observatoire du Marché Immobilier Toulonnais

## Contexte

**Client fictif :** NidDouillet, agence immobilière toulonnaise ciblant des jeunes couples primo-accédants avec un budget maximum de 450 000 €. L'agence effectue actuellement ses recherches manuellement (SeLoger, tableurs, appels téléphoniques). L'objectif est de remplacer ce travail manuel par un outil en ligne alimenté par des données réelles.

> ⚠️ Le produit doit être utilisable par les conseillers dès le lendemain de la soutenance.

---

## Livrable attendu

Une **application Streamlit déployée** (URL publique fonctionnelle) comprenant :
- État du marché
- Filtres (budget, surface, quartier, type)
- Tendances (prix/m² par quartier, distributions)
- Opportunités (biens sous-évalués identifiés)

**Stack :** Python + Streamlit + Streamlit Community Cloud

---

## Contraintes non-négociables

- **Données réelles uniquement** — pas de CSV fabriqué (DVF + annonces réelles)
- **Application déployée** — URL publique fonctionnelle le jour de la soutenance
- **Algorithmes from scratch** — stats et régression sans sklearn/numpy
- **Git workflow** — commits significatifs par membre, branches + Pull Requests

---

## Collecte des données

**DVF (obligatoire)**
- Source : data.gouv.fr/geo-dvf
- Code INSEE Toulon : 83137
- Filtrer : 2 dernières années, appartements et maisons
- Objectif : 500+ transactions

**Annonces actuelles**
- Option A (recommandé) : GumLoop (workflow no-code → export JSON/Sheet)
- Option B : Scraper Python avec requests + BeautifulSoup (SeLoger, PAP, LeBonCoin)
- Objectif : 100+ annonces < 500k€

---

## Algorithmes from scratch

Basés sur le livre *Data Science From Scratch* de Joel Grus.

**Statistiques** (`analysis/stats.py`) — Chapitre 5
- `mean()`, `median()`, `variance()`, `standard_deviation()`, `covariance()`, `correlation()`

**Régression** (`analysis/regression.py`) — Chapitre 14
- `predict()`, `error()`, `sum_of_sqerrors()`, `least_squares_fit()`, `r_squared()`

🚫 Interdit : `numpy.mean()`, `pandas.mean()`, `sklearn`, `statistics.*` — listes Python uniquement

**Bonus** — k-NN (Chapitre 12) : `distance()`, `knn_similar()` → "Biens similaires à votre recherche"

---

## Enrichissement IA (recommandé)

Via Claude API ou OpenAI (intégré dans GumLoop ou en Python) :
1. **Extraction structurée** — parser les descriptions textuelles vers des champs normalisés (étage, parking, vue mer…)
2. **Résumé par quartier** — synthèse basée sur les annonces
3. **Scoring automatique** — classifier : Opportunité / Prix marché / Surévalué

---

## Structure du projet suggérée

```
observatoire-toulon/
├── data/
│   ├── collect.py
│   ├── dvf.py
│   └── raw/
├── analysis/
│   ├── stats.py
│   ├── regression.py
│   └── scoring.py
├── app/
│   └── streamlit_app.py
├── tests/
│   └── test_*.py
├── .github/workflows/
├── requirements.txt
└── README.md
```

---

## Évaluation

### Code GitHub — 55 pts
| Critère | Points |
|---|---|
| Stats from scratch | 15 |
| Régression from scratch | 10 |
| Pipeline collecte | 15 |
| App déployée | 10 |
| Tests pytest | 5 |

### Soutenance — 45 pts
| Critère | Points |
|---|---|
| Architecture & choix | 15 |
| Compréhension algos | 10 |
| Répartition du travail | 10 |
| Recul critique | 5 |
| Git workflow | 5 |

### Questions typiques du jury
- *"Montrez-moi votre régression. Qu'est-ce que le R² vous dit ?"*
- *"Comment votre pipeline se met-il à jour ?"*
- *"Votre corrélation surface/prix, elle est de combien ? C'est attendu ?"*

---

## GitHub Classroom

- Lien d'invitation : https://classroom.github.com/a/JY1xUUGg
- Un repo privé est créé automatiquement par groupe
- CI automatique à chaque push (pytest → score sur 55 pts via GitHub Actions)
- Score visible dans l'onglet **Actions** → workflow "Evaluation Automatique"

---

## Contacts — Product Owners (experts immobilier)

- **Sarah Champagne** — Investisseur en immobilier : sarah.champagne@sciencespo.fr
- **Louis-Marie Masfayon** — Chargé d'études en immobilier logistique : louismariemasfayon@yahoo.fr

---

## Livrables à rendre

| Livrable | Détails |
|---|---|
| Repo GitHub | Partagé avec l'enseignant (pas de ZIP) |
| URL déployée | Fonctionnelle le jour J, dans le README |
| README complet | Installation, architecture, rôles, lien démo |
| Soutenance | 15 min : 10 min démo + 5 min questions |

**Durée :** 1 semaine — **Groupes :** 4 étudiants maximum
