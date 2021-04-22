def coherence(docs, topics):
    def PMI(i, j, word_occur):
        n_ij = 0
        n_i = 0
        n_j = 0
        for m in range(word_occur.shape[0]):
            i_indexes = word_occur[m, i]
            j_indexes = word_occur[m, j]

            if len(i_indexes):
                n_i += 1

            if len(j_indexes):
                n_j += 1

                # # i_indexes iter
            # first = 0
            # # j_indexes iter
            # second = 0
            # while first != len(i_indexes) and second != len(j_indexes):
            #     if abs(i_indexes[first] - j_indexes[second]) <= 10:
            #         n_ij += 1
            #         break
            #     elif first < second:
            #         first += 1
            #     else:
            #         second += 1

            flag = 0
            for r in i_indexes:
                for t in j_indexes:
                    if abs(r - t) <= 10:
                        n_ij += 1
                        flag = 1
                        break
                if flag:
                    break

        if not n_i or not n_j or not n_ij:
            return 0

        p_ij = n_ij / word_occur.shape[0]
        p_i = n_i / word_occur.shape[0]
        p_j = n_j / word_occur.shape[0]

        _ = np.log((p_ij) / (p_i * p_j))

        return _ if _ > 0 else 0

    coherence_sum = 0.0
    num_topics = len(topics)
    coherences = []
    for q, topic in enumerate(topics):
        top_tokens = topics[q]
        k = len(top_tokens)

        # matrix of indexes evaluation
        word_occur = []
        for doc in docs:
            indexes = [[] for i in range(k)]
            for i, word in enumerate(doc):
                if word in top_tokens:
                    idx = top_tokens.index(word)
                    indexes[idx].append(i)
            word_occur.append(indexes)
        word_occur = np.array(word_occur)

        # coherence evalution for exact topic
        coherence_topic = 0.0
        for i in range(k - 1):
            for j in range(i + 1, k):
                coherence_topic += PMI(i, j, word_occur)

        # coherence_topic *= (2 / (k * (k - 1)))
        coherences.append(coherence_topic)
        coherence_sum += coherence_topic

    print(coherences)
    return coherence_sum / num_topics