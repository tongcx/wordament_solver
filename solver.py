def build_tree():
    ret = {}

    def add_word(word):
        u = ret
        for c in word:
            if c not in u:
                u[c] = {}
            u = u[c]
        u['flag'] = True

    for word in open('wordsEn.txt'):
        word = word.strip().upper()
        if len(word) >= 3:
            add_word(word)

    return ret

def solve(board, tree):
    n = len(board)
    m = len(board[0])

    ret = {}
    used = [[False] * m for i in range(n)]
    chars = []
    answers = [['-'] * m for i in range(n)]

    def search(i, j, u, depth):
        if i < 0 or i >= n or j < 0 or j >= m or used[i][j]:
            return

        def advance(u, cs):
            for c in cs:
                if c not in u:
                    return None
                u = u[c]
            return u

        if board[i][j].endswith('-'):
            if u != tree:
                return

        u = advance(u, board[i][j].strip('-'))
        if u == None:
            return

        used[i][j] = True
        chars.append(board[i][j].strip('-'))
        answers[i][j] = str(depth)
        if 'flag' in u:
            word = ''.join(chars)
            seq = '\n\n'.join(' '.join(row) for row in answers)
            ret[word] = seq

        if not board[i][j].startswith('-'):
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di != 0 or dj != 0:
                        search(i+di, j+dj, u, depth+1)

        answers[i][j] = '-'
        chars.pop()
        used[i][j] = False

    for i in range(4):
        for j in range(4):
            search(i,j, tree, 0)

    return ret

def read_board():
    ret = []
    for line in open('board.txt'):
        cell = []
        buf = []
        brace = False
        for c in line.strip():
            if c == '(':
                brace = True
            elif c == ')':
                cell.append(''.join(buf))
                brace = False
                buf = []
            else:
                if not brace:
                    cell.append(c)
                else:
                    buf.append(c)
        ret.append(cell)
    return ret

def output(answer):
    for row in sorted(answer.items(), key=lambda x: len(x[0]))[::-1]:
        print(row[0])
        print(row[1])
        print()
        input()


tree = build_tree()
board = read_board()
answer = solve(board, tree)
output(answer)
