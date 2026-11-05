"""Map, cluster and score every embedding, and report what each one actually groups by."""

from common import ANALYSIS, cards, load_json, save_json

import numpy as np
import umap
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_mutual_info_score, silhouette_score


def merged_field(joined, records, section, field):
    return [joined[r["id"]]["form"][section][field] for r in records]


def mutual_info(clusters, labels):
    return round(float(adjusted_mutual_info_score(clusters, labels)), 3)


def best_kmeans(vectors):
    results = []
    for k in range(4, 25, 2):
        labels = KMeans(k, n_init=10, random_state=0).fit_predict(vectors)
        results.append((silhouette_score(vectors, labels, metric="cosine"), k, labels))
    return max(results, key=lambda r: r[0])


def main():
    records = cards()
    joined = {card["id"]: card for card in load_json(ANALYSIS / "cards.json")}
    set_map = load_json(ANALYSIS / "set_map.json")
    targets = {
        "set": [set_map[r["id"]]["set_index"] for r in records],
        "art_category": merged_field(joined, records, "staging", "art_category"),
        "background": merged_field(joined, records, "staging", "background_type"),
        "object_class": merged_field(joined, records, "identity", "object_class"),
    }

    maps = {}
    for path in sorted((ANALYSIS / "embeddings").glob("*.npy")):
        vectors = np.load(path)
        pca = PCA(min(30, len(vectors) - 1), random_state=0).fit_transform(vectors)
        layout = umap.UMAP(n_neighbors=12, min_dist=0.2, metric="cosine", random_state=0).fit_transform(vectors)
        dense = umap.UMAP(n_components=8, n_neighbors=12, min_dist=0.0, metric="cosine",
                          random_state=0).fit_transform(vectors)
        silhouette, k, kmeans = best_kmeans(pca)
        density = HDBSCAN(min_cluster_size=4).fit_predict(dense)

        similarity = vectors @ vectors.T
        np.fill_diagonal(similarity, -1)
        neighbours = np.argsort(-similarity, axis=1)[:, :8]

        maps[path.stem] = {
            "xy": np.round(layout, 3).tolist(),
            "kmeans": kmeans.tolist(),
            "hdbscan": density.tolist(),
            "neighbours": neighbours.tolist(),
            "scores": {
                "kmeans_k": k,
                "kmeans_silhouette": round(float(silhouette), 3),
                "hdbscan_clusters": int(density.max() + 1),
                "hdbscan_noise": int((density < 0).sum()),
                "kmeans_ami": {name: mutual_info(kmeans, labels) for name, labels in targets.items()},
                "hdbscan_ami": {name: mutual_info(density, labels) for name, labels in targets.items()},
            },
        }
        print(path.stem, maps[path.stem]["scores"], flush=True)
    save_json(ANALYSIS / "embedding_map.json", maps)


if __name__ == "__main__":
    main()
