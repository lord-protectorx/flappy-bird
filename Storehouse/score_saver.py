import os
# прописал чтобы не ругалось, вместо int(), тут должно быть значение реальное


def save_res(score):
    files = os.listdir("../data")
    if 'best_score.txt' in files:
        file = open('../data/best_score.txt', 'r', encoding="utf-8")
        best_score = file.read()
        if score > int(best_score):
            best_score = str(score)
        file.close()
        file = open('../data/best_score.txt', 'w', encoding="utf-8")
        file.write(str(best_score))
        file.close()
    else:
        file = open('../data/best_score.txt', 'w', encoding="utf-8")
        file.write(str(score))
        file.close()
