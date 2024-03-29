"""
Apparent:
Data structures and routines for working with apparent resistivity data (raw data)
"""

import csv
import numpy as np
from itertools import tee, izip

class Survey():
	"""
	A Survey is a collection of Profiles
	"""
	
	def __init__(self, profiles = []):
		"""
		"""
		self.Profiles = profiles



class Profile():
	"""
	A profile is defined as a collection of quadrapoles. 
	"""
	def __init__(self, quads = []):
		"""
		"""
		self.Quads = quads
		self.Electrodes = None #Or not see comment in read_electrodes?
		
	
	def read_electrodes(self, fname):
		""" 
		Reads a electrode coordinates from a table
		Input file must have the following columns: 
		Ref X (Y) (Z) 
		where Y and Z are optional.  
		"""
		elecs = []
		with open(fname, 'rb') as f:
			dialect = csv.Sniffer().sniff(f.read(1024))
			f.seek(0)
			reader = csv.reader(f, dialect)
			for line in reader:
				try:
					ref, x, y, z = line
					elecs.append(Electrode(x, y, z, ref))
				except ValueError:
					try:
						ref, x, y = line
						elecs.append(Electrode(x=x, y=y, ref=ref))
					except ValueError:
						try:
							ref, x = line
							elecs.append(Electrode(x=x, ref=ref))
						except:
							print('Could not read file')
							return
		self.Electrodes = PolyLine(points = elecs)
		
		
		
		
		if self.quads:
			# if a list of quadrapoles is present,
			# populate the electrodes in this list with
			# relevant data
			pass
		
		else:
			# if list of quadrapoles not present, 
			# create electrode list?? (or throw error?)
			pass
			
	@classmethod
	def from_protocol(cls, fname):
		"""
		Reads a R2 protocol file and returns a Profile() instance
		"""
		quads = []
		with open(fname, 'rb') as f:
			dialect = csv.Sniffer().sniff(f.read(1024))
			f.seek(0)
			reader = csv.reader(f, dialect)
			for line in reader:
				try:
					i, pp, pm, cp, cm, r, e = line
				except ValueError:
					i, pp, pm, cp, cm, r = line
					e = None
				except:
					raise Exception('Error reading file %s'% fname)		
				
				
				quads.append(Quadrapole(A = Electrode(ref = pp), 
									B = Electrode(ref = pm),
									M = Electrode(ref = cp),
									N = Electrode(ref = cm),
									res = r, std = e, ref = i))
				
			return cls(quads = quads)
	
	
	def to_protocol(self, folder):
		"""
		Writes the profile to a R2 protocol file
		"""
		pass
	
	
	def pseudosection(self, ax = None):
		""" Makes a contour pseudosection of the apparent resistivity
		If ax = None, creates a new figure and axes.
		If an axes is passed as an argument, it plots into the given axes
		"""
			
			

class Quadrapole():
	"""
	A quadrapole is a configuration of 4 electrodes which has data associated to it
	"""
	
	def __init__(self, A = None, B = None, M = None, N = None,
				rho = None, res= None, std = None, foc_dep = None,
				foc_pos = None, ref = None):
		
		self.A = A
		self.B = B
		self.M = M
		self.N = N
		
		self.FocusDepth = foc_dep
		self.FocusPosition = foc_pos
		
		self.Res = res
		self.Rho = rho
		self.Std = std 
		
		self.Ref = ref
		
	def focus_depth(self):
		"""Calculates the focus depth """
		pass
	

class PolyLine():
	"""
	Defines a line. It can have 2 or more points along it
	and is not necessarily straight. The points list be in sequential order 
	"""
	
	def __init__(self, points=[]):
		
		self.Points = points
		
	def length(self):
		""" Calculates the total length of the polyline """		
		initial = self.Points[0]
		total_dist = 0
		for point in self.Points[1:]:
			total_dist = total_dist + point.distance(initial)
			initial = point
			
		return total_dist
	
	def slope(self):
		""" Returns the slope between each pair of points as a list """
		slope = []
		for p1, p2 in self.line_segments():
			slope.append((p1.x-p2.x)/(p1.y-p2.y))
		
		return slope

	def line_segments(self):
		""" Returns each line segment as a tuple containing a pair of points"""
		a, b = tee(self.Points)
		next(b, None)
		return izip(a, b)
	
	def x(self):
		return [pnt.x for pnt in self.Points]
	
	def y(self):
		return [pnt.y for pnt in self.Points]
	
	def z(self):
		return [pnt.z for pnt in self.Points]
	
	def ref(self):
		try:
			return [pnt.ref for pnt in self.Points]
		except ValueError:
			print 'Line does not contain referenced points (electrodes)'			
		except: # Only here as unsure the ValueError is the correct error. Delete when verified
			'Unable to find references'
			

class Point():
	"""
	Defines a point 
	"""	
	
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z
		
	def move(self, dx=0, dy=0, dz=0):
		""" Moves the point by the specified amount """
		
		self.x = self.x + dx
		self.y = self.y + dy
		self.z = self.z + dz
		
	def distance(self, p):
		"""Returns the distance between self and another point, p. 
		"""
		return np.sqrt([(self.x - p.x)**2 + (self.y-p.y)**2 + (self.z-p.z)**2])
	
	def __add__(self, p):
		"""
        return a new point found by adding self and p. This method is
        called by e.g. p+q for points p and q
        """
		return Point(self.x+p.x, self.y+p.y, self.z+p.z)
	
	def __repr__(self):
		"""
        return a string representation of this point. This method is
        called by the repr() function, and
        also the str() function. It should produce a string that, when
        evaluated, returns a point with the 
        same data.
        """
		return 'Point(%d,%d)' % (self.x, self.y)
		
class Electrode(Point):
	"""
	Defines a single electrode.
	An electrode is essentially a referenced point.
	"""
	
	def __init__(self, x = 0.0, y= 0.0, z = 0.0, ref = None):
		Point.__init__(self, x, y, z)		
		self.Ref = ref
