import unittest


# Beginner practice in python

# Easy function that adds n + n and divides by 2
def equals_n(n):
    if type(n) != int:
        raise TypeError("Wrong input type!")
    return (n + n) / 2


# Recursion function that counts down to zero starting from n
def countdown(n):
    if type(n) != int:
        raise TypeError("Wrong input type!")
    if n > 0:
        return countdown(n - 1)
    elif n < 0:
        print(n)
        return countdown(n + 1)
    else:
        return n


# Unit tests for equals_n
class UnitTestsForEqualsN(unittest.TestCase):
    def test_function(self):
        self.assertEqual(equals_n(12), 12)
        self.assertEqual(equals_n(12133114), 12133114)
        self.assertEqual(equals_n(-1), -1)
        self.assertNotEqual(equals_n(122), 12)
        self.assertEqual(countdown(331), 0)
        self.assertEqual(countdown(-12), 0)
        self.assertEqual(countdown(0), 0)
        self.assertNotEqual(countdown(2), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            equals_n("Not an int")
        with self.assertRaises(Exception):
            equals_n((1, 2, 3))
        with self.assertRaises(TypeError):
            countdown("Not an int")
        with self.assertRaises(Exception):
            countdown((1, 2, 3))