s=open('gen_e.py',encoding='utf-8').read()
a='''    body = "\n".join([
        f'<div class="sky">{mast}',
        '<main>','''
print(repr(a)); print(s.count(a))
