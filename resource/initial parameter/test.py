# f=file('test_cmd.txt', 'r')
# liens = f.readlines()
# f.close()
# st = 'CONF:VOLT:DC'
# trecord = ''
# for i in range(len(liens)):
    # if liens[i][:len(st)] == st:
        # print 'in', trecord, liens[i]
        # if trecord != liens[i]:
            # open('test_cmd1.txt', 'a').write(liens[i])
            # trecord = liens[i]
        else:
    # else:
        # open('test_cmd1.txt', 'a').write(liens[i])
f=file('test_cmd1.txt', 'r')
liens = f.readlines()
f.close()
st = 'CONF:VOLT:DC'
trecord = ''
for i in range(len(liens)):
    if liens[i][:len(st)] == st:
        print 'in', trecord, liens[i]
        if trecord != liens[i]:
            open('test_cmd2.txt', 'a').write(liens[i])
            trecord = liens[i]
        # else:
    else:
        open('test_cmd2.txt', 'a').write(liens[i])
