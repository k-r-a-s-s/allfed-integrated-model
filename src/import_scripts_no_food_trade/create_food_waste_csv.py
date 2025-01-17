from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing food waste data...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_waste = pd.read_excel(xls, "Food waste")[
    [
        "ISO3 Country Code",
        "Country",
        "Crops (Greenhouses/ outdoor growing)",
        "Sugar",
        "Meat",
        "Dairy",
        "Seafood",
        "% wasted - pre disaster",
        "% wasted - post disaster - food prices double",
        "% wasted - post disaster - food prices triple",
    ]
]

# Rename columns
df_waste.columns = [
    "iso3",
    "country",
    "distribution_loss_crops",
    "distribution_loss_sugar",
    "distribution_loss_meat",
    "distribution_loss_dairy",
    "distribution_loss_seafood",
    "retail_waste_baseline",
    "retail_waste_price_double",
    "retail_waste_price_triple",
]


df_waste = df_waste.iloc[
    0:138,
]

df_waste.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "food_waste_csv.csv",
    sep=",",
    index=False,
)
