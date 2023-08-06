import pytest 
import math
from AutoDiff.ad import DiffObj, Variable, VectorFunction
from AutoDiff.ad import MathOps as mo

class TestAutoDiff():

	# test add 
	def test_add(self):  
		val_dict = {'x' : 10, 'y' : 20, 'z':1}
		x = Variable('x')
		y = Variable('y')
		z = Variable('z')
		c1 = 5

		f0 = x + y		     
		assert(f0.get_val(val_dict) ==30)
		assert(f0.get_der(val_dict)['x'] == 1)
		assert(f0.get_der(val_dict)['y'] == 1)

		f1 = y + x
		assert(f1.get_val(val_dict) ==30)
		assert(f1.get_der(val_dict)['x'] == 1)
		assert(f1.get_der(val_dict)['y'] == 1)	

		f2 = f0 + f1 + x
		assert(f2.get_val(val_dict) ==70)
		assert(f2.get_der(val_dict)['x'] == 3)
		assert(f2.get_der(val_dict)['y'] == 2)

		f3 = f0 + c1	
		assert(f3.get_val(val_dict) ==35)
		assert(f3.get_der(val_dict)['x'] == 1)
		assert(f3.get_der(val_dict)['y'] == 1)

		f4 = c1 + f0	
		assert(f4.get_val(val_dict) ==35)
		assert(f4.get_der(val_dict)['x'] == 1)
		assert(f4.get_der(val_dict)['y'] == 1)

		with pytest.raises(AttributeError):
			assert(c1.get_der(val_dict, ['x', 'y'])['x'] == 0)
		with pytest.raises(AttributeError):
			assert(c1.get_der(val_dict, ['x', 'y'])['y'] == 0)


	# test subtract 
	def test_subtract(self):
		val_dict = {'x' : 10, 'y' : 20}
		x = Variable('x')
		y = Variable('y')
		f0 = x - y	
		c1 = 5

		assert(f0.get_val(val_dict) ==-10)
		assert(f0.get_der(val_dict)['x'] == 1)
		assert(f0.get_der(val_dict)['y'] == -1)

		f1 = y - x
		assert(f1.get_val(val_dict) ==10)
		assert(f1.get_der(val_dict)['x'] == -1)
		assert(f1.get_der(val_dict)['y'] == 1)

		f2 = f0 + f1 - x
		assert(f2.get_val(val_dict) ==-10)
		assert(f2.get_der(val_dict)['x'] == -1)
		assert(f2.get_der(val_dict)['y'] == 0)

		f3 = f0 - c1
		assert(f3.get_val(val_dict) == -15)
		assert(f3.get_der(val_dict)['x'] == 1)
		assert(f3.get_der(val_dict)['y'] == -1)

		f4 = c1 - f0
		assert(f4.get_val(val_dict) == 15)
		assert(f4.get_der(val_dict)['x'] == -1)
		assert(f4.get_der(val_dict)['y'] == 1)

		f5 = x + y - y 
		assert(f5.get_val(val_dict) ==10)
		assert(f5.get_der(val_dict)['x'] == 1)
		assert(f5.get_der(val_dict)['y'] == 0)

		f6 = 6 - x
		assert(f6.get_val(val_dict)==-4)


	# test multiply
	def test_multiply(self):
		val_dict = {'x' : 10, 'y' : 20}
		x = Variable('x')
		y = Variable('y')	
		c1 = 5

		f0 = x*y	     
		assert(f0.get_val(val_dict) ==200)
		assert(f0.get_der(val_dict)['x'] == 20)
		assert(f0.get_der(val_dict)['y'] == 10)

		f1 = y*x	     
		assert(f1.get_val(val_dict) ==200)
		assert(f1.get_der(val_dict)['x'] == 20)
		assert(f1.get_der(val_dict)['y'] == 10)

		f2 = f0*f1
		assert(f2.get_val(val_dict) ==40000)
		assert(f2.get_der(val_dict)['x'] == 8000)
		assert(f2.get_der(val_dict)['y'] == 4000)

		f3 = f0*c1 
		assert(f3.get_val(val_dict) ==1000)
		assert(f3.get_der(val_dict)['x'] == 100)
		assert(f3.get_der(val_dict)['y'] == 50)

		f4 = c1*f0 
		assert(f4.get_val(val_dict) ==1000)
		assert(f4.get_der(val_dict)['x'] == 100)
		assert(f4.get_der(val_dict)['y'] == 50)


	# test divide 
	def test_divide(self):
		val_dict = {'x' : 10, 'y' : 20, 'z':2}
		x = Variable('x')
		y = Variable('y')
		c1 = 5
		z = Variable('z')

		f0 = x/y
		assert(f0.get_val(val_dict) ==0.5)
		assert(f0.get_der(val_dict)['x'] == 0.05)
		assert(f0.get_der(val_dict)['y'] == -0.025)

		f1 = y/x
		assert(f1.get_val(val_dict) ==2.0)
		assert(f1.get_der(val_dict)['x'] == -0.2)
		assert(f1.get_der(val_dict)['y'] == 0.1)

		f2 = f1/y
		assert(f2.get_val(val_dict) ==0.1)
		assert(f2.get_der(val_dict)['x'] == -0.01)
		assert(f2.get_der(val_dict)['y'] == 0.00)

		f3 = f0/f1 
		assert(f3.get_val(val_dict) ==0.25)
		assert(f3.get_der(val_dict)['x'] == 0.05)
		assert(f3.get_der(val_dict)['y'] == -0.025)

		f4 = f0/c1 
		assert(f4.get_val(val_dict) ==0.1)
		assert(f4.get_der(val_dict)['x'] == 0.01)
		assert(f4.get_der(val_dict)['y'] == -0.005)

		f5 = 5/x
		assert(f5.get_val(val_dict)==0.5)
		assert(f5.get_der(val_dict)['x']==-.05)

		f6 = 5**z
		assert(f6.get_val(val_dict) == 25)
		assert(f6.get_der(val_dict)['z'] == 5**2*math.log(5))

	# test power
	def test_power(self):
		val_dict = {'x' : 10.0, 'y' : 3.0}
		x = Variable('x')
		y = Variable('y')	
		c1 = 2.0
		c2 = -2.0
		c3 = 0.0

		f0 = x**c1
		assert(f0.get_val(val_dict) ==100)
		assert(f0.get_der(val_dict)['x'] == 20)

		f1 = x**c2
		assert(f1.get_val(val_dict) ==0.01)
		assert(f1.get_der(val_dict)['x'] == -0.002)

		f2 = x**c3 
		assert(f2.get_val(val_dict) ==1)
		assert(f2.get_der(val_dict)['x'] == 0)

		f3 = x**y
		assert(f3.get_val(val_dict) ==1000)
		assert(f3.get_der(val_dict)['x'] == 300)
		assert(f3.get_der(val_dict)['y'] == math.log(10.0)*1000)

		f4 = f0 ** f1
		assert(f2.get_val(val_dict) ==1)
		assert(f2.get_der(val_dict)['x'] == 0)

		f5 = 2.0**y
		assert(f5.get_der(val_dict)['y'] == 8*math.log(2))

		f5 = y**2.0
		assert(f5.get_der(val_dict)['y'] == 6.0)

	def test_trig(self):
		val_dict = {'x' : 0, 'y' : math.pi/2}
		x = Variable('x')
		y = Variable('y')	
		c1 = 2.0
		c2 = -2.0
		c3 = 0.0

		f0 = mo.sin(x)
		assert(f0.get_val(val_dict) ==0)
		assert(f0.get_der(val_dict)['x'] == 1.0)

		f1 = c1*f0
		assert(f1.get_val(val_dict) ==0)
		assert(f1.get_der(val_dict)['x'] == 2.0)

		f2 = c1+f0
		assert(f2.get_val(val_dict) ==2.0)
		assert(f2.get_der(val_dict)['x'] == 1.0)

		f3 = mo.sin(y)
		assert(f3.get_val(val_dict) ==1.0)
		assert(f3.get_der(val_dict)['y'] == math.cos(math.pi/2))

		f4 = mo.cos(f3)
		assert(f4.get_val(val_dict) ==math.cos(math.sin(math.pi/2)))
		assert(f4.get_der(val_dict)['y'] == -math.sin(math.sin(math.pi/2))*math.cos(math.pi/2))

		f5 = mo.tan(x)
		assert(f5.get_val(val_dict)) == math.tan(0)
		assert(f5.get_der(val_dict)['x']) == 1/math.cos(0)**2

	def test_hyperbolic_trig(self):
		val_dict = {'x' : 0, 'y' : math.pi/2}
		x = Variable('x')
		y = Variable('y')	

		f1 = mo.tanh(x)
		assert(f1.get_val(val_dict) == 0)
		assert(f1.get_der(val_dict)['x'] == 1)

		f2 = mo.cosh(x)
		assert(f2.get_val(val_dict) == 1)
		assert(f2.get_der(val_dict)['x'] == 0)

		f3 = mo.sinh(x)
		assert(f3.get_val(val_dict) == 0)
		assert(f3.get_der(val_dict)['x'] == 1)

	def test_inverse_trig(self):
		val_dict = {'x' : 0, 'y' : -1}
		x = Variable('x')
		y = Variable('y')	

		f1 = mo.arctan(x)
		assert(f1.get_val(val_dict) == 0)
		assert(f1.get_der(val_dict)['x'] == 1)

		f2 = mo.arccos(x)
		f21 = mo.arccos(y)
		assert(f2.get_val(val_dict) == math.pi/2)
		assert(f2.get_der(val_dict)['x'] == -1)
		with pytest.raises(ValueError):
			f21.get_der(val_dict)

		f3 = mo.arcsin(x)
		f31 = mo.arcsin(y)
		assert(f3.get_val(val_dict) == 0)
		assert(f3.get_der(val_dict)['x'] == 1)
		with pytest.raises(ValueError):
			f31.get_der(val_dict)


	def test_log(self):
		val_dict = {'x' : 10, 'y' : 5, 'z' : -1, 'a' : 0}
		x = Variable('x')
		y = Variable('y')
		z = Variable('z')
		a = Variable('a')
		c1 = 2.0

		f0 = mo.log(x)
		assert(f0.get_val(val_dict) ==math.log(10))
		assert(f0.get_der(val_dict)['x'] == 0.10)

		f1 = f0**c1
		assert(f1.get_val(val_dict) ==math.log(10)**2.0)
		assert(f1.get_der(val_dict)['x'] == 2*math.log(10)*0.1)

		f2 = mo.log(y)*f0
		assert(f2.get_val(val_dict) ==math.log(5)*math.log(10))
		assert(f2.get_der(val_dict)['x'] == math.log(5)*(1/10))
		assert(f2.get_der(val_dict)['y'] == math.log(10)*(1/5))

		with pytest.raises(ValueError):
			f2 = mo.log(z)
			f2.get_val(val_dict)['z']

		with pytest.raises(ValueError):
			f2 = mo.log(a)
			f2.get_der(val_dict)['a']

		with pytest.raises(ValueError):
			f3 = mo.log(x,-5)

		f3 = mo.log(x,10)
		assert(f3.get_val(val_dict) ==1)
		# issue with rounding
		assert(f3.get_der(val_dict)['x']-(1.0/(10.0*math.log(10)))<1e-10)

		f4 = mo.loge(x)
		assert(f4.get_val(val_dict) == math.log(10))

	def test_exp(self):
		val_dict = {'x' : 10, 'y' : 5}
		x = Variable('x')
		y = Variable('y')
		c1 = 2.0
		c2 = 0.0

		f0 = mo.exp(x)
		assert(f0.get_val(val_dict) == math.exp(10))
		assert(f0.get_der(val_dict)['x'] == math.exp(10))

		f1 = c1*f0

		assert(f1.get_val(val_dict)==2.0*math.exp(10))
		assert(f1.get_der(val_dict)['x'] == 2.0*math.exp(10))

	def test_logistic(self):
		val_dict = {'x' : 10, 'y' : 5}
		x = Variable('x')
		f = mo.logistic(x)
		assert(f.get_val(val_dict) == 1/(1+math.exp(-10)))

	def test_sqrt(self):
		val_dict = {'x' : 10, 'y' : 4, 'z':-5}
		x = Variable('x')
		y = Variable('y')
		z = Variable('z')
		c1 = 2.0
		c2 = 0.0

		f = mo.sqrt(y)
		g = mo.sqrt(z)

		assert(f.get_val(val_dict) == 2)
		assert(f.get_der(val_dict)['y'] == 0.25)
		with pytest.raises(ValueError):
                    g.get_der(val_dict)['z']
		with pytest.raises(ValueError):
                    g.get_val(val_dict)['z']

	def test_exceptions(self):
		val_dict = {'x' : 10, 'y' : 5}
		x = Variable('x')
		y = Variable('y')
		c1 = 2.0
		c2 = 0.0
		f = 5
			
		with pytest.raises(ValueError):
			f0 = x/c2
			f0.get_val(val_dict)
		with pytest.raises(ValueError):
			f0.get_der(val_dict)['p']
		with pytest.raises(ValueError):
			f0.get_val({'p':5})
		with pytest.raises(TypeError):
			f0.get_val({'x':'hello'})
		with pytest.raises(TypeError):
			mo.sin("hello")


	def test_neg(self):
		val_dict = {'x' : 10, 'y' : 5}
		x = Variable('x')
		y = Variable('y')
		c1 = 2.0	

		f1 = c1*x
		f2 = -f1
		assert(f2.get_val(val_dict) == -20.0)

		f3 = x*y
		f4 = -f3 
		assert(f4.get_val(val_dict) == -50.0)
		assert(f4.get_der(val_dict)['x']==-5)
		assert(f4.get_der(val_dict)['y']==-10)

	def test_divide_by_zero_dir(self):
		val_dict = {'x' : 0}
		x = Variable('x')
		y = Variable('y')
		c1 = 1/3

		f0 = x**c1
		with pytest.raises(ZeroDivisionError):
			f0.get_der(val_dict)['x']

	def test_get_dict_val(self):
		val_dict = {'x' : 0, 'y':5}
		x = Variable('x', 5)
		y = Variable('y', 7)
		z = Variable('x', 7)
		w = 5
		p = Variable('x')

		f = 2*x*y
		g = 2*x*z
		assert(f.get_dict_val() == {'x':5, 'y':7})

		with pytest.raises(ValueError):
			g.get_dict_val()

		assert(p.get_der(val_dict)['x'] == 1)

	def test_equalities(self):
		x = Variable('x', 5)
		y = Variable('y', 7)
		z = Variable('x', 5)
		w = Variable('y',5)
		assert(not x==y)
		assert(not 'a'==y)
		assert(x!=y)
		assert(x==z)
		assert(x<y)
		assert(x<=y)
		assert(x>=z)
		assert(x!=w)
		assert(y>x)
		with pytest.raises(ValueError):
			assert(x > "hi")
		with pytest.raises(ValueError):
			assert(x < "hi")
		with pytest.raises(ValueError):
			assert(x >= "hi")
		with pytest.raises(ValueError):
			assert(x <= "hi")

		f = 5*x
		g = 10*x
		h = 5*w
		assert(not f==g)
		assert(not 'a'==f)
		assert(f!=g)
		assert(f<=g)
		assert(f<g)
		assert(f!=h)
		assert(h>=f)
		assert(g>f)
		with pytest.raises(ValueError):
			assert(f > 2)
		with pytest.raises(ValueError):
			assert(f < 2)
		with pytest.raises(ValueError):
			assert(f >= 2)
		with pytest.raises(ValueError):
			assert(f <= 2)


		f1 = VectorFunction([f,g])
		f2 = VectorFunction([f,g])
		f3 = VectorFunction([f,h])
		t1 = 0
		t2 = 1 
		f4 = VectorFunction([t1*f,t1*g])
		f5 = VectorFunction([t2*f,t2*g])
		assert(f1==f2)
		assert(f1!=f3)
		assert(f3<=f2)
		assert(f1>=f2)
		assert(f5>f4)
		assert(f4<f5)

		a = mo.sin(x)
		b = mo.sin(y)
		c = mo.sin(z)
		assert(not a==b)
		assert(a!=h)
		assert(a<=b)
		assert(a<b)
		assert(b>c)
		assert(b>=c)

		with pytest.raises(ValueError):
			assert(a > 2)
		with pytest.raises(ValueError):
			assert(a < 2)
		with pytest.raises(ValueError):
			assert(a >= 2)
		with pytest.raises(ValueError):
			assert(a <= 2)
