import openai
import json
import torch
from sentence_transformers import SentenceTransformer
import random


def sim_matrix(a, b, eps=1e-8):
    a = torch.from_numpy(a)
    b = torch.from_numpy(b)
    a_n, b_n = a.norm(dim=1)[:, None], b.norm(dim=1)[:, None]
    a_norm = a / torch.max(a_n, eps * torch.ones_like(a_n))
    b_norm = b / torch.max(b_n, eps * torch.ones_like(b_n))
    sim_mt = torch.mm(a_norm, b_norm.transpose(0, 1))
    return sim_mt


def get_knn_samples(train_samples, test_samples, k=5):
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    all_sentences = []
    for sample in test_samples:
        parts = sample.split("\t")
        all_sentences.append(parts[0].replace("_", parts[3]))

    for sample in train_samples:
        parts = sample.split("\t")
        all_sentences.append(parts[0].replace("_", parts[3]))

    embeddings = model.encode(all_sentences)
    similarity_scores = sim_matrix(embeddings[:(len(test_samples))], embeddings[len(test_samples):])

    res, ind = torch.topk(similarity_scores, k, largest=True, dim=1)

    knn_samples = []
    for i, indices in enumerate(ind):
        retrieved_samples = [train_samples[index] for index in indices]
        knn_samples.append(retrieved_samples)

    return knn_samples


def create_prompt(explanation_samples, knn_samples, dev_samples, curr_index):
    prompt = "Let's explain commonsense questions\n"
    for sample in reversed(knn_samples[curr_index]):
        parts = sample.split("\t")
        prompt += "question: " + parts[0] + " What does the \"_\" refer to?\n"
        prompt += parts[1] + ", " + parts[2] + "?\n"
        prompt += parts[3] + "\n"
        prompt += "why? " + parts[5] + "\n"
        prompt += "###" + "\n"

    curr_sample = dev_samples[curr_index].split("\t")
    prompt += "question: " + curr_sample[0] + " What does the \"_\" refer to?\n"
    prompt += curr_sample[1] + ", " + curr_sample[2] + "?\n"
    prompt += curr_sample[3] + "\n"
    prompt += "why?"

    return prompt


if __name__ == '__main__':
    random.seed(42)
    top_k = 5

    openai.api_key = open("path_to_api_key", "r", encoding="utf-8-sig").read().splitlines()[0]
    train_samples = open("path_to_retrieval_pool", "r", encoding="utf-8-sig").read().splitlines()
    test_samples = open("path_to_test_samples", "r", encoding="utf-8-sig").read().splitlines()
    knn_samples = get_knn_samples(train_samples, test_samples, k=top_k)

    output_file = open("path_to_output_file", "w", encoding="utf-8-sig")
    for i in range(len(test_samples)):
        prompt = create_prompt(train_samples, knn_samples, test_samples, i)
        retrieved_samples = [sample.split("\t")[0] for sample in reversed(knn_samples[i])]

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=50,
            top_p=1,
            n=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        output_file.write(response["choices"][0]["text"] + "\t" + "\t".join(retrieved_samples) + "\n")
