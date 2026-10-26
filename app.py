import re
import customtkinter as ctk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Recommender logic ----------
def cleaner(text):
    text = str(text).lower().strip()
    text = text.replace("(", "").replace(")", "")
    text = re.sub(r"\d+", "", text)
    return text


data = pd.read_csv("movies.csv")
data["clean_title"] = data["title"].apply(cleaner)
data["clean_genre"] = data["genres"].apply(cleaner).str.replace("|", " ", regex=False)

title_cv = CountVectorizer()
title_vectors = title_cv.fit_transform(data["clean_title"])

genre_cv = CountVectorizer()
genre_vectors = genre_cv.fit_transform(data["clean_genre"])


def recommend(movie_name, n):
    movie_vec = title_cv.transform([cleaner(movie_name)])
    title_scores = cosine_similarity(title_vectors, movie_vec).flatten()
    best = title_scores.argmax()
    if title_scores[best] == 0:
        return None, None

    selected = data.iloc[best]
    genre_text = cleaner(selected["genres"]).replace("|", " ")
    genre_vec = genre_cv.transform([genre_text])
    scores = cosine_similarity(genre_vectors, genre_vec).flatten()

    order = [i for i in scores.argsort()[::-1] if i != best][:n]
    result = data.iloc[order].copy()
    result["score"] = scores[order]
    return selected, result


# ---------- GUI ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PINK = "#ff4e8a"
ORANGE = "#ff8a4c"
BG = "#12081f"
CARD = "#201236"
MUTED = "#b9b0d6"


class CineMatch(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CineMatch - Movie Recommender")
        self.geometry("760x820")
        self.minsize(640, 600)
        self.configure(fg_color=BG)

        # Header
        ctk.CTkLabel(
            self, text="🎬 CineMatch",
            font=ctk.CTkFont("Segoe UI", 40, "bold"), text_color=PINK,
        ).pack(pady=(28, 0))
        ctk.CTkLabel(
            self, text="Tell us a movie you love — we'll find your next favourite.",
            font=ctk.CTkFont("Segoe UI", 14), text_color=MUTED,
        ).pack(pady=(2, 18))

        # Search row
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=36)
        self.entry = ctk.CTkEntry(
            row, height=46, corner_radius=14, border_color="#4a3570",
            fg_color=CARD, font=ctk.CTkFont("Segoe UI", 15),
            placeholder_text="e.g. Toy Story, The Matrix, Jumanji…",
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.search())
        ctk.CTkButton(
            row, text="✨ Recommend", height=46, width=150, corner_radius=14,
            fg_color=PINK, hover_color=ORANGE,
            font=ctk.CTkFont("Segoe UI", 15, "bold"), command=self.search,
        ).pack(side="right")

        # Slider row
        srow = ctk.CTkFrame(self, fg_color="transparent")
        srow.pack(fill="x", padx=40, pady=(14, 6))
        ctk.CTkLabel(srow, text="Recommendations:", text_color=MUTED).pack(side="left")
        self.count_label = ctk.CTkLabel(srow, text="10", text_color=ORANGE,
                                        font=ctk.CTkFont(weight="bold"))
        self.count_label.pack(side="right")
        self.slider = ctk.CTkSlider(
            srow, from_=3, to=20, number_of_steps=17,
            progress_color=PINK, button_color=ORANGE, button_hover_color=PINK,
            command=lambda v: self.count_label.configure(text=str(int(v))),
        )
        self.slider.set(10)
        self.slider.pack(side="left", fill="x", expand=True, padx=12)

        self.status = ctk.CTkLabel(self, text="", text_color=MUTED,
                                   font=ctk.CTkFont("Segoe UI", 13))
        self.status.pack(pady=(8, 4))

        # Results
        self.results = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results.pack(fill="both", expand=True, padx=26, pady=(0, 18))

        self.entry.focus()

    def clear(self):
        for w in self.results.winfo_children():
            w.destroy()

    def genre_chips(self, parent, genres):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        for g in genres.split("|"):
            ctk.CTkLabel(
                box, text=g, corner_radius=10, fg_color="#3b1f55",
                text_color="#ffb3d1", font=ctk.CTkFont(size=11), padx=8, pady=1,
            ).pack(side="left", padx=(0, 5))
        return box

    def search(self):
        name = self.entry.get().strip()
        self.clear()
        if not name:
            self.status.configure(text="⚠️ Please type a movie title first.", text_color=ORANGE)
            return

        selected, recs = recommend(name, int(self.slider.get()))
        if selected is None:
            self.status.configure(text="😕 No matching movie found. Try another title.",
                                  text_color=ORANGE)
            return

        self.status.configure(text="", text_color=MUTED)

        # Matched movie banner
        banner = ctk.CTkFrame(self.results, fg_color=CARD, corner_radius=16,
                              border_width=2, border_color=PINK)
        banner.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(banner, text="CLOSEST MATCH", text_color=MUTED,
                     font=ctk.CTkFont(size=11)).pack(anchor="w", padx=16, pady=(10, 0))
        ctk.CTkLabel(banner, text=selected["title"],
                     font=ctk.CTkFont("Segoe UI", 18, "bold")).pack(anchor="w", padx=16)
        self.genre_chips(banner, selected["genres"]).pack(anchor="w", padx=16, pady=(4, 12))

        ctk.CTkLabel(self.results, text="🍿 You might also like",
                     font=ctk.CTkFont("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 6))

        for rank, (_, row) in enumerate(recs.iterrows(), start=1):
            card = ctk.CTkFrame(self.results, fg_color=CARD, corner_radius=16)
            card.pack(fill="x", pady=5)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(card, text=str(rank), width=44, height=44, corner_radius=12,
                         fg_color=PINK, font=ctk.CTkFont(size=16, weight="bold")
                         ).grid(row=0, column=0, rowspan=2, padx=14, pady=12)

            ctk.CTkLabel(card, text=row["title"], anchor="w",
                         font=ctk.CTkFont("Segoe UI", 14, "bold")
                         ).grid(row=0, column=1, sticky="w", pady=(10, 0))
            self.genre_chips(card, row["genres"]).grid(row=1, column=1, sticky="w",
                                                       pady=(2, 10))

            pct = int(round(row["score"] * 100))
            side = ctk.CTkFrame(card, fg_color="transparent")
            side.grid(row=0, column=2, rowspan=2, padx=14)
            ctk.CTkLabel(side, text=f"{pct}% match", text_color="#ffd6a5",
                         font=ctk.CTkFont(size=12, weight="bold")).pack()
            bar = ctk.CTkProgressBar(side, width=90, height=7, progress_color=ORANGE,
                                     fg_color="#3a2a55")
            bar.set(row["score"])
            bar.pack(pady=(3, 0))


if __name__ == "__main__":
    CineMatch().mainloop()
