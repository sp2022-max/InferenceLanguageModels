import numpy as np
import pandas as pd


num2word = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    21: "twenty-one",
    22: "twenty-two",
    23: "twenty-three",
    24: "twenty-four",
    25: "twenty-five",
    26: "twenty-six",
    27: "twenty-seven",
    28: "twenty-eight",
    29: "twenty-nine",
    30: "thirty"}

num2word_pt = {
    1: "um",
    2: "dois",
    3: "três",
    4: "quatro",
    5: "cinco",
    6: "seis",
    7: "sete",
    8: "oito",
    9: "nove",
    10: "dez",
    11: "onze",
    12: "doze",
    13: "treze",
    14: "catorze",
    15: "quinze",
    16: "dezesseis",
    17: "dezessete",
    18: "dezoito",
    19: "dezenove",
    20: "vinte",
    21: "vinte e um",
    22: "vinte e dois",
    23: "vinte e três",
    24: "vinte e quatro",
    25: "vinte e cinco",
    26: "vinte e seis",
    27: "vinte e sete",
    28: "vinte e oito",
    29: "vinte e nove",
    30: "trinta"}


def rem_definite_article(str_):
    str_ = str_.split(" ")
    if len(str_) == 2:
        return str_[1]
    else:
        return str_[0]


def Rt(x, y):
    return "{} is taller than {}".format(x, y)


def Rt_pt(x, y):
    return "{} é mais alto que {}".format(x, y)


def Rt_eq(x, y):
    return "{} is as tall as {}".format(x, y)


def Rt_eq_pt(x, y):
    return "{} é tão alto quanto {}".format(x, y)


def vi(x, y):
    return "{} has visited {}".format(x, y)


def vi_pt(x, y):
    return "{} visitou {}".format(x, y)


def not_vi(x, y):
    return "{} didn't visit {}".format(x, y)


def not_vi_pt(x, y):
    return "{} não visitou {}".format(x, y)


def vi_Sn(x, y):
    if len(x) == 1:
        S = x[0]
    else:
        S = list2coordination(x)
    return "{} have visited {}".format(S, y)


def vi_On(x, y):
    if len(y) == 1:
        S = y[0]
    else:
        S = list2coordination(y)
    return "{} has visited {}".format(x, S)


def vi_Sn_pt(x, y):
    if len(x) == 1:
        S = x[0]
    else:
        S = list2coordination(x, and_str="e")
    return "{} visitaram {}".format(S, y)


def vi_On_pt(x, y):
    if len(y) == 1:
        S = y[0]
    else:
        S = list2coordination(y, and_str="e")
    return "{} visitou {}".format(x, S)


def person(x, rest_f):
    return rest_f("{} is the person that".format(x))


def person_pt(x, rest_f):
    return rest_f("{} é a pessoa que".format(x))


def list2coordination(x, and_str="and"):
    assert len(x) > 1
    if len(x) == 2:
        S = "{} {} {}".format(x[0], and_str, x[1])
    else:
        carS = x[:-1]
        cdrS = x[-1]
        S = ", ".join(carS) + " {} {}".format(and_str, cdrS)
    return S


def get_new_item(item_list, src_list):
    size = len(src_list)
    new_item = src_list[np.random.choice(size)]
    while new_item in item_list:
        new_i = np.random.choice(size)
        new_item = src_list[new_i]
    return new_item


def get_n_different_items(item_list, n):
    new = []
    for _ in range(n):
        new.append(get_new_item(new, item_list))
    return new


NLIdict = {"contradiction": 0,
           "entailment": 1,
           "neutral": 2}

NLI2CD = {"entailment": 0,
          "neutral": 0,
          "contradiction": 1}


NLI2RTE = {"entailment": 1,
           "neutral": 0,
           "contradiction": 0}


def create_csv_binary(out_path,
                      size,
                      positive_instances_list,
                      negative_instances_list,
                      person_list,
                      place_list,
                      n,
                      min_n,
                      NLI2dict):

    sentence1 = []
    sentence2 = []
    label = []
    subjects = []
    objects = []
    ids = []
    people = []
    places = []

    positive_examples = int(size / 2)
    negative_examples = int(size / 2)
    positives_len = len(positive_instances_list)
    negatives_len = len(negative_instances_list)
    positives = [int(positive_examples / positives_len) for _ in positive_instances_list]  # noqa
    negatives = [int(negative_examples / negatives_len) for _ in negative_instances_list]  # noqa

    for i, f in zip(positives, positive_instances_list):
        for _ in range(i):
            current_n = np.random.choice(range(min_n, n + 1))
            s1, s2, l, s, o, i, pe, pl = f(person_list, place_list, current_n)  # noqa
            sentence1.append(s1)
            sentence2.append(s2)
            label.append(l)
            subjects.append(s)
            objects.append(o)
            ids.append(i)
            people.append(pe)
            places.append(pl)

    for i, f in zip(positives, negative_instances_list):
        for _ in range(i):
            current_n = np.random.choice(range(min_n, n + 1))
            s1, s2, l, s, o, i, pe, pl = f(person_list, place_list, current_n)  # noqa
            sentence1.append(s1)
            sentence2.append(s2)
            label.append(l)
            subjects.append(s)
            objects.append(o)
            ids.append(i)
            people.append(pe)
            places.append(pl)

    label = list(map(lambda x: NLI2dict[x], label))

    df = pd.DataFrame({"sentence1": sentence1,
                       "sentence2": sentence2,
                       "label": label,
                       "subjects": subjects,
                       "objects": objects,
                       "ids": ids,
                       "people": people,
                       "places": places})
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(out_path, header=True, index=False)


def create_csv_contradiction(out_path,
                             size,
                             positive_instances_list,
                             negative_instances_list,
                             person_list,
                             place_list,
                             n,
                             min_n):

    create_csv_binary(out_path=out_path,
                      size=size,
                      positive_instances_list=positive_instances_list,
                      negative_instances_list=negative_instances_list,
                      person_list=person_list,
                      place_list=place_list,
                      n=n,
                      min_n=min_n,
                      NLI2dict=NLI2CD)


def create_csv_entailment(out_path,
                          size,
                          positive_instances_list,
                          negative_instances_list,
                          person_list,
                          place_list,
                          n,
                          min_n):

    create_csv_binary(out_path=out_path,
                      size=size,
                      positive_instances_list=positive_instances_list,
                      negative_instances_list=negative_instances_list,
                      person_list=person_list,
                      place_list=place_list,
                      n=n,
                      min_n=min_n,
                      NLI2dict=NLI2RTE)


def create_csv_NLI(out_path,
                   size,
                   entailment_instances_list,
                   neutral_instances_list,
                   contradiction_instances_list,
                   person_list,
                   place_list,
                   n,
                   min_n):

    sentence1 = []
    sentence2 = []
    label = []
    subjects = []
    objects = []
    ids = []
    people = []
    places = []

    entailment_examples = int(size / 3)
    neutral_examples = int(size / 3)
    contradiction_examples = int(size / 3)

    entailment_len = len(entailment_instances_list)
    neutral_len = len(neutral_instances_list)
    contradiction_len = len(contradiction_instances_list)

    entailments = [int(entailment_examples / entailment_len) for _ in entailment_instances_list]  # noqa
    neutrals = [int(neutral_examples / neutral_len) for _ in neutral_instances_list]  # noqa
    contradictions = [int(contradiction_examples / contradiction_len) for _ in contradiction_instances_list]  # noqa

    tuples = [(entailments, entailment_instances_list),
              (neutrals, neutral_instances_list),
              (contradictions, contradiction_instances_list)]

    for tuple_ in tuples:
        for i, f in zip(tuple_[0], tuple_[1]):
            for _ in range(i):
                current_n = np.random.choice(range(min_n, n + 1))
                s1, s2, l, s, o, i, pe, pl = f(person_list, place_list, current_n)  # noqa
                sentence1.append(s1)
                sentence2.append(s2)
                label.append(l)
                subjects.append(s)
                objects.append(o)
                ids.append(i)
                people.append(pe)
                places.append(pl)

    label = list(map(lambda x: NLIdict[x], label))

    df = pd.DataFrame({"sentence1": sentence1,
                       "sentence2": sentence2,
                       "label": label,
                       "subjects": subjects,
                       "objects": objects,
                       "ids": ids,
                       "people": people,
                       "places": places})
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(out_path, header=True, index=False)
