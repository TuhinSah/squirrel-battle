import sys, decimal, copy

def evaluate(state):
	sum = 0
	for row in range(5):
		for col in range(5):
			if state[row][col] == maxPlayer:
				sum = sum + board[row][col]
			elif state[row][col] != '*':
				sum = sum - board[row][col]
	return sum

def successors(state, player):
	successors = []
	for row in range(5):
		for col in range(5):
			if state[row][col] == '*':
				successors.append([row, col])
	return successors

def terminalTest(state):
	if any('*' in sublist for sublist in state):
		return False
	return True

def switchPlayer(player):
	if player == 'X':
		return 'O'
	else:
		return 'X'

def printTraverseLog(cell, depth, value, alpha, beta, algo, task):
	if task in {2, 3}:
		node = cellName[cell]
		if type(depth) is not str:
			depth = `depth`
		if type(value) is not str:
			if type(value) is decimal.Decimal:
				value = value.number_class()
			else:
				value = `value`
		if value == '+Infinity':
			value = 'Infinity'
		if algo == 3:
			if type(alpha) is not str:
				if type(alpha) is decimal.Decimal:
					if alpha.is_infinite():
						alpha = alpha.number_class()
				else:
					alpha = `alpha`
			if type(beta) is not str:
				if type(beta) is decimal.Decimal:
					if beta.is_infinite():
						beta = beta.number_class()
				else:
					beta = `beta`
			if beta == '+Infinity':
				beta = 'Infinity'
			traverseLog.write('\n' + node + ',' + depth + ',' + value + ',' + alpha + ',' + beta)
		else:
			traverseLog.write('\n' + node + ',' + depth + ',' + value)

def maxValue(state, alpha, beta, depth, player, algo, maxDepth, node, task):
	nextPlayer = switchPlayer(player)
	if terminalTest(state) or depth == 0:
		value = evaluate(state)
		printTraverseLog(node, maxDepth, value, alpha, beta, algo, task)
		return value
	v = decimal.Decimal('-Infinity')
	for successor in successors(state,player):
		printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
		nextNode = successor[0]*5+successor[1]
		v = max(v, minValue(move(state, nextPlayer, successor[0], successor[1]), alpha, beta, depth-1, nextPlayer, algo, maxDepth, nextNode, task))
		if task == 3:
			if v >= beta:
				printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
				return v
			alpha = max(alpha, v)
	printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
	return v

def minValue(state, alpha, beta, depth, player, algo, maxDepth, node, task):
	nextPlayer = switchPlayer(player)
	if terminalTest(state) or depth == 0:
		value = evaluate(state)
		printTraverseLog(node, maxDepth, value, alpha, beta, algo, task)
		return value
	v = decimal.Decimal('Infinity')
	for successor in successors(state,player):
		printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
		nextNode = successor[0]*5+successor[1]
		v = min(v, maxValue(move(state, nextPlayer, successor[0], successor[1]), alpha, beta, depth-1, nextPlayer, algo, maxDepth, nextNode, task))
		if task == 3:
			if v <= alpha:
				printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
				return v
			beta = min(beta, v)
	printTraverseLog(node, maxDepth - depth, v, alpha, beta, algo, task)
	return v

def search(state, depth, player, algo, maxDepth, task):
	if task in {2,3}:
		if algo == 3:
			traverseLog.write('Node,Depth,Value,Alpha,Beta')
		elif algo == 2:
			traverseLog.write('Node,Depth,Value')
	if player == maxPlayer:
		printTraverseLog(25,'0','-Infinity','-Infinity','Infinity',algo,task)
		alpha = decimal.Decimal('-Infinity')
		beta = decimal.Decimal('Infinity')
		nextStateEval = decimal.Decimal('-Infinity')
		for successor in successors(state,player):
			node = successor[0]*5+successor[1]
			successorState = move(state, player, successor[0], successor[1])
			successorEval = minValue(successorState, alpha, beta, depth-1, player, algo, maxDepth, node, task)
			if successorEval > nextStateEval:
				nextStateEval = successorEval
				nextState = successorState
				alpha = max(alpha, successorEval)
			printTraverseLog(25,'0',nextStateEval,alpha,beta,algo,task)
	else:
		printTraverseLog(25,'0','-Infinity','-Infinity','Infinity',algo,task)
		alpha = decimal.Decimal('-Infinity')
		beta = decimal.Decimal('Infinity')
		nextStateEval = decimal.Decimal('Infinity')
		for successor in successors(state,player):
			node = successor[0]*5+successor[1]
			successorState = move(state, player, successor[0], successor[1])
			successorEval = maxValue(successorState, alpha, beta, depth-1, player, algo, maxDepth, node, task)
			if successorEval < nextStateEval:
				nextStateEval = successorEval
				nextState = successorState
				beta = min(beta, successorEval)
			printTraverseLog(25,'0',nextStateEval,alpha,beta,algo,task)
	return nextState

def isRaidable(state, player, row, col):
	if row - 1 >= 0 and state[row - 1][col] == player:
		return True
	if row + 1 < 5 and state[row + 1][col] == player:
		return True
	if col - 1 >= 0 and state[row][col - 1] == player:
		return True
	if col + 1 < 5 and state[row][col + 1] == player:
		return True
	return False

def raid(state, player, row, col):
	raidedState = copy.deepcopy(state)
	raidedState[row][col] = player
	if row - 1 >= 0 and raidedState[row - 1][col] not in {'*', player}:
		raidedState[row - 1][col] = player
	if row + 1 < 5 and raidedState[row + 1][col] not in {'*', player}:
		raidedState[row + 1][col] = player
	if col - 1 >= 0 and raidedState[row][col - 1] not in {'*', player}:
		raidedState[row][col - 1] = player
	if col + 1 < 5 and raidedState[row][col + 1] not in {'*', player}:
		raidedState[row][col + 1] = player
	return raidedState

def sneak(state, player, row, col):
	sneakedState = copy.deepcopy(state)
	sneakedState[row][col] = player
	return sneakedState

def move(state, player, row, col):
	if isRaidable(state, player, row, col):
		return raid(state, player, row, col)
	else:
		return sneak(state, player, row, col)

def printState(state,f):
	for row in range(5):
		currentRow = ''
		for col in range(5):
			currentRow = currentRow + state[row][col]
		f.write(currentRow)
		f.write('\n')

if __name__ == '__main__':
	filename = sys.argv[-1]
	file = open(filename, 'r')

	global cellNmae
	cellName = {0:'A1',1:'B1',2:'C1',3:'D1',4:'E1',\
		5:'A2',6:'B2',7:'C2',8:'D2',9:'E2',\
		10:'A3',11:'B3',12:'C3',13:'D3',14:'E3',\
		15:'A4',16:'B4',17:'C4',18:'D4',19:'E4',\
		20:'A5',21:'B5',22:'C5',23:'D5',24:'E5',25:'root'}

	task = int(file.readline().rstrip())

	player = file.readline().rstrip()
	global maxPlayer
	maxPlayer = copy.deepcopy(player)
	global board

	if task != 4:
		algo = task

		depth = int(file.readline().rstrip())
		maxDepth = copy.deepcopy(depth)

		board = [ map(int,next(file).split(' ')) for x in xrange(5)]

		state = [ list(next(file).strip()) for x in xrange(5)]

		nextState = open('next_state.txt','w')

		global traverseLog
		if algo in {2, 3}:
			traverseLog = open('traverse_log.txt','w')

		printState(search(state, depth, player, algo, maxDepth, task), nextState)
	else:
		algo1 = int(file.readline().rstrip())
		depth1 = int(file.readline().rstrip())
		maxDepth1 = copy.deepcopy(depth1)
		minPlayer = file.readline().rstrip()
		algo2 = int(file.readline().rstrip())
		depth2 = int(file.readline().rstrip())
		maxDepth2 = copy.deepcopy(depth2)

		board = [ map(int,next(file).split(' ')) for x in xrange(5)]

		state = [ list(next(file).strip()) for x in xrange(5)]

		players = [player, minPlayer]
		algos = [algo1, algo2]
		depths = [depth1, depth2]
		maxDepths = [maxDepth1, maxDepth2]
		current = 0

		traceState = open('trace_state.txt','w')

		while not terminalTest(state):
			state = search(state, depths[current], players[current], algos[current], maxDepths[current], task)
			printState(state,traceState)
			current = 1 - current
