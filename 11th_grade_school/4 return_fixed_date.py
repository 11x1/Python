import datetime
in_ = input("Kuupaev: ")
print(f""
      f"{in_.split('.')[0]}. "
      f"{datetime.date(month=int(in_.split('.')[1]), year=1, day=1).strftime('%B')} "
      f"{in_.split('.')[2]}"
      )
