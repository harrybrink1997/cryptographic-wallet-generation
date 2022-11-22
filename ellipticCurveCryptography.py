
basePoint = {
  "x": 5,
  "y": 7
}

currentPoint = {}
fieldInverseMap = {}
fieldSquareRootMap = {}

def finiteEllipticalGradient(a, point, fieldSize):
  # Completing the following equation (3x^2 + a) / (2 * y)

  numerator_1 = finiteMultiplication(3, finiteMultiplication(point["x"], point["x"], fieldSize), fieldSize)
  numerator = finiteAddition(numerator_1, a, fieldSize)

  denominator = finiteMultiplication(2, point["y"], fieldSize)

  return finiteDivision(numerator, denominator, fieldSize)

def finiteAddition(num1, num2, fieldSize):
  return (num1 + num2) % fieldSize

def finiteSubtraction(num1, num2, fieldSize):
  return (num1 - num2) % fieldSize

def finiteDivision(num1, num2, fieldSize):
  return (num1 * fieldInverseMap[num2]) % fieldSize

def finiteMultiplication(num1, num2, fieldSize):
  return (num1 * num2) % fieldSize

def generateFieldInversionMap(fieldSize):

  for i in range(0, fieldSize):
    for j in range(0, fieldSize):
      product = finiteMultiplication(i, j, fieldSize)

      if product == 1:
        fieldInverseMap[i] = j
        break

def generateFieldSquareRootMap(fieldSize):
  for i in range(0, fieldSize):
    product = finiteMultiplication(i, i, fieldSize)
    if product in range(0, fieldSize):
      if (product not in fieldSquareRootMap):
        fieldSquareRootMap[product] = [i]
      else:
        fieldSquareRootMap[product].append(i)

def finiteNegation(num, fieldSize):
  return fieldSize - num 

def addPoints(point1, point2, fieldSize):
  global currentPoint

  rise = finiteSubtraction(point2["y"], point1["y"], fieldSize)
  run = finiteSubtraction(point2["x"], point1["x"], fieldSize)

  gradient = finiteDivision(rise, run, fieldSize)

  # New x-coordinate follow equation x = gradient^2 - x1 -x2
  newX_gradientSquared = finiteMultiplication(gradient, gradient, fieldSize)
  newX_firstSubtraction = finiteSubtraction(newX_gradientSquared, point1["x"], fieldSize)
  newX = finiteSubtraction(newX_firstSubtraction, point2["x"], fieldSize)

  # New x-coordinate follow equation y = gradient(x1 - x3) - y1
  newY_FirstSubtraction = finiteSubtraction(point1["x"], newX, fieldSize)
  newY_multiplication = finiteMultiplication(gradient, newY_FirstSubtraction, fieldSize)
  newY = finiteSubtraction(newY_multiplication, point1["y"], fieldSize) 

  newPoint = {
    "x": newX,
    "y": newY
  }

  currentPoint = newPoint
  return newPoint

def generateDoublePoint(a, b, point, fieldSize):
  gradient = finiteEllipticalGradient(a, point, fieldSize)

  # New x-coordinate follow equation x = gradient^2 - x1 -x2
  newX_gradientSquared = finiteMultiplication(gradient, gradient, fieldSize)
  newX_firstSubtraction = finiteSubtraction(newX_gradientSquared, point["x"], fieldSize)
  newX = finiteSubtraction(newX_firstSubtraction, point["x"], fieldSize)

  # New x-coordinate follow equation y = gradient(x1 - x3) - y1
  newY_FirstSubtraction = finiteSubtraction(point["x"], newX, fieldSize)
  newY_multiplication = finiteMultiplication(gradient, newY_FirstSubtraction, fieldSize)
  newY = finiteSubtraction(newY_multiplication, point["y"], fieldSize) 

  newPoint = {
    "x": newX,
    "y": newY
  }

  global currentPoint
  currentPoint = newPoint
  return newPoint


def generatePointsThroughAddition(curveConstant_A, curveConstant_B, fieldSize):

  print("Point 1: " + str(basePoint))
  for i in range (0, 11):
    if (i == 0):
      print("Point " + str(i + 2) + ": " + str(generateDoublePoint(curveConstant_A, curveConstant_B, basePoint, fieldSize)))
    else:
      print("Point " + str(i + 2) + ": " + str(addPoints(basePoint, currentPoint, fieldSize)))


def generatePointsThroughMultiplication(curveConstant_A, curveConstant_B, fieldSize):
  print("Point 1: " + str(basePoint))

  for i in range (1, 20):
    if i == 1:
      print("Point " + str(2**i) + ": " + str(generateDoublePoint(curveConstant_A, curveConstant_B, basePoint, fieldSize)))
    else:
      print("Point " + str(2**i) + ": " + str(generateDoublePoint(curveConstant_A, curveConstant_B, currentPoint, fieldSize)))

def decompressCoordinates(curveConstant_A, curveConstant_B, compressedCoord, fieldSize):
  parity = compressedCoord[3]
  xCoord = int(compressedCoord[4:], 16)

  componentOne = finiteMultiplication(finiteMultiplication(xCoord, xCoord, fieldSize), xCoord, fieldSize)
  componentTwo = finiteMultiplication(xCoord, curveConstant_A, fieldSize)
  ySquared = finiteAddition(finiteAddition(componentOne, componentTwo, fieldSize), curveConstant_B, fieldSize)
  yCoordinates = fieldSquareRootMap[ySquared]

  if (parity == '2'):
    for coord in yCoordinates:
      if coord % 2 == 0:
        return (xCoord, coord)
  else:
    for coord in yCoordinates:
      if coord % 2 != 0:
        return (xCoord, coord)


class FiniteEllipticCurve:
  def __init__(self, constantA, constantB, fieldSize, basePoint):
    self.constantA = constantA
    self.constantB = constantB
    self.fieldSize = fieldSize
    self.fieldInverseMap = this.generateFieldInversionMap(fieldSize)
    self.fieldSquareRootMap = {}
    self.basePoint = self.decompressCoordinate(basePoint)


  def generateFieldInversionMap(fieldSize):

    for i in range(0, fieldSize):
      for j in range(0, fieldSize):
        product = finiteMultiplication(i, j, fieldSize)

        if product == 1:
          fieldInverseMap[i] = j
          break

  def generateFieldSquareRootMap(fieldSize):
    for i in range(0, fieldSize):
      product = finiteMultiplication(i, i, fieldSize)
      if product in range(0, fieldSize):
        if (product not in fieldSquareRootMap):
          fieldSquareRootMap[product] = [i]
        else:
          fieldSquareRootMap[product].append(i)


  def decompressCoordinate(self, point):


if __name__ == "__main__":

    fieldSize = 61
    curveConstant_A = 9
    curveConstant_B = 1
    generateFieldInversionMap(fieldSize)
    generateFieldSquareRootMap(fieldSize)

    print('\nThrough Addition\n')
    generatePointsThroughAddition(curveConstant_A, curveConstant_B, fieldSize)
    print('\nThrough Multiplication\n')
    generatePointsThroughMultiplication(curveConstant_A, curveConstant_B, fieldSize)

    print('\nDecompression of Coordinate 0x025: ', decompressCoordinates(curveConstant_A,curveConstant_B ,'0x025', fieldSize))
    
    






