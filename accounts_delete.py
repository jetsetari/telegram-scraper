"""
ACCOUNTS : DELETE ACCOUNT
"""
import os
import pickle

#CONFIG
from config.globals import lg, n, w, cy, ye, r, vars_file_path
from config.header import banner

def delete_account():
    """DELETE ACCOUNT"""
    os.system('clear')
    banner()
    print(w+'=== DELETE ACCOUNT'+n)
    accs = []
    with open(vars_file_path, "rb") as f:
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}Choose an account to delete\n')
        for acc in accs:
            print(f'{n}[{ye}{i}{n}] {acc[2]}{n}')
            i += 1

        try:
            index = input(f'\n{cy}Enter your choice: {ye}')
            if not index:
                f.close()
                return
            index = int(index)
            if index < 0 or index >= len(accs):
                raise ValueError("Invalid index")
        except ValueError:
            print(f'{r}Invalid input. No account deleted.')
            return

        phone = str(accs[index][2])
        session_file = phone + '.session'
        os.system(f'rm sessions/{session_file}')
        del accs[index]
        with open(vars_file_path, "wb") as f:
            for account in accs:
                pickle.dump(account, f)
        print(f'\n{ye}[i]{w} Account Deleted')
        input(cy+'\nPress enter to goto main menu')
    f.close()

if __name__ == "__main__":
    delete_account()
