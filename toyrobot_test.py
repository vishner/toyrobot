import unittest
from toyrobot import ToyRobot

class TestToyRobot(unittest.TestCase):

    def setUp(self):
        self.robot = ToyRobot()

    def test_initial_state(self):
        self.assertFalse(self.robot.placed)
        self.assertIsNone(self.robot.x)
        self.assertIsNone(self.robot.y)
        self.assertIsNone(self.robot.direction)

    def test_valid_placement(self):
        self.assertTrue(self.robot.place(0, 0, 'NORTH'))
        self.assertTrue(self.robot.placed)
        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)
        self.assertEqual(self.robot.direction, 'NORTH')

    def test_invalid_placement(self):
        self.assertFalse(self.robot.place(5, 5, 'NORTH'))
        self.assertFalse(self.robot.place(0, 0, 'INVALID'))
        self.assertFalse(self.robot.placed)

    def test_move(self):
        self.robot.place(0, 0, 'NORTH')
        self.assertTrue(self.robot.move())
        self.assertEqual(self.robot.y, 1)
        
        self.robot.place(0, 4, 'NORTH')
        self.assertFalse(self.robot.move())
        self.assertEqual(self.robot.y, 4)

    def test_left(self):
        self.robot.place(0, 0, 'NORTH')
        self.assertTrue(self.robot.left())
        self.assertEqual(self.robot.direction, 'WEST')
        self.assertTrue(self.robot.left())
        self.assertEqual(self.robot.direction, 'SOUTH')

    def test_right(self):
        self.robot.place(0, 0, 'NORTH')
        self.assertTrue(self.robot.right())
        self.assertEqual(self.robot.direction, 'EAST')
        self.assertTrue(self.robot.right())
        self.assertEqual(self.robot.direction, 'SOUTH')

    def test_report(self):
        self.assertEqual(self.robot.report(), "Robot not placed yet.")
        self.robot.place(1, 2, 'EAST')
        self.assertEqual(self.robot.report(), "1,2,EAST")

    def test_move_sequence(self):
        self.robot.place(0, 0, 'NORTH')
        self.robot.move()
        self.robot.right()
        self.robot.move()
        self.assertEqual(self.robot.report(), "1,1,EAST")

    def test_invalid_moves(self):
        self.assertFalse(self.robot.move())
        self.assertFalse(self.robot.left())
        self.assertFalse(self.robot.right())
        
        self.robot.place(0, 0, 'SOUTH')
        self.assertFalse(self.robot.move())
        
        self.robot.place(0, 0, 'WEST')
        self.assertFalse(self.robot.move())

if __name__ == '__main__':
    unittest.main()