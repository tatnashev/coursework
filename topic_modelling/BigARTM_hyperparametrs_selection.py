import operator


class model_param():
    def __init__(self, tau_sparse, tau_decorr, tau_smooth, author_weight, num_passes, perplexity, phi_sparsity):
        self.tau_sparse = tau_sparse
        self.tau_decorr = tau_decorr
        self.tau_smooth = tau_smooth
        self.author_weight = author_weight
        self.num_passes = num_passes
        self.perplexity = perplexity
        self.phi_sparsity = phi_sparsity


sparse = np.arange(-1, 0, 0.1)
decorr = [0.3]
smooth = np.arange(0, 1, 0.1)
weight = [7]
passes = [7]

model = artm.ARTM(num_topics=15,
                      class_ids={'@default_class': 1.0, 'author': 7.0},
                      dictionary = batch_vectorizer_authors.dictionary,
                      num_document_passes=5)

model.scores.add(artm.TopTokensScore(name='TopTokensScore', num_tokens=7))
model.scores.add(artm.PerplexityScore(name='perplexity', dictionary=batch_vectorizer_authors.dictionary))
model.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore'))

model.regularizers.add(artm.SmoothSparsePhiRegularizer(name='sparse_phi_def', tau=-0.4, class_ids=['@default_class']))
model.regularizers.add(artm.DecorrelatorPhiRegularizer(name='decorrelator_phi_def',
                                                       class_ids=['@default_class'], tau=0.3))

model.regularizers.add(artm.SmoothSparsePhiRegularizer(name='smooth_phi_author',
                                                       class_ids=['author'], tau=0.3))


# perplexity_values = []
# phi_sparsity = []
model_parametrs = []

with open('topics_and_tokens.txt', 'w') as f:
    for num_pass in tqdm(passes):
        model.num_document_passes = num_pass
        f.write('Num document passes is {}\n'.format(num_pass))
        f.write('#########################################\n')
        for w in tqdm(weight):
            model.class_ids = {'@default_class': 1.0, 'author': w}
            f.write('Author weight is {}\n'.format(w))
            f.write('===============================\n')
            for tau_sparse in tqdm(sparse):
                model.regularizers['sparse_phi_def'].tau = tau_sparse
                f.write('Tau sparse is {}\n'.format(tau_sparse))
                f.write('--------------------------------\n')
                for tau_decorr in tqdm(decorr):
                    model.regularizers['decorrelator_phi_def'].tau = tau_decorr
                    f.write('Tau decorr is {}\n'.format(tau_decorr))
                    f.write('*************************************\n')
                    for tau_smooth in tqdm(smooth):
                        f.write('Tau smooth is {}\n'.format(tau_smooth))
                        f.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
                        model.regularizers['smooth_phi_author'].tau = tau_smooth

                        model.fit_offline(batch_vectorizer=batch_vectorizer_authors,
                                    num_collection_passes=20)

                        perplexity = model.score_tracker['perplexity'].last_value
                        phi_sparsity = model.score_tracker['SparsityPhiScore'].last_value

                        model_parametrs.append(model_param(tau_sparse, tau_decorr,
                                                           tau_smooth, w,
                                                           num_pass, perplexity, phi_sparsity))

                        f.write('Last perplexity: {}\n'.format(model.score_tracker['perplexity'].last_value))
                        f.write('Sparsity Phi {}\n'.format(model.score_tracker['SparsityPhiScore'].last_value))

                        for topic in model.topic_names:
                            f.write(str(topic) + ': ' +  ' '.join(model.score_tracker['TopTokensScore'].last_tokens[topic]))
                            f.write('\n')
                        f.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')

                    f.write('*************************************\n')

                f.write('--------------------------------\n')
                f.write('\n')
            f.write('===============================\n')
        f.write('#########################################\n')


model_parametrs.sort(key=operator.attrgetter('perplexity'))
with open('best_parametrs.txt', 'w') as f:
    for elem in model_parametrs[:50]:
        f.write('tau_sparse is: {}\n'.format(elem.tau_sparse))
        f.write('tau_decorr is: {}\n'.format(elem.tau_decorr))
        f.write('tau_smooth is: {}\n'.format(elem.tau_smooth))
        f.write('author_weight is: {}\n'.format(elem.author_weight))
        f.write('num_passes is: {}\n'.format(elem.num_passes))
        f.write('perplexity is: {}\n'.format(elem.perplexity))
        f.write('phi_sparsity is: {}\n'.format(elem.phi_sparsity))
        f.write('---------------------------------------------\n')