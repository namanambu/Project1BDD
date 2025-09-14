import csv

# Define test variations

test_variations = [
    {
        "filename": "Large_Test.csv",
        "data": [
            ["Hospital", "H1A", "H1B", "H1C", "H2A", "H2B", "H2C", "H3A"],
            ["Num", 3, 2, 1, 2, 4, 3, 1],
            ["D1", 12, 34, 45, 14, 67, 56, 89],
            ["D2", 29, 83, 72, 63, 23, 19, 14],
            ["D3", 41, 67, 15, 36, 49, 84, 55],
            ["D4", 53, 19, 97, 22, 78, 80, 11],
            ["D5", 88, 25, 46, 10, 35, 50, 99],
        ],
    },
    {
        "filename": "Test_Var2.csv",
        "data": [
            ["Hospital", "H1", "H2", "H3"],
            ["Num", 1, 1, 1],
            ["D1", 0, 0, 0],
            ["D2", 1, 0, 1],
            ["D3", 0, 0, 0],
            ["D4", 1, 1, 0],
        ],
    },
    {
        "filename": "Test_Var3.csv",
        "data": [
            ["Hospital", "H1", "H2", "H3"],
            ["Num", 6, 4, 5],
            ["D1", 0, 6, 2],
            ["D2", 3, 0, 7],
            ["D3", 5, 2, 0],
            ["D4", 8, 1, 4],
        ],
    },
]

# Generate CSV files
i = 0
for variation in test_variations:
    if i == 0:
        with open(variation["filename"], mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(variation["data"])
        print(f"File {variation['filename']} has been created.")