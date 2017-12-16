
file = 'test_file'
with open(file, 'a') as fout:
    print>>fout, 'aello'.encode('utf-8')