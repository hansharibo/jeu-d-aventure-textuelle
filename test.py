import fonctionutile as fu
# fichier teste de la fonction Jukebox et des différente musique
if __name__ == '__main__':
    musique2 = 'test.mp3'
    print(musique2)
    p= 0
    p = fu.jukebox('start', p , musique2)
    input('enter to stop this madness')
    p = fu.jukebox('stop',  p)
