import pandas as pd
import numpy as np

def generate_cairo_data():
    np.random.seed(42)

    neighborhoods = [
        "Maadi", "Zamalek", "New Cairo", "Heliopolis", "Nasr City",
        "6th of October", "Sheikh Zayed", "Dokki", "Mohandessin", "Garden City",
        "Rehab City", "Katameya", "Tagamoa", "Shorouk", "Obour"
    ]

    property_types = ["Apartment", "Villa", "Duplex", "Studio", "Penthouse"]

    # Base prices per sqm (EGP) per neighborhood
    base_prices = {
        "Zamalek": 45000, "Garden City": 42000, "Maadi": 38000,
        "Heliopolis": 35000, "New Cairo": 32000, "Katameya": 36000,
        "Sheikh Zayed": 30000, "6th of October": 22000, "Tagamoa": 28000,
        "Dokki": 33000, "Mohandessin": 31000, "Nasr City": 25000,
        "Rehab City": 27000, "Shorouk": 20000, "Obour": 18000
    }

    # Lat/lon for each neighborhood (approximate)
    coords = {
        "Zamalek": (30.065, 31.219), "Garden City": (30.038, 31.231),
        "Maadi": (29.960, 31.257), "Heliopolis": (30.087, 31.321),
        "New Cairo": (30.027, 31.470), "Katameya": (29.980, 31.430),
        "Sheikh Zayed": (30.063, 30.949), "6th of October": (29.936, 30.918),
        "Tagamoa": (30.022, 31.451), "Dokki": (30.047, 31.211),
        "Mohandessin": (30.059, 31.198), "Nasr City": (30.066, 31.341),
        "Rehab City": (30.058, 31.493), "Shorouk": (30.117, 31.607),
        "Obour": (30.200, 31.470)
    }

    records = []
    months = pd.date_range(start="2021-01-01", end="2024-12-01", freq="MS")

    for month in months:
        for neighborhood in neighborhoods:
            for ptype in property_types:
                # Skip some combos to make it realistic
                if ptype == "Villa" and neighborhood in ["Zamalek", "Garden City", "Dokki", "Mohandessin"]:
                    continue
                if ptype == "Penthouse" and neighborhood in ["Shorouk", "Obour", "6th of October"]:
                    continue

                n_listings = np.random.randint(5, 40)
                base = base_prices[neighborhood]

                # Inflation trend: prices increase ~20% per year
                months_elapsed = (month.year - 2021) * 12 + month.month
                trend_factor = 1 + (months_elapsed / 12) * 0.20

                # Property type premium
                type_multiplier = {
                    "Apartment": 1.0, "Studio": 0.85, "Duplex": 1.25,
                    "Villa": 1.60, "Penthouse": 1.80
                }[ptype]

                avg_sqm = {
                    "Apartment": 130, "Studio": 60, "Duplex": 200,
                    "Villa": 350, "Penthouse": 250
                }[ptype]

                price_per_sqm = base * trend_factor * type_multiplier * np.random.uniform(0.92, 1.08)
                avg_price = price_per_sqm * avg_sqm

                lat, lon = coords[neighborhood]

                records.append({
                    "date": month,
                    "neighborhood": neighborhood,
                    "property_type": ptype,
                    "avg_price_egp": round(avg_price),
                    "price_per_sqm": round(price_per_sqm),
                    "avg_area_sqm": avg_sqm,
                    "listings": n_listings,
                    "lat": lat + np.random.uniform(-0.01, 0.01),
                    "lon": lon + np.random.uniform(-0.01, 0.01),
                })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_cairo_data()
    print(df.head())
    print(f"\nTotal records: {len(df)}")
    print(f"Neighborhoods: {df['neighborhood'].nunique()}")
