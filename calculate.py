import csv
import random
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEIGHTS = {'C1_raw':25,'C2_raw':20,'C3_raw':15,'C4_raw':10,'C5_raw':15,'C6_raw':10,'C7_raw':5}
TIE = ['C1_raw','C2_raw','C5_raw','C6_raw']

with open(ROOT/'SCORE_MATRIX.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

def calc(row, weights=WEIGHTS):
    value = sum(Decimal(row[k]) / Decimal(10) * Decimal(str(weights[k])) for k in WEIGHTS)
    return value.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

for row in rows:
    actual = calc(row)
    assert actual == Decimal(row['score']), (row['participant'], actual, row['score'])

def rank_key(row):
    return (-float(row['score']),) + tuple(-int(row[k]) for k in TIE) + (row['participant'],)

ranked = sorted(rows, key=rank_key)
assert ranked[0]['participant'] == 'Спортивное ориентирование'
assert ranked[1]['participant'] == 'Шахматы'

rng = random.Random(42)
ori_first = chess_second = athletics_third = ski_third = 0

for _ in range(50000):
    w = {k: WEIGHTS[k] * rng.uniform(0.8,1.2) for k in WEIGHTS}
    total = sum(w.values())
    w = {k: v*100/total for k,v in w.items()}

    scored = []
    for row in rows:
        value = sum((int(row[k])/10)*w[k] for k in WEIGHTS)
        scored.append((value,row))

    scored.sort(key=lambda t:(-t[0],) + tuple(-int(t[1][k]) for k in TIE) + (t[1]['participant'],))
    order = [x[1]['participant'] for x in scored]

    if order[0] == 'Спортивное ориентирование':
        ori_first += 1
    if order[1] == 'Шахматы':
        chess_second += 1
    if order[2] == 'Легкая атлетика':
        athletics_third += 1
    if order[2] == 'Лыжные гонки':
        ski_third += 1

print('OK: raw matrix and weighted totals verified')
print('Спортивное ориентирование first:', ori_first, 'of 50000')
print('Шахматы second:', chess_second, 'of 50000')
print('Легкая атлетика third:', athletics_third)
print('Лыжные гонки third:', ski_third)
