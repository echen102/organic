# global variable declaration of operations 
# the calculator will support
supported_operations = ['+', '-', '*', '/']

def main():
	print "Welcome to my first calculator!"
	print "This calculator only takes in whole number inputs"

	# taking in first operand in calculation
	first_operand = raw_input('Please enter first operand: ')

	# checking to make sure operand is a digit sequence
	while not first_operand.isdigit() or len(first_operand) == 0:
		# check for negative numbers
		if len(first_operand) > 1:
			if first_operand[0] == '-' and first_operand[1:].isdigit():
				break
		print "Please enter a valid digit sequence!"
		first_operand = raw_input('Please enter first operand: ')

	# taking in the operation
	operation = raw_input('\nPlease enter operation: ')

	# checking to see if the input operation is one we support
	while operation not in supported_operations:
		print "Whoops! We don't support that operation."
		operation = raw_input('Please enter operation: ')

	# taking in second operand in calculation
	second_operand = raw_input('\nPlease enter second operand :')

	# checking to make sure operand is a digit sequence
	while not second_operand.isdigit() or len(second_operand) == 0:
		# check for negative numbers
		if len(second_operand) > 1:
			if second_operand[0] == '-' and second_operand[1:].isdigit():
				break
		print "Please enter a valid digit sequence!"
		second_operand = raw_input('Please enter second operand :')

	# converting operands from strings into ints
	# also known as "casting"
	first_operand = float(first_operand)
	second_operand = float(second_operand)

	# Compute the sequence and output answer
	if operation == '+': 
		ans = add(first_operand, second_operand)
	elif operation == '-': 
		ans = sub(first_operand, second_operand)
	elif operation == '*':
		ans = multiply(first_operand, second_operand)
	else:
		ans = divide(first_operand, second_operand)
	
	print "\nCalculated Answer " + str(ans)

# Operation function definitions
# Performs addition
def add(first, second): 
	out = first + second
	return out

# Performs subtraction
def sub(first, second):
	out = first - second
	return out

# Performs multiplication
def multiply(first, second):
	out = first * second
	return out

# Performs division
def divide(first, second):
	if second == 0:
		print "Divide by 0 error!"
		return 0
	out = first/second
	return out

if __name__ == "__main__": 
	main()