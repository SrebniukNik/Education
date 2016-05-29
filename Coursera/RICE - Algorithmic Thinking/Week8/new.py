new_x = 'MQN--------------------------------------S--------------HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ'
new_y = 'MRNLPCLGTAGGSGLGGIAGKPSPTMEAVEASTASHPHSTSSYFATTYYHLTDDECHSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
max_x = max(new_x.split('-'), key=lambda x: len(x))
max_y = max(new_y.split('-'), key=lambda x: len(x))
print max_x, max_y
if new_y.count('-') > new_x.count('-'):
    max_y, max_x = max_x, max_y

idx = new_x.find(max_x)
align_new_x = new_x[idx:idx + len(max_x)]
align_new_y = new_y[idx:idx + len(max_x)]
print align_new_x + "\n",
print align_new_y



# index = []
# pos1, pos2 = None
# flag = False
# for letter in range(len(string1) -1):
#     if string1[letter] !='-' and not flag:
#         pos1 = letter
#         flag = True
#     if string1[letter + 1] == '-' and flag:





