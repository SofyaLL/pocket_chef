from pathlib import Path
from fastmcp import FastMCP
import pandas as pd


mcp = FastMCP(name="ChefMCP")

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "data" / "Recipes_en.csv"
recipes_df = pd.read_csv(csv_path)
recipes_df["ingredients"] = recipes_df["ingredients"].apply(
    lambda x: (
        x.replace("Potatoes type A, B, C", "Potatoes type A/B/C")
        if isinstance(x, str)
        else x
    )
)
ingridients_dict = dict(
    zip(recipes_df["name"].values, recipes_df["ingredients"].values)
)


@mcp.tool
def recipe_finder() -> list[str]:
    """Return all available recipes."""
    return list(recipes_df["name"].values)


@mcp.tool
def get_ingridients(recipe: str) -> list[str]:
    """Return list of ingridients for one recipe."""
    return ingridients_dict[recipe].split(", ")


if __name__ == "__main__":
    mcp.run()
