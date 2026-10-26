# 🎬 CineMatch — Movie Recommender

CineMatch is a desktop app written entirely in Python. Type the name of a movie you like and it suggests similar movies based on their genres, shown in a clean, dark-themed window.

---

## ✨ Features

- 🔍 **Fuzzy title search** – type a partial or approximate title and the app finds the closest match.
- 🎯 **Genre-based recommendations** – movies are ranked by how similar their genres are to your movie.
- 📊 **Match percentage** – every recommendation shows a score and a progress bar.
- 🎚️ **Adjustable results** – choose between 3 and 20 recommendations with a slider.
- 🎨 **Modern dark UI** – built with CustomTkinter: rounded cards, genre tags and a scrollable results list.
- ⌨️ **Press Enter to search** – no need to click the button.
- 🛡️ **Friendly error messages** – empty input or unknown titles don't crash the app.

---

## 🧠 How It Works

1. **Clean the text** – titles and genres are lowercased, and parentheses and digits (such as release years) are removed.
2. **Find the movie** – titles are converted into word-count vectors with `CountVectorizer`. Cosine similarity picks the title closest to your input.
3. **Compare genres** – the genres of that movie (e.g. `Adventure|Animation|Children`) are vectorized the same way and compared against every other movie with cosine similarity.
4. **Rank and display** – the top results (excluding the movie you searched for) are shown as cards with a match percentage.

This is a simple **content-based filtering** approach: it recommends items based on their own attributes, not on other users' ratings.

---

## 📁 Project Structure

```
.
├── movie_gui.py     # The application (logic + GUI)
├── movies.csv       # Movie dataset (you provide this)
└── README.md        # This file
```

---

## 📦 Requirements

- Python 3.8 or newer
- [pandas](https://pandas.pydata.org/)
- [scikit-learn](https://scikit-learn.org/)
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 🚀 Installation

```bash
# 1. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install pandas scikit-learn customtkinter
```

---

## 📄 Dataset Format

Place a `movies.csv` file in the same folder as `movie_gui.py`. It must have at least these two columns:

| Column   | Description                                  | Example                                   |
|----------|----------------------------------------------|-------------------------------------------|
| `title`  | Movie name, optionally with the year         | `Toy Story (1995)`                        |
| `genres` | Genres separated by a pipe (`\|`)            | `Adventure\|Animation\|Children\|Comedy`  |

The [MovieLens](https://grouplens.org/datasets/movielens/) `movies.csv` file uses exactly this format and works out of the box.

---

## ▶️ Usage

```bash
python movie_gui.py
```

1. Type a movie title (for example `Toy Story`).
2. Move the slider to choose how many recommendations you want.
3. Click **✨ Recommend** or press **Enter**.
4. Browse the results. The top banner shows which movie was matched, and each card shows the title, genres and match percentage.

---

## 🖼️ Interface Overview

| Area               | Purpose                                              |
|--------------------|------------------------------------------------------|
| Search box         | Enter the movie you like                             |
| Slider             | Number of recommendations (3–20)                     |
| Closest match      | The movie the app understood from your input         |
| Recommendation list| Ranked cards with genres and a match-percentage bar  |

---

## 🛠️ Customization

- **Colors** – edit the `PINK`, `ORANGE`, `BG`, `CARD` and `MUTED` constants near the top of the GUI section.
- **Number of results** – change the slider range in `ctk.CTkSlider(from_=3, to=20, ...)`.
- **Theme** – switch `ctk.set_appearance_mode("dark")` to `"light"` or `"system"`.

---

## ⚠️ Limitations

- Recommendations use **genres only**, so many movies can tie with identical scores.
- Title matching is word-based; a very short or misspelled title may match the wrong movie.
- There is no use of ratings, cast, plot or user history.

---

## 🔮 Future Ideas

- Include plot descriptions or tags and use TF-IDF for better similarity.
- Show posters through the TMDB API.
- Add autocomplete suggestions while typing.
- Combine content-based filtering with user ratings (collaborative filtering).
- Package the app as a standalone `.exe` with PyInstaller.

---

## 🧰 Troubleshooting

| Problem                                | Fix                                                               |
|----------------------------------------|-------------------------------------------------------------------|
| `FileNotFoundError: movies.csv`        | Put `movies.csv` in the same folder you run the script from.      |
| `ModuleNotFoundError: customtkinter`   | Run `pip install customtkinter`.                                  |
| "No matching movie found"              | Try a different or simpler part of the title.                     |
| Window looks blurry on Windows         | Right-click Python → Properties → Compatibility → High DPI settings. |

---

## 📜 License

Free to use, modify and share for learning and personal projects.

---

Made with ❤️ using Python, pandas, scikit-learn and CustomTkinter.