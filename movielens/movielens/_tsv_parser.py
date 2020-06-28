import pandas as pd


def parse():
    u_data = pd.read_csv('u.data.tsv', delimiter='\t', header=None)
    u_genre = pd.read_csv('u.genre.tsv', delimiter='|', header=None)
    u_item = pd.read_csv('u.item.tsv', delimiter='|', header=None, encoding='latin-1')
    u_occupation = pd.read_csv('u.occupation.tsv', delimiter='\t', header=None)
    u_user = pd.read_csv('u.user.tsv', delimiter='|', header=None)
    return u_data, u_genre, u_item, u_occupation, u_user