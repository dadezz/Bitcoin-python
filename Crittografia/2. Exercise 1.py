"""
Write the corresponding method __ne__, which checks if two FieldElement objects
are not equal to each other.
"""

def __ne__(self, other):
	if other is None:
		return True
	return self.num != other.num and self.prime != other.prime
