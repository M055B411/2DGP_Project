

wave1 = ['goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin', 'goblin']
wave2 = ['wolf', 'goblin', 'wolf', 'goblin', 'goblin', 'wolf', 'goblin', 'goblin', 'wolf', 'goblin', 'goblin', 'wolf', 'wolf', 'goblin', 'goblin', 'goblin']
wave3 = ['wolf', 'goblin', 'wolf', 'goblin', 'goblin', 'robot', 'wolf', 'goblin', 'goblin', 'wolf', 'goblin', 'robot', 'goblin', 'wolf', 'wolf', 'goblin', 'goblin', 'goblin', 'robot']
wave4 = ['wolf', 'goblin', 'wolf', 'goblin', 'goblin', 'robot', 'wolf', 'goblin', 'goblin', 'golem', 'wolf', 'goblin', 'robot', 'goblin', 'wolf', 'wolf', 'goblin', 'goblin', 'goblin', 'robot','golem', 'golem']

wave_list = [wave1, wave2, wave3, wave4]

def Monsterspawn(number):
        for monster in wave_list[number]:
            yield monster