import sys
sys.path.append('../')

import cosmopy as cosmo
import numpy as np
from scipy import sparse
from math import sqrt, exp

# Unit Test
import unittest
import numpy.testing as nptest


class basic_tests(unittest.TestCase):

    def test_QP(self):
        P = sparse.csc_matrix([[4., 1], [1, 2]])
        q = np.array([1., 1])
        A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1], [-1., -1], [-1, 0], [0, -1]])
        b = np.array([1, 0.7, 0.7, -1, 0, 0])
        cone = {"l" : 6 }
        model = cosmo.Model()
        model.setup(P, q, A, b, cone, eps_abs = 1e-5, eps_rel = 1e-5)
        self.assertTrue(model.setup_complete)

        model.optimize()
        self.assertTrue(model.solved)

        obj_val, x, y, s = model.get_sol()
        self.assertEqual(model.get_status(), 'Solved')
        nptest.assert_array_almost_equal(x, np.array([0.3, 0.7]), decimal = 3)
        nptest.assert_array_almost_equal(y, np.array([0.0033, 0., 0.2, 2.903, 0., 0.]), decimal = 3)
        nptest.assert_array_almost_equal(s, np.array([0., 0.4, 0., 0., 0.3, 0.7]), decimal = 3)
        nptest.assert_almost_equal(obj_val, 1.88)


    def test_wrong_dims(self):
        model = cosmo.Model()
        q = np.array([1.,0.])
        A = sparse.eye(3, format = "csc")
        b = np.zeros(3)
        cone = {"f" : 3}
        with self.assertRaises(ValueError):
            model.setup(q = q, A = A, b = b, cone = cone)
        q = np.array([1.,0., 0.])
        cone = {"f" : 2}
        with self.assertRaises(ValueError):
            model.setup(q = q, A = A, b = b, cone = cone)
        
    def test_wrong_order(self):
        model = cosmo.Model()
        self.assertWarns(Warning, model.optimize)
        self.assertWarns(Warning, model.get_objective_value)
        self.assertWarns(Warning, model.get_x)

    def test_reset(self):
        P = sparse.csc_matrix([[4., 1], [1, 2]])
        q = np.array([1., 1])
        A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1], [-1., -1], [-1, 0], [0, -1]])
        b = np.array([1, 0.7, 0.7, -1, 0, 0])
        cone = {"l" : 6 }
        model = cosmo.Model()
        model.setup(P, q, A, b, cone, eps_abs = 1e-5, eps_rel = 1e-5, check_termination = 1)
        model.optimize()
        model.reset()
        self.assertTrue(model.result == None)
        self.assertTrue(model.solved == False)
        self.assertTrue(model.setup_complete == False)

    def test_warm_start(self):
        P = sparse.csc_matrix([[4., 1], [1, 2]])
        q = np.array([1., 1])
        A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1], [-1., -1], [-1, 0], [0, -1]])
        b = np.array([1, 0.7, 0.7, -1, 0, 0])
        cone = {"l" : 6 }
        model = cosmo.Model()
        model.setup(P, q, A, b, cone, eps_abs = 1e-5, eps_rel = 1e-5, check_termination = 1)
        model.optimize()
        obj_val, xopt, yopt, sopt = model.get_sol()
        iter_cold = model.get_iter()

        # now run again but warm start the variables
        model = cosmo.Model()
        model.setup(P, q, A, b, cone, eps_abs = 1e-5, eps_rel = 1e-5, check_termination = 1)
        model.warm_start( x= xopt, y = yopt)
        model.optimize()
        iter_warm = model.get_iter()
        self.assertTrue(iter_warm < iter_cold)



    def test_SDP(self):
        n = 6
        q = np.array([1., 4, 9, 6, 0, 7]) #upper(C)
        b = np.hstack((np.array([11., 19.]), np.zeros(6)))
        A1_t = sparse.csc_matrix([1.0, 0, 3, 2, 14, 5])
        A2_t = sparse.csc_matrix([0.0, 4, 6, 16, 0, 4])
        Is = -sparse.eye(n, format = "csc")
        Is[1, 1] = Is[3, 3] = Is[4, 4] = -sqrt(2.)
        A = sparse.vstack([A1_t, A2_t, Is], format = "csc" )
        cone = {"f" : 2, "s" : [6]}
        model = cosmo.Model()
        model.setup(q = q, A = A, b = b, cone = cone, eps_abs = 1e-5, eps_rel = 1e-5)
        model.optimize()
        obj_val = model.get_objective_value()
        self.assertEqual(model.get_status(), 'Solved')
        nptest.assert_almost_equal(obj_val, 13.902, decimal = 3)

    def test_EXP(self):
        # # max  x
        # # s.t. y * exp(x / y) <= z
        # #      y == 1, z == exp(5)
        q = np.array([-1., 0, 0])

        A1 = sparse.csc_matrix([[0., 1, 0], [0., 0, 1]])
        b1 = np.array([1., exp(5)])

        A2 = -sparse.eye(3, format = "csc")
        b2 = np.zeros(3)


        A = sparse.vstack([A1, A2], format = "csc" )
        b = np.hstack((b1, b2))
        cone = {"f" : 2, "ep" : 1}
        model = cosmo.Model()
        model.setup(q = q, A = A, b = b, cone = cone, eps_abs = 1e-5, eps_rel = 1e-5)
        model.optimize()
        obj_val = model.get_objective_value()
        status = model.get_status()

        self.assertEqual(status, 'Solved')
        nptest.assert_almost_equal(obj_val, -5, decimal = 3)

    def test_POW(self):
        # max  x1^0.6 y^0.4 + x2^0.1
        # s.t. x1, y, x2 >= 0
        #      x1 + 2y  + 3x2 == 3
        # which is equivalent to
        # max z1 + z2
        # s.t. (x1, y, z1) in K_pow(0.6)
        #      (x2, 1, z2) in K_pow(0.1)
        #      x1 + 2y + 3x2 == 3
        # x = (x1, y, z1, x2, y2, z2)
        q = np.array([0, 0, -1., 0, 0, -1.])

        # x1 + 2y + 3x2 == 3
        A1 = sparse.csc_matrix([1., 2, 0, 3., 0, 0])
        b1 = np.array([3.])

        # y2 == 1
        A2 = sparse.csc_matrix([0, 0, 0, 0, 1.0, 0])
        b2 = np.array([1.])

        # (x1, y, z1) in K_pow(0.6)
        A3 = sparse.hstack([-sparse.eye(3), np.zeros((3, 3))], format = "csc") 
        b3 = np.zeros(3)

        # (x2, y2, z2) in K_pow(0.1)
        A4 = sparse.hstack([np.zeros((3, 3)), -sparse.eye(3)], format = "csc")         
        b4 = np.zeros(3)

        A = sparse.vstack([A1, A2, A3, A4], format = "csc" )
        b = np.hstack((b1, b2, b3, b4))
        cone = {"f" : 2, "p" : [0.6, 0.1]}

        model = cosmo.Model()
        model.setup(q = q, A = A, b = b, cone = cone, eps_abs = 1e-5, eps_rel = 1e-5, max_iter = 5000)
        model.optimize()
        obj_val = model.get_objective_value()
        status = model.get_status()

        self.assertEqual(status, 'Solved')
        nptest.assert_almost_equal(obj_val, -1.8458, decimal = 3)

    def test_box_QP(self):
        # min  1/2 x'Px + q'X
        # s.t. l <= A x + b <= u
        q = np.array([1., 1.])
        P = sparse.csc_matrix([[4., 1], [1, 2]])
        A = -sparse.csc_matrix([[1., 1], [1, 0.], [0., 1]]) # s = -Ax + b, l <= s <= u
        b = np.zeros(3)
        l = np.array([1., 0, 0])
        u = np.array([1., 0.7, 0.7])
        cone = {"b" : 3}

        model = cosmo.Model()
        model.setup(P = P, q = q, A = A, b = b, cone = cone, l = l, u = u, eps_abs = 1e-5, eps_rel = 1e-5, scaling = 0)
        model.optimize()
        obj_val = model.get_objective_value()
        status = model.get_status()
        x  = model.get_x()

        self.assertEqual(status, 'Solved')
        nptest.assert_almost_equal(obj_val, 1.88)
        nptest.assert_array_almost_equal(x, np.array([0.3, 0.7]), decimal = 3)
