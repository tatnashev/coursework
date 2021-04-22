import operator


num_topics = np.arange(10, 25, 3)
# chunksizes = [300, 500, 700, 1000, 1500, 2000]
num_passes = [20, 30, 50, 70, 100, 200]
coherences = []

for passes in num_passes:
    coh = []
    perp = []
    for num_topic in num_topics:
        lda = LdaModel(corpus, num_topics=num_topic, id2word = dictionary, chunksize=500, passes=passes, iterations=100)
        cm = gensim.models.coherencemodel.CoherenceModel(model=lda, corpus=corpus, texts=texts, dictionary=dictionary, coherence='c_v')
        coh.append(cm.get_coherence())

        _ = Topic()
        _.topics = lda.show_topics(num_topics=num_topic)
        _.passes = passes
        _.num_topics = num_topic
        _.coherence = cm.get_coherence()

        results.append(_)

    coherences.append(coh)

with open('results_coherence.txt', 'w+') as coher:
    top_results_coherence = sorted(results, key=lambda x: x.coherence, reverse=True)[:70]

    for _ in top_results_coherence:
        coher.write('Coherence value: {}\n'.format(_.coherence))
        coher.write('Passes: {}\n'.format(_.passes))
        coher.write('Num Topics: {}\n'.format(_.num_topics))
        coher.write('Topics:\n')
        for topic in _.topics:
            coher.write(str(topic))
            coher.write('\n')
        coher.write('\n\n')