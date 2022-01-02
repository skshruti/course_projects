All the bash scripts required are in the directory. 

The specifications are adhered by and the sample commands to run are given below:
bash rocchio_rerank.sh ../col764-ass2-release/covid19-topics.xml ../col764-ass2-release/t40-top-100.txt ../colldir ../outfiles/rocchio.out
bash lm_rerank.sh rm1 ../col764-ass2-release/covid19-topics.xml ../col764-ass2-release/t40-top-100.txt ../colldir ../outfiles/lm.out ../outfiles/exp.out
bash lm_rerank.sh rm2 ../col764-ass2-release/covid19-topics.xml ../col764-ass2-release/t40-top-100.txt ../colldir ../outfiles/lm.out ../outfiles/exp.out

Set evaluate to 1 and provide the qrels file in the beginning of the code if the evaluator wants to generate ndcg, mrr and map scores.

Rocchio:
=>Optimised query is formed using original query and the top 100 relevant documents for the query. 
=>The similarity of this optimised query is calculated with each each of the top 100 relevant documents. 
=>The documents are then ranked by their similarity score and the ranked documents are returned. 

LM:
=>All the probabilities are calculated using Dirichlet smoothening.
=>Query likelihood score is calculated for each query.
=>P(w,q1..qk) is then calculated depending on the argument rm1 or rm2.
=>Top 20 words are selected from the vocabulary having the highest P(w,q1..qk).
=>KL divergence score is then calculated using the above results for top 20 words.
=>Documents are reranked according to this KL divergence score.