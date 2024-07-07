import unittest

from cheeze import *
from tests.pgutils import *

class TestLayoutManagerUnits(unittest.TestCase):
    def test_LUnit_abs(self):
        # When there is ample space
        self.assertAlmostEqual(LUnit("10 px").abs(100, LUnit2(100, 100)), 10)

        # When the space requirement exceeds given space
        self.assertAlmostEqual(LUnit("110 px").abs(100, LUnit2(100, 100)), 100)

        # Other normal unit cases
        self.assertAlmostEqual(LUnit("9 %").abs(100, LUnit2(100, 100)), 9)
        self.assertAlmostEqual(LUnit("1 f").abs(100, LUnit2(100, 100)), 100)
        self.assertAlmostEqual(LUnit("2.5 vh").abs(100, LUnit2(10, 100)), 2.5)
        self.assertAlmostEqual(LUnit("5.54 vw").abs(100, LUnit2(1000, 100)), 55.4)

        # Check the unit representation
        self.assertEqual(repr(LUnit("1 %")), "1.0%")
        
        # Check for exceeding space
        for x in UNIT:
            self.assertAlmostEqual(LUnit(130.4, x).abs(100, LUnit2(100, 100)), 100)
    
    def test_LUnit2_arithmethic(self):
        x = LUnit2(100, 100)

        # Do arithmetic checking
        self.assertEqual((x.x.val, x.y.val), (100, 100))

        with self.assertRaises(AssertionError):
            x += LUnit2(10, "20 %")
        
        x += LUnit2(10, 10)
        self.assertEqual((x.x.val, x.y.val), (110, 110))

        x /= (10, 10)
        self.assertEqual((x.x.val, x.y.val), (11, 11))

        x *= (11, 11)
        self.assertEqual((x.x.val, x.y.val), (121, 121))

        with self.assertRaises(ZeroDivisionError):
            x /= (0, 0)

        # Check repr
        self.assertEqual(repr(x), "(121.0px, 121.0px)")        

    def test_LRect(self):
        r = LRect((10, 11), (10.4, 20.62))
        self.assertTrue(r.collides_withr(LRect((12, 12), (100, 100))))
        self.assertTrue(r.collides_withr(LRect((12, 12), (1, 1))))
        self.assertFalse(r.collides_withr(LRect((12, 12), (0, 10))))

        self.assertEqual(r.as_int(), (10, 11, 10, 20))
        self.assertEqual(r.as_float(), (10, 11, 10.4, 20.62))

        self.assertFalse(r.is_zero())

        self.assertEqual(repr(r), "LRect((10, 11), (10.4, 20.62))")

    def test_shaderbounds_reshade(self):
        
        # Tests the shaderbounds reshade mechanism
        bounds = ShaderBounds((0, 0), (500, 500), partial_shader=True, parent="A", drawable=True, children=[
            ShaderBounds((40, 40), (300, 300), partial_shader=True, drawable=True, parent="B", children=[
                ShaderBounds((4, 4), (120, 110), partial_shader=False, drawable=True, parent="B1"),
                ShaderBounds((200, 90), (220, 110), partial_shader=True, drawable=True, parent="B2")
            ]),
            ShaderBounds((340, 230), (140, 120), partial_shader=True, drawable=True, parent="C")
        ])

        bounds.calculate_child_bounds()

        # show_shaderbounds(bounds)