import json
import os

def create_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, 'w') as f:
        json.dump(nb, f, indent=2)

# Material EDA cells
material_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# Material Data EDA\n", "Exploratory Data Analysis of material properties from Materials Project and AFLOW."]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": ["import pandas as pd\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "\n", "df = pd.read_csv('../data/external/DS1_material_properties_5500.csv')\n", "df.head()"]
    }
]

# Financial EDA cells
financial_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# Financial Data EDA\n", "Exploratory Data Analysis of commodity prices and technical indicators."]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": ["import pandas as pd\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "\n", "df = pd.read_csv('../data/external/DS2_commodity_prices_10yr.csv')\n", "df.head()"]
    }
]

if __name__ == "__main__":
    os.makedirs('notebooks', exist_ok=True)
    create_notebook('notebooks/01_material_eda.ipynb', material_cells)
    create_notebook('notebooks/02_financial_eda.ipynb', financial_cells)
    print("Notebooks created.")
