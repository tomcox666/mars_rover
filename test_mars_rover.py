import unittest
import sys
from io import StringIO

from mars_rover import Robot, main

class TestRobot(unittest.TestCase):
    def setUp(self):
        # Initialize a Robot object for testing
        self.robot = Robot(2, 2, "N", "")
    
    def test_turn_left(self):
        # Test that the Robot object's orientation changes to "W" after turning left once
        self.robot.turn_left()
        self.assertEqual(self.robot.orientation, "W")
        
        # Test that the Robot object's orientation changes to "S" after turning left a second time
        self.robot.turn_left()
        self.assertEqual(self.robot.orientation, "S")
    
    def test_turn_right(self):
        # Test that the Robot object's orientation changes to "E" after turning right once
        self.robot.turn_right()
        self.assertEqual(self.robot.orientation, "E")
        
        # Test that the Robot object's orientation changes to "S" after turning right a second time
        self.robot.turn_right()
        self.assertEqual(self.robot.orientation, "S")
    
    def test_move_forward_north(self):
        # Test that the Robot object's y-coordinate increases by 1 when moving forward while facing north
        self.robot.move_forward((5, 5))
        self.assertEqual(self.robot.x, 2)
        self.assertEqual(self.robot.y, 3)

    def test_move_forward_east(self):
        # Test that the Robot object's x-coordinate increases by 1 when moving forward while facing east
        self.robot.orientation = "E"
        self.robot.move_forward((5, 5))
        self.assertEqual(self.robot.x, 3)
        self.assertEqual(self.robot.y, 2)

    def test_move_forward_south(self):
        # Test that the Robot object's y-coordinate decreases by 1 when moving forward while facing south
        self.robot.orientation = "S"
        self.robot.move_forward((5, 5))
        self.assertEqual(self.robot.x, 2)
        self.assertEqual(self.robot.y, 1)

    def test_move_forward_west(self):
        # Test that the Robot object's x-coordinate decreases by 1 when moving forward while facing west
        self.robot.orientation = "W"
        self.robot.move_forward((5, 5))
        self.assertEqual(self.robot.x, 1)
        self.assertEqual(self.robot.y, 2)

    def test_move_forward_off_grid(self):
        # Test that the robot's "lost" flag is set correctly when it goes off the grid
        self.robot.move_forward((3, 3))
        self.assertFalse(self.robot.lost)

        self.robot.move_forward((3, 3))
        self.assertTrue(self.robot.lost)
    
    def test_str(self):
        # Test that the string representation of the robot is correct
        self.assertEqual(str(self.robot), "(2, 2, N)")
        
        self.robot.lost = True
        self.assertEqual(str(self.robot), "(2, 2, N) LOST")

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Capture stdout at the start of each method in class
        cls.stdout_backup = sys.stdout
        sys.stdout = StringIO()
    
    @classmethod
    def tearDownClass(cls):
        # Restore stdout at the end of each method in class
        sys.stdout = cls.stdout_backup

    def test_main(self):
        # Test imain runs properly, correct outputs are given for inputs
        input_str = '5 5\n(1, 2, N) FFLFLFLFF\n(3, 3, E) FFLFFF\n\ny\n'
        sys.stdin = StringIO(input_str)
        main()
        output = sys.stdout.getvalue()
        expected_output = '(2, 3, E)\n(5, 6, N) LOST\n'
        self.assertIn(expected_output, output)
        sys.stdin = sys.__stdin__

    def test_negative_grid_size(self):
        # Tests for correct error message if the grid input is negative (kind of workaround with the error message)
        input_str = '-1 -1\n(1, 2, N) FFLFLFLFF\n(3, 3, E) FFLF\n\ny\n'
        sys.stdin = StringIO(input_str)
        main()
        output = sys.stdout.getvalue()
        expected_output = ("Grid size cannot be negative")
        self.assertIn(expected_output, output)
        sys.stdin = sys.__stdin__

    def test_invalid_grid_imputs(self):
        # Tests for correct error message if the grid input is invalid (kind of workaround with the error message)
        input_str = 'a b\n(1, 2, N) FFLFLFLFF\n(3, 3, E) FFLF\n\ny\n'
        sys.stdin = StringIO(input_str)
        main()
        output = sys.stdout.getvalue()
        expected_output = ("Invalid grid size")
        self.assertIn(expected_output, output)
        sys.stdin = sys.__stdin__

    def robot_starts_outside_grid(self):
        # Tests for robot starting outside of the grid size that the user specified
        input_str = '1 1\n(1, 2, N) FFLFLFLFF\n(3, 3, E) FFLF\n\ny\n'
        sys.stdin = StringIO(input_str)
        main()
        output = sys.stdout.getvalue()
        expected_output = ("starting conditions outside grid space")
        self.assertIn(expected_output, output)
        sys.stdin = sys.__stdin__

if __name__ == '__main__':
    unittest.main(argv=['-v'], verbosity=2)