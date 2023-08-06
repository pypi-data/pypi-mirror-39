import yo

def make():
    return yo.Query().get().sum()

if __name__ == '__main__':
    print(make())