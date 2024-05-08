import pandas as pd

def cetak_df(df):
    df = pd.DataFrame(df)
    df['id'] = df.index
    kolom = df.columns.tolist()
    kolom.insert(0, kolom.pop())
    df = df[kolom]

    cetak = df.to_string(index=False)
    cetak = cetak.split('\n')

    for i in range(len(cetak)):
        cetak[i] = list(cetak[i])

    pemisah = []
    for i in range(len(cetak[0]) - 1):
        if cetak[0][i] != ' ' and cetak[0][i + 1] == ' ':
            pemisah.append(i + 1)

    pembatas = '╔'
    for i in range(len(cetak[0])):
        if i in pemisah:
            pembatas += '╦═'
        else:
            pembatas += '═'
    pembatas += '╗'

    pembatas_atas = pembatas
    pembatas_tengah = pembatas.replace('╔', '╠').replace('╦', '╬').replace('╗', '╣')
    pembatas_bawah = pembatas.replace('╔', '╚').replace('╦', '╩').replace('╗', '╝')

    print(pembatas_atas)
    awal = True
    for i in cetak:
        if awal:
            awal = False
        else:
            print(pembatas_tengah)

        for j in pemisah[::-1]:
            i.insert(j, '║')
        print('║' + ''.join(i) + '║')
    print(pembatas_bawah)

df = pd.read_csv('anggota.csv')
cetak_df(df)