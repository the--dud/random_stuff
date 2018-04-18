import csv, os, subprocess, sys, time

def sleepexit():
	time.sleep(3)
	sys.exit()

def parsematches(matches):
	print("\nSøketreff:\nSkriv '0' for å starte på nytt! Ctrl+C for å avslutte!")
	if len(matches) is 0:
		print("Ingen treff! Starter på nytt...")
		return False
	if len(matches) < 25:
		print("\nID".ljust(9) + " - " + "Åpnet Av".center(17) + " - Sti")
		for m in matches:
			print(m['ID'].ljust(9) + " - " + m['opened_by'].center(17) + " - " + m['path'])
		return True
	else:
		print("Mer enn 25 treff - vær mer spesifikk. Starter på nytt......")
		return False

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
	matches = []
	openfiles_p = r"C:\Windows\SysNative\openfiles.exe" # Path to openfiles.exe
	csv_p = r".\openfiles_tmp.csv" # Path to a temp file which will be created by the script. User running script needs read/write access.
	fp = os.path.normpath(csv_p)
	killid = 999999999
	closedfiles = ""
	pmret = False

	cls()
	print("INSTRUKSJONER:\n" + "\
	  Dette programmet kan brukes til å søke i alle åpne filer på en bestemt server - \n\
	  for så å velge hvilke filer man vil lukke.\n\
	  Søket er IKKE 'case sensitiv'. Det søkes i både brukernavn og sti. Maks treff er 25.\n\n")

	match = str(input("Hva leter du etter da?: "))
	serv = str(input("Skriv inn servernavn: "))

	openfvar = openfiles_p + r" /query /fo csv /nh /s " + serv + r" > " + csv_p
	print("Henter liste med åpne filer - vennligst vent...")
	try:
		subprocess.check_output(openfvar, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print(e.output)
		print("Fikk ikke lagret liste med treff i åpne filer! Avslutter om 5 sekund...")
		sleepexit()
	with open(fp,encoding="cp437") as f:
		reader = csv.reader(f)
		for row in reader:
			if (match.casefold() in row[1].casefold() or match.casefold() in row[3].casefold()) and "." in row[3][-8:]:
				matches.append({'ID': row[0], 'opened_by': row[1], 'path': row[3]})

	print("Lagret liste med treff i åpne filer! Yay!")
	time.sleep(3)
	cls()
	pmret = parsematches(matches)
	if (pmret):
		while (killid is not 0 and pmret):
			killid = int(input('Skriv inn ID på filen du vil lukke: '))
			if killid is 0:
				print ("Starter på nytt...")
			else: 
				print("LUKKER FIL ID: " + str(killid))
				openfvar = openfiles_p + r" /disconnect /s " + serv + " /id " + str(killid)
				try:
					subprocess.check_output(openfvar, stderr=subprocess.STDOUT, shell=True)
					matches[:] = [d for d in matches if d.get('ID') != str(killid)] # http://stackoverflow.com/questions/1235618/python-remove-dictionary-from-list
					print("Lukket fil " + str(killid) + "!")
					if closedfiles is "":
						closedfiles = str(killid)
					else:
						closedfiles = closedfiles + ", " + str(killid)
				except subprocess.CalledProcessError as e:
					print(e.output)
					print("Klarte ikke å lukke fil " + str(killid) + "!")
					sleepexit()
				time.sleep(2)
				cls()
				pmret = parsematches(matches)
				print("Lukkede filer: " + closedfiles + ".")
		time.sleep(2)
		cls()
	else:
		print ("Ingen treff! Starter på nytt...")
		time.sleep(2)
		cls()

if  __name__ =='__main__':
	while (1):
		main()
