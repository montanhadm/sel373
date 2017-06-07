import sqlite3 as sql
import random

# TEST ACCOUNTS:
#	Mario	mario123	4p - float values
#	Luigi	luigi123	3p
#	Yoshi	yoshi123	2p
#	Toad	toad123		7p
#	Shyguy	shyguy123	1p
#	Peach	peach123	4p

# Parâmetros Iniciais

user = "Luigi"
num_pessoas = 3
local_waste = random.randint(0, 450000)
bath_h = [0, 6, 7, 8, 9, 18, 19, 20, 21, 22, 23]
wash_h = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
leak_chance = [0.5, 0.25, 0.1, 0.01]
leak_fixchance = [20, 20, 20, 30]
leak_ratio = [10, 20, 30, 200]
is_leak = [0, 0, 0, 0]
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
years = [2015, 2016, 2017]
bath_waste = 35
bath_waste_range = 15
wash_waste = 50
wash_waste_range = 15
other_waste = 140 * num_pessoas / 100
other_waste_range = 40 * num_pessoas / 100
other_normal_waste = [2.46, 0, 0, 0, 0, 0, 1.23, 1.85, 2.46, 8.61, 5.54, 8.61, 8.61, 9.84, 8.61, 2.46, 2.46, 9.84, 6.15, 7.38, 3.08, 4.31, 2.21, 3.69]

# Hábitos

random.seed()

bath_times = []
for i in range(num_pessoas):
	bath_times.append(random.choice(bath_h))

wash_ratio = (int)(4.5*((num_pessoas/2) + random.randint(-1,1)) + 0.5)

# Simulação

with sql.connect("database/winput.db") as con:
	cur = con.cursor()

for year in years:

	if year == 2016:
		month_days[1] = 29
	else:
		month_days[1] = 28



	for month in range( 5 if year == 2017 else 12):

		days = month_days[month]

		# dias para lavar roupa
		step = (int)((days / wash_ratio) + 0.5)
		initial_day = random.randint(1,step)

		for day in range(days):

			if (day + 1 - initial_day) % step == 0:
				wash_hour = random.choice(wash_h)
			
			data = "{}-{}-{}".format(year, str(month+1).zfill(2), str(day+1).zfill(2))
			
			for hour in range(24):

				#lava roupa
				if (day + 1 - initial_day) % step == 0 and hour == wash_hour:
					local_waste += wash_waste + random.randint(-100,100)*wash_waste_range/100

				#banho
				if hour in bath_times:
					local_waste += bath_waste + random.randint(-100,100)*bath_waste_range/100

				#other
				local_waste += other_normal_waste[hour]*(other_waste + random.randint(-100,100)*other_waste_range/100)

				#vazamentos
				for i in range(4):
					local_waste += is_leak[i]*leak_ratio[i]/24

					if is_leak[i] > 0 and hour > 8 and hour < 20 and random.randrange(0, 100, 1) < leak_fixchance[i]:
						is_leak[i] -= 1
						print("VAZAMENTO ARRUMADO\n")


					if random.randrange(0, 10000, 1)/100 < leak_chance[i]:
						is_leak[i] += 1
						print("VAZOU\n")

				hora = "{}:00".format(str(hour).zfill(2))

				local_waste = int(local_waste)

				cur.execute("""INSERT INTO leituras (DATA, HORA, VALOR, USER) VALUES (?,?,?,?)""", (data, hora, local_waste, user))
				con.commit()

con.close()


