#!/usr/bin/env python3
## Encryption stuff.

def decodePadDungeon(e):
    return NotImplementedError("Secret info, do not share.")

def encodePadDungeon(p: str, key: int):
    return NotImplementedError("Secret info, do not share.")


def _test():
    e = ciphertext = '237AAVk4N8yyeAYcdLQRkbVqdpXXlVaxmD82C67ygAafKcmhCTohmmnRJWupMhJ1S7Ew6CD2Y5xI4HYN6nUTSSTg3mR.oO6xmD86C67zlI68L8nhCTolmmnMx,lhZrI1S7EA6CDdX4xx0EMN6nUXSSTi1qWXuR4xmD8aC67BpG4aFaIJy,njmmnMFTiiNiL1S7EyVrFaM7Iy7CS0WjMZ9T4k1hM,mT0nnv45m49pvA5by1sBCPEhKrrPiWjuSsGUZ9xtWzA6VTJCfwO7cmWVSTYpdv0UtU3qlE38rX8x0,M8J7nAyUqnE'

    # plaintext from the JS version.
    p = plaintext = 'ss=1c9e9e39&s=1050548&e1=5cd44e14&e2=213020cf&e3=50cf746e&e4=7ffb58f4&e5=49583f55&e6=7d6bad6e&e7=a7dfa052&e8=5d340e86&e9=253a197&e10=75ec91fd&e11=ce297b4f&e12=8e46a283&e13=b02cea22&e14=56187987&e15=fd0887ca&e16=515195b3&sm=a5b69c40'

    assert decodePadDungeon(ciphertext) == plaintext
    assert ciphertext == encodePadDungeon(plaintext, 0x23)


def main():
    _test()


if __name__ == '__main__':
    try:
        main()
    except:
        import sys
        print("Args:", sys.argv)
        print()
        
        import atexit
        atexit.register(input, "Press Enter to continue...")
        raise
    


