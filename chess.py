import sys
import os
import copy
import random

# Koden representerer brettet slik at f-eks a2 = board[1][2].

# Brikker er representert ved en streng med 2 tegn - farge og brikke.
# F-eks 'bk' = black knight, 'wk' = white king. Tomme felt er '  '.

# Et trekk er representert ved  fire tall i en streng.
# For eksempel å flytte en brikke fra A2 til A4 = '1214' i koden.
# Brikken som står på A2 kan da hentes ved board[int(move[0])][int(move[1])]

# "Mulige trekk" er alle gyldige trekk på brettet,
# når man ikke ser på om kongen er i sjakk.

# "Gyldige trekk" er trekkene som er lov å ta, også medregnet
# at kongen ikke kan frivillig stilles i sjakk.

def meny(): # Hovedmeny, velger spilltype.
	
	print("Velkommen til dette sjakkprogrammet.")
	print("Alternativer:")
	print("1 - La maskinen spille mot seg selv")
	print("2 - Spill mot datamaskin")
	print("3 - Spill mot en annen person")

	game_type = input()
	
	if game_type == '1':
		computerVScomputer()
	elif game_type == '2':
		vsAI()
	elif game_type == '3':
		vsPlayer()



def computerVScomputer(): # To AI spiller mot hverandre
	
	board = createBoard()
		
	while True:
		board[0] += 1
		
		if board[0]%2 == 0:
			name = 'Deep Blue'
			player = 'b'
			opponent = 'w'
		else:
			name = 'AlphaZero'
			player = 'w'
			opponent = 'b'
		
		
		printBoard(board)
		
		print("Det er", name, "sin tur.")
		
		move = getAutoMove(board)
		
		if move == '1111':
			print("Remi.")
			break
		
		makeMove(board, move)
		
		computerPromote(board, move)
		
		if isCheck(board, opponent):
			if isMate(board, opponent):
				print("Det er sjakk matt!")
				break
			else:
				print("Sjakk.")



def vsAI(): # Spill mot enkel AI
	
	name = input("Hva heter du? ")
	
	board = createBoard()
	
	
	while True:
		board[0] += 1
		
		if board[0]%2 == 0: # Spiller er alltid hvit
			playerName = 'Sjakkmaskin'
			opponentName = name
			player = 'b'
			opponent = 'w'
		else:
			playerName = name
			opponentName = 'Sjakkmaskin'
			player = 'w'
			opponent = 'b'
		
		printBoard(board)
		
		if player == 'w':
			legalMoves = allLegalMoves(board)
			print(legalMoves)
			while True:
				move = getMove(board, [name])
				if move not in legalMoves:
					print("Det er ikke et gyldig trekk. Prøv igjen.")
				else:
					break
		elif player == 'b':
			move = getAutoMove(board)
		
		makeMove(board, move)
		
		print(board)
		
		if player == 'b':
			computerPromote(board, move)
		else:
			promote(board, move)
		
		if isCheck(board, opponent):
			if isMate(board, opponent):
				print("Det er sjakk matt!", playerName, "har vunnet.")
				break
			else:
				print(opponentName, "sin konge er i Sjakk.")
			
	

def vsPlayer(): # Spill mot en annen spiller
	
	board = createBoard()
	
	names = getNames()
	
	while True:
		board[0] += 1
		
		if board[0]%2 == 0:
			playerName = names[1]
			opponentName = names[0]
			player = 'b'
			opponent = 'w'
		else:
			playerName = names[0]
			opponentName = names[1]
			player = 'w'
			opponent = 'b'
			
		printBoard(board)
		
		legalMoves = allLegalMoves(board)
		while True:
			move = getMove(board, names)
			if move not in legalMoves:
				print("Det er ikke et gyldig trekk. Prøv igjen.")
			else:
				break
		
		makeMove(board, move)
		
		promote(board, move)
		
		if isCheck(board, opponent):
			if isMate(board, opponent):
				print("Det er sjakk matt!", playerName, "har vunnet.")
				break
			else:
				print(opponentName, "sin konge er i Sjakk.")



def getMove(board, names): # Henter og formaterer trekk
	
	while True:

		if board[0]%2 == 0:
			print("Det er", names[1], "sin tur.")
		else:
			print("Det er", names[0], "sin tur.")
		
		move = input("Skriv inn ditt trekk: ").lower()
		
		
		# Feil lengde på trekket
		if len(move) != 4:
			print("Trekket skal bestå av 4 tegn.")
		else:
			inrange = True
			
			if ord(move[0])-96 < 1 or ord(move[0])-96 > 8:
				inrange = False
			elif int(move[1]) < 1 or int(move[1]) > 8:
				irange = False
			elif ord(move[2])-96 < 1 or ord(move[2])-96 > 8:
				inrange = False
			elif int(move[3]) < 1 or int(move[3]) > 8:
				irange = False
				
			if not inrange:
				print('Ugyldige verdier i trekket. Skriv på formatet "a1h8".')
			else:
				# Konverterer fra type a2b4 til 1224
				return str(ord(move[0])-96) + move[1] + str(ord(move[2])-96) + move[3]
		


def getNames(): # Henter brukernavn
	
	print("Welcome to this chess program! ")
	whitePlayer = input("Hvem spiller hvit? ")
	blackPlayer = input("Hvem spiller svart? ")

	return [whitePlayer, blackPlayer]



def createBoard(): # Lager brettet
	
	board = [0,
	['--', 'wr', 'wp', '  ', '  ', '  ', '  ', 'bp', 'br'],
	['--', 'wn', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bn'],
	['--', 'wb', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bb'],
	['--', 'wq', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bq'],
	['--', 'wk', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bk'],
	['--', 'wb', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bb'],
	['--', 'wn', 'wp', '  ', '  ', '  ', '  ', 'bp', 'bn'],
	['--', 'wr', 'wp', '  ', '  ', '  ', '  ', 'bp', 'br']
	]
	
	return board



def printBoard(board): # Skriver ut brettet
	
	letters = ['br','wr','bb','wb','bn','wn','bq','wq','bk','wk','bp','wp','  ']
	symbols = ['♜','♖','♝','♗','♞','♘','♛','♕','♚','♔','♟','♙','　']
	
	print()
	for i in range(8):
		for j in range(8):
			if j == 0:
				print('-', end='')
			row = board[1+j]
			piece = row[8-i]
			index = letters.index(piece)
			print(letters[index]+'|', end='')
		print('\n―――――――――――――――――――――――――')
	print()



def isPossible(board, move): # Returnerer om trekket er mulig på brettet
	
	# Move skal her allerede være på riktig format, og begrense seg til brettet.
	
	# Bruker nesten kun "if"-statements (ikke elif/else) i denne
	# funksjonen fordi logikken blir enklere, og koden mer oversiktlig.
	
	# Lager først noen forkortelser som gjør koden raskere å skrive.
	
	b = board
	
	x1 = int(move[0])
	y1 = int(move[1])
		
	x2 = int(move[2])
	y2 = int(move[3])

	dx = x2-x1
	dy = y2-y1

	p = b[x1][y1]
	p2 = b[x2][y2]
	
	# Angriper samme farge
	if p[0] == p2[0]:
		return False
	
	# Flytter ikke egen brikke
	if b[0]%2 != 0 and p[0] != 'w':
		return False
	if b[0]%2 == 0 and p[0] != 'b':
		return False
	
	# Spesifikke begrensninger for hver brikke
	
	if p[1] == 'r': # Tårn
		if dy*dx != 0: # Må gå langs en linje, altså dx==0 eller dy==0
			return False
			
		length = abs(dx + dy)
		for i in range(1, length):
			if dx > 0:
				if b[x1+i][y1] != '  ': # Kan ikke hoppe over andre brikker
					return False
			if dy > 0:
				if b[x1][y1+i] != '  ':
					return False
			if dx < 0:
				if b[x1-i][y1] != '  ':
					return False
			if dy < 0:
				if b[x1][y1-i] != '  ':
					return False
		
	if p[1] == 'n': # Springer
		if abs(dx) == 1 and abs(dy) == 2:
			return True
		if abs(dy) == 1 and abs(dx) == 2:
			return True
		else:
			return False
		
	if p[1] == 'b': # Løper
		if abs(dy) != abs(dx): # Må gå på skrått
			return False
		
		length = abs(dx)
		
		for i in range(1, length):
			if dx > 0 and dy > 0:
				if b[x1+i][y1+i] != '  ': # Kan ikke hoppe over brikker
					return False
			if dx > 0 and dy < 0:
				if b[x1+i][y1-i] != '  ':
					return False
			if dx < 0 and dy > 0:
				if b[x1-i][y1+i] != '  ':
					return False
			if dx < 0 and dy < 0:
				if b[x1-i][y1-i] != '  ':
					return False
	
	if p[1] == 'k': # Konge
		if abs(dx) > 1 or abs(dy) > 1: # Kan kun gå ett felt om gangen
			return False
		
	if p[1] == 'q': # Dronning
		if dx*dy == 0: # Oppfører seg som et tårn. Kopier og lim inn.
			length = abs(dx + dy)
			for i in range(1, length):
				if dx > 0:
					if b[x1+i][y1] != '  ':
						return False
				if dy > 0:
					if b[x1][y1+i] != '  ':
						return False
				if dx < 0:
					if b[x1-i][y1] != '  ':
						return False
				if dy < 0:
					if b[x1][y1-i] != '  ':
						return False
		
		elif abs(dx) == abs(dy): # Oppfører seg som en løper. Kopier og lim inn.
			length = abs(dx)
			for i in range(1, length):
				if dx > 0 and dy > 0:
					if b[x1+i][y1+i] != '  ':
						return False
				if dx > 0 and dy < 0:
					if b[x1+i][y1-i] != '  ':
						return False
				if dx < 0 and dy > 0:
					if b[x1-i][y1+i] != '  ':
						return False
				if dx < 0 and dy < 0:
					if b[x1-i][y1-i] != '  ':
						return False
		
		else: # Dronning må bevege seg som enten løper eller tårn.
			return False
	
	if p[1] == 'p': # Bonde
		if abs(dy) != 1 and abs(dy) != 2: # 2 alternativ i y-retning
			return False
		if abs(dx) > 1: # Maks 1 i x-retning
			return False
		
		if abs(dy) == 2 and abs(dx) != 0: # Kan ikke gjøre begge
			return False
		if (abs(dx) == 1) and (b[x1+dx][y1+dy] == '  '): # Kan kun gå skrått for å ta en brikke
			return False
		if abs(dx) == 0 and b[x1+dx][y1+dy] != '  ': # Kan ikke angripe fremover
			return False
		
		if p[0] == 'w': # Regler spesifikt for hvite bønder
			if dy == 2 and y1 != 2: # Kan kun flytte dobbelt fra startfelt
				return False
			if dy < 0: # Må bevege seg i positiv retning
				return False
		
		if p[0] == 'b':
			if dy == -2 and y1 != 7:
				return False
			if dy > 0: # Må bevege seg i negativ retning
				return False

	return True # Hvis alt er riktig



def makeMove(b, move): # Gjennomfører et trekk
	
	b[int(move[2])][int(move[3])] = b[int(move[0])][int(move[1])] # Flytter brikken
	b[int(move[0])][int(move[1])] = '  '



def promote(board, move): # Gjennomfører eventuell forfremmelse av bonde
	
	x = int(move[2])
	y = int(move[3])
	
	piece = board[x][y]
	
	if piece[1] != 'p': # Ikke en bonde
		return board
	elif y != 8 and y != 1: # Bonden har ikke nådd kanten
		return board
	
	promote = False # Initialiserer
	if piece == 'wp' and y == 8:
		promote = True
	elif piece == 'bp' and y == 1:
		promote = True
	
	if promote:
		valid = False # Holder kontroll på gyldighet
		while not valid:
			valid = True
			newPiece = input("Hvilken offisær vil du forfremme til? [q/r/b/n]: ")
			validPieces = ['q', 'r', 'b', 'n']
			if newPiece not in validPieces:
				valid = False
		board[x][y] = piece[0] + newPiece
	
	return board



def allMoves(board): # Returnerer liste over alle mulige trekk
	
	possible_moves = []
	
	for i in range(1,9): # Alle brikker på alle plasser kan flyttes til alle plasser.
		for j in range(1,9):
			for k in range(1,9):
				for l in range(1,9):
					move = str(i)+str(j)+str(k)+str(l)
					if isPossible(board, move):
						possible_moves.append(move)
	
	return possible_moves



def isCheck(board, player): # Returnerer om spillerens konge er i sjakk
	# player er 'w' eller 'b'

	possible_next_moves = allMoves(board)
	
	for move in possible_next_moves:
		p1 = board[int(move[0])][int(move[1])]
		p2 = board[int(move[2])][int(move[3])]
		
		if player == 'w':
			if p1[0] == 'b' and p2 == 'wk':
				return True
		else:
			if p1[0] == 'w' and p2 == 'bk':
				return True
	
	return False



def isMate(board, player): # Sjekker om det er sjakkmatt
	
	b = copy.deepcopy(board) # Kopi
	if not isCheck(b, player): # Kan ikke være sjakk matt uten sjakk
		return False
	
	b[0] += 1
	
	possibleMoves = allMoves(b)
	
	for move in possibleMoves:
		b = copy.deepcopy(board) # Lager ny kopi for hvert forsøk
		makeMove(b, move)
		if not isCheck(b, player):
			return False
	
	return True



def allLegalMoves(board): # Returnerer liste over alle gyldige trekk
	
	if board[0]%2 == 0: # Hvilken spiller skal til å trekke
		player = 'b'
	else:
		player = 'w'
	
	possibleMoves = allMoves(board)
	
	legalMoves = []
	for move in possibleMoves:
		b = copy.deepcopy(board)
		makeMove(b, move)
		b[0] += 1 			# Skal se om motstander kan angripe kongen
		if not isCheck(b, player):
			legalMoves.append(move)
	
	return legalMoves



# De tre neste funksjonene er kun nødvendig for å kunne spille mot datamaskin.



def countMaterial(board): # Teller poeng på brettet
	
	m = 0 # Poengforskjell
	
	# m>0 == fordel til hvit og omvendt
	
	for i in range(1, 9):
		for j in range(1, 9):
			p = board[i][j]
			if p == 'wr':
				m += 5
			elif p == 'wn':
				m += 3
			elif p == 'wb':
				m += 3
			elif p == 'wq':
				m += 9
			elif p == 'wp':
				m += 1
			elif p == 'br':
				m -= 5
			elif p == 'bn':
				m -= 3
			elif p == 'bb':
				m -= 3
			elif p == 'bq':
				m -= 9
			if p == 'bp':
				m -= 1
	return m



def getAutoMove(board): # Bestemmer et halvveis lurt datamaskin-trekk
	
	legalMoves = allLegalMoves(board)
	
	current_material = countMaterial(board)
	
	
	max_goodness = -10000 # En sjekk for remis, behandles i hovedprogrammet
	best_move = '1111'
	
	for move in legalMoves:

		goodness = 0

		b = copy.deepcopy(board)
		makeMove(b, move)
		new_material = countMaterial(b)
		new_moves = allMoves(b)
		
		goodness += random.randint(1,20) # En sunn mengde tilfeldighet
		
		goodness += len(new_moves) - len(legalMoves) # Flere trekk tyder på utvikling
			
		goodness += 10 * abs(new_material - current_material) # Bra å ta brikker
		
		if board[0]%2 == 0:
			if isCheck(b, 'w'): # Ofte bra å gi sjakk
				goodness += 6

		if board[0]%2 != 0:
			if isCheck(b, 'b'):
				goodness += 6
		
		if board[int(move[0])][int(move[1])][1] == 'p': # Bondestormen
			goodness += 4
		elif board[int(move[0])][int(move[1])][1] != 'k': # Viktig å spille ut offisærer
			goodness += 6
		
		if goodness >= max_goodness:
			best_move = move
			max_goodness = goodness
	
	return best_move



def computerPromote(board, move): # Forenklet forfremmelse for datamaskinen

	x = int(move[2])
	y = int(move[3])
	
	piece = board[x][y]
	
	if piece == 'wp' and y == 8:
		board[x][y] = 'wq'
	elif piece == 'bp' and y == 1:
		board[x][y] = 'bq'



meny()
