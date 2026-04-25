import win32clipboard
p = r'c:\Thesis_Hr_system\humanize_chunks_450\batch_1.txt'
with open(p, encoding='utf-8-sig') as f:
    c = f.read()
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardText(c, win32clipboard.CF_UNICODETEXT)
win32clipboard.CloseClipboard()
print('Done')
