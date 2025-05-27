import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_movie_recommendations_for_user(db, user_id, num_recommendations=5):
    from models import Review, Movie

    reviews = db.session.query(Review).all()

    data = pd.DataFrame([
        {'user_id': r.user_id, 'movie_id': r.movie_id, 'rating': r.rating}
        for r in reviews if r.rating > 0
    ])
    
    print("\n--- [DEBUG] Tüm rating verisi ---")
    print(data)

    if data.empty or user_id not in data['user_id'].values:
        print(f"Boş veri ya da kullanıcı {user_id} hiç yorum yapmamış.")
        return []

    rating_matrix = data.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
    print("\n--- [DEBUG] Kullanıcı-Film Matrisi ---")
    print(rating_matrix)

    similarity = cosine_similarity(rating_matrix)
    user_idx = list(rating_matrix.index).index(user_id)
    similarity_scores = list(enumerate(similarity[user_idx]))
    
    print("\n--- [DEBUG] Similarity Scores ---")
    print(similarity_scores)

    similar_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:]
    user_movies = set(data[data['user_id'] == user_id]['movie_id'])

    print(f"\n[DEBUG] Kullanıcının izlediği filmler: {user_movies}")

    recommended = {}

    for sim_user_idx, score in similar_users:
        sim_user_id = rating_matrix.index[sim_user_idx]
        sim_user_movies = data[data['user_id'] == sim_user_id]

        for _, row in sim_user_movies.iterrows():
            if row['movie_id'] not in user_movies:
                if row['movie_id'] not in recommended:
                    recommended[row['movie_id']] = (row['rating'], score)
                else:
                    existing = recommended[row['movie_id']]
                    recommended[row['movie_id']] = (existing[0] + row['rating'], existing[1] + score)

        if len(recommended) >= num_recommendations:
            break

    sorted_recs = sorted(recommended.items(), key=lambda x: (x[1][0] * x[1][1]), reverse=True)
    movie_ids = [int(movie_id) for movie_id, _ in sorted_recs[:num_recommendations]]

    print(f"\n[DEBUG] Önerilen film ID'leri: {movie_ids}")

    movies = db.session.query(Movie).filter(Movie.id.in_(movie_ids)).all()

    print(f"\n[DEBUG] Önerilen film isimleri: {[m.title for m in movies]}")
    return movies
