#!/usr/bin/env python
# coding: utf-8

u'''
テキストファイルから末尾空白を取り除きます。

使い方:
　　rm_rspace [-d] [-c] [-e ENCODING] FILE [NEWFILE]

引数:
  FILE                  末尾空白を削除したいテキストファイルのパス
  NEWFILE               処理後の保存先パス

オプション:
  -h, --help            ヘルプメッセージを表示して終了
  -d, --display         末尾空白があった行とその行番号を表示
  -c, --count           末尾空白を取り除いた行の数を表示
  -e ENCODING, --encoding ENCODING
                        指定したエンコーディングでファイルを開く。省略した場合は UTF-8 で開く

Copyright (c) 2018 Masashi Takahashi
License: MIT
'''

__author__ = 'Masashi Takahashi'
__version__ = '0.0.1'
__license__ = 'MIT'

import codecs

def rm_rspace(file, newfile=None, encoding='utf-8'):
    u'''file のパスが示すテキストファイルから、行末の空白を取り除きます。
    対象とするファイルのエンコーディングが UTF-8 でなければ、encoding に指定してください。
    newfile のパスに処理後のテキストを保存します。 newfile の指定がなければ元のファイルに上書きします。

    この関数は返り値として、末尾空白があった行の詳細をリストで返します。

    '''

    # Python2系はopen関数にエンコーディングを指定できないので、代わりにcodecs.open関数を使用
    with codecs.open(file, 'r', encoding) as fr:
        lines = fr.readlines()

    line_number = 0
    newlines = []
    rstripped_log = []
    for line in lines:
        line_number += 1
        lnsep = ''
        # 改行コードの判定
        if line[-2:] == '\r\n':    # Windows
            lnsep = '\r\n'
        elif line[-1:] == '\n':    # Unix系
            lnsep = '\n'
        elif line[-1:] == '\r':    # 古いMac OS（バージョン9以前）
            lnsep = '\r'
        rstripped_line = line.rstrip()
        newlines.append(rstripped_line + lnsep)

        lnsep_width = len(lnsep)
        diff = len(line) - (len(rstripped_line) + lnsep_width)
        if diff:
            space_start = -(diff + lnsep_width)
            space_stop = len(line) - lnsep_width
            rstripped_log.append((
                line_number,                     # 行番号（int型）
                rstripped_line,                  # 末尾空白と改行文字を取り除いた行
                line[space_start:space_stop],    # 末尾空白
                lnsep                            # 改行文字
            ))

    newfile = newfile or file
    with codecs.open(newfile, 'w', encoding) as fw:
        fw.write(''.join(newlines))

    return rstripped_log

def main():
    import argparse
    import os
    import sys
    import traceback

    py_major_ver = sys.version_info[0]
    if py_major_ver == 2:
        # encodingを標準入力(sys.stdin)から取得しているのは、
        # 出力リダイレクトをしたとき標準入力(sys.stdout)のencodingがNoneになるから。
        # 上記はPython2で確認。Python3では問題なし。
        system_encoding = sys.stdin.encoding
        # Python2のリダイレクトエラーとUnicode文字列の文字化け対処
        sys.stdout = codecs.getwriter(system_encoding)(sys.stdout)

    parser = argparse.ArgumentParser(
        prog='rm_rspace',
        usage='rm_rspace.py [-d] [-c] [-e ENCODING] FILE [NEWFILE]',
        description=u'テキストから末尾空白を取り除きます',
        add_help=True
    )
    parser.add_argument(
        'file', metavar='FILE',
        help=u'末尾空白を削除したいテキストファイルのパス'
    )
    parser.add_argument(
        'newfile', metavar='NEWFILE',
        default=None,
        nargs='?',
        help=u'処理後の保存先パス'
    )
    parser.add_argument(
        '-d', '--display',
        action='store_true',
        help=u'末尾空白があった行とその行番号を表示'
    )
    parser.add_argument(
        '-c', '--count',
        action='store_true',
        help=u'末尾空白を取り除いた行の数を表示'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help=u'指定したエンコーディングでファイルを開く。省略した場合は UTF-8 で開く'
    )
    args = parser.parse_args()
    try:
        log = rm_rspace(args.file, args.newfile, args.encoding)
    except:
        # トレースバック文字列から最後の行を取得（下から2行目）
        error_message = traceback.format_exc().split('\n')[-2]
        sys.stderr.write('rm_rspace: ' + error_message + '\n')
        exit(1)

    nlog = len(log)
    after_nlsep = ''
    # Unix環境のターミナルの場合は、一部色を付けて表示
    if os.name == 'posix' and sys.stdout.isatty():
        GREEN, CYAN, COLOR_END = '\033[32m', '\033[36m', '\033[0m'
    else:
        GREEN, CYAN, COLOR_END = '', '', ''

    # オプション -d が付いていた場合
    if args.display and nlog:
        num_width = len(str(log[-1][0]))
        res = '\n'.join(
            [str(n).rjust(num_width) + ' ' + l + (GREEN +  '*' * len(s) + COLOR_END)
             for n, l, s, _ in log]
        )
        sys.stdout.write(res + '\n')
        after_nlsep = '\n'

    # オプション -c が付いていた場合
    if args.count:
        sys.stdout.write(after_nlsep + CYAN + str(nlog) + COLOR_END +
                         u' 行の末尾空白を取り除きました\n')

if __name__ == '__main__':
    main()
