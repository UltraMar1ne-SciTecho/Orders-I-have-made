import cv2
import numpy as np
import tqdm

MIN_MATCH_COUNT = 10


def get_match_score(query, refs):
    scores = []
    sift = cv2.SIFT_create()

    for ref in tqdm.tqdm(refs):

        kp1, des1 = sift.detectAndCompute(ref, None)
        kp2, des2 = sift.detectAndCompute(query, None)

        index_params = dict(algorithm=0, trees=5)

        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            scores.append(len(matchesMask))
        else:
            scores.append(0)

    return scores


def get_best_matches(scores, threshold):
    if max(scores) < threshold:
        return ['No matches found in these references']
    return [max(scores), scores.index(max(scores))]


def get_best_matches_with_topk(scores, topk):
    indexed_arr = list(enumerate(scores))
    sorted_indexed_arr = sorted(indexed_arr, key=lambda x: x[1], reverse=True)
    sorted_indices = [x[0] for x in sorted_indexed_arr]
    sorted_arr = [x[1] for x in sorted_indexed_arr]

    return sorted_indices[: topk]
