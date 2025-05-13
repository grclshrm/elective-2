import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import tkinter as tk
from tkinter import ttk, messagebox, font

# Load the data
df = pd.read_csv("ermita.csv", delimiter='\t')
df_clean = df.dropna(subset=['title', 'country', 'release_year', 'type'])

# Label Encoding
le_country = LabelEncoder()
df_clean['country_enc'] = le_country.fit_transform(df_clean['country'])

le_title = LabelEncoder()
df_clean['title_enc'] = le_title.fit_transform(df_clean['title'])

le_type = LabelEncoder()
df_clean['type_enc'] = le_type.fit_transform(df_clean['type'])

X = df_clean[['country_enc', 'release_year', 'title_enc']]
y = df_clean['type_enc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# GUI Function
def predict_type():
    title_input = title_var.get().strip()
    country_input = country_var.get().strip()
    year_input = year_var.get().strip()

    if not title_input or not country_input or not year_input:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    if not year_input.isdigit():
        messagebox.showerror("Input Error", "Release year must be a number.")
        return

    if country_input not in le_country.classes_:
        messagebox.showerror("Input Error", f"Country '{country_input}' not in training data.")
        return

    if title_input not in le_title.classes_:
        messagebox.showerror("Input Error", f"Title '{title_input}' not in training data.")
        return

    country_encoded = le_country.transform([country_input])[0]
    title_encoded = le_title.transform([title_input])[0]
    year = int(year_input)

    prediction = model.predict([[country_encoded, year, title_encoded]])
    predicted_type = le_type.inverse_transform(prediction)[0]
    result_var.set(f"🎬 Predicted Type: {predicted_type}")

# Create GUI
app = tk.Tk()
app.title("NETFLIX")
app.configure(bg="#f9f9f9")

# Custom fonts
title_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Helvetica", size=10)

# Title label
tk.Label(app, text="TV SHOW OR MOVIE", font=title_font, fg="#3366cc", bg="#f9f9f9").grid(row=0, column=0, columnspan=2, pady=(20,10))

# Input fields
fields = [("Title", "title_var"), ("Country", "country_var"), ("Release Year", "year_var")]
vars = {}

for i, (label, varname) in enumerate(fields, start=1):
    tk.Label(app, text=label + ":", font=label_font, bg="#f9f9f9").grid(row=i, column=0, sticky="e", padx=10, pady=5)
    vars[varname] = tk.StringVar()
    ttk.Entry(app, textvariable=vars[varname], width=30).grid(row=i, column=1, padx=10, pady=5)

# Bind variables
title_var = vars["title_var"]
country_var = vars["country_var"]
year_var = vars["year_var"]

# Predict button
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=6)
ttk.Button(app, text="Predict Type", command=predict_type).grid(row=4, column=0, columnspan=2, pady=15)

# Result label
result_var = tk.StringVar()
result_label = tk.Label(app, textvariable=result_var, font=("Helvetica", 11, "bold"), fg="#006400", bg="#f9f9f9")
result_label.grid(row=5, column=0, columnspan=2, pady=(5, 20))

app.mainloop()
