# create_reports.py

'''
A script to create two sample reports to be used in improved.py
'''

import os

os.makedirs("reports", exist_ok=True)

soil_text = """Soil Organic Matter and Nutrient Cycling in East Africa

Healthy soils in East Africa typically have 2–5% organic matter, which improves water retention,
provides slow-release nutrients and supports microbial biodiversity. Common constraints include
nitrogen and phosphorus depletion, which can be remediated through integrated nutrient management:
combining mineral fertilizers with compost and legume rotation. Cover cropping with species like
Mucuna pruriens reduces erosion, increases soil cover and boosts nitrogen fixation by 20–30%.
Regular pH testing (target 6.0–7.0) and micronutrient assays (Zn, B) are critical for high-value
vegetable and fruit production.
"""

water_text = """Small-Scale Irrigation and Water Harvesting in Sub-Saharan Africa

Rainfall variability in the Sahel and East Africa leads to frequent dry spells. Simple water
harvesting techniques—such as zai pits, contour bunds and stone lines—can increase infiltration
by up to 50%. Farmer-managed small reservoirs (100–500 m³) paired with drip irrigation boost
water-use efficiency to >80%. Integrating soil moisture sensors and SMS alerts allows precise
scheduling of irrigation, reducing water use by 25% and increasing yields by 15–20% in tomato and
maize trials.
"""

with open("reports/soil_health_ea.txt", "w", encoding="utf-8") as f:
    f.write(soil_text)

with open("reports/water_management.txt", "w", encoding="utf-8") as f:
    f.write(water_text)

print("✔️ reports/soil_health_ea.txt and water_management.txt created")
