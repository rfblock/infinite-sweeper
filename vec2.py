from typing import Self

class Vec2:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y
	
	@property
	def tuple(self):
		return (self.x, self.y)
	
	def __add__(self, v: int | Self) -> Self:
		if (isinstance(v, Vec2)):
			return Vec2(self.x + v.x, self.y + v.y)
		
		if (isinstance(v, int)):
			return Vec2(self.x + v, self.y + v)
		
		raise TypeError
	
	def __neg__(self) -> Self:
		return Vec2(-self.x, -self.y)

	def __sub__(self, v: int | Self) -> Self:
		return self + (-v)
	
	def __mul__(self, v: int) -> Self:
		return Vec2(self.x * v, self.y * v)
	
	def __floordiv__(self, v: int) -> Self:
		return Vec2(self.x // v, self.y // v)
	
	def __mod__(self, v) -> Self:
		return Vec2(self.x % v, self.y % v)

	def __repr__(self) -> str:
		return str(self)

	def __str__(self) -> str:
		return f'<{self.x}, {self.y}>'
	
	def __hash__(self) -> int:
		return (self.x, self.y).__hash__()