import unittest

from lean_preflight import imports_in, mask_comments_and_strings


class LeanPreflightTests(unittest.TestCase):
    def test_nested_comments_and_line_numbers(self):
        source = 'import A\n/- sorry /- axiom -/ admit\n -/\nimport B -- sorry\n'
        clean = mask_comments_and_strings(source)
        self.assertEqual(clean.count('\n'), source.count('\n'))
        self.assertEqual(len(clean), len(source))
        self.assertNotIn('sorry', clean)
        self.assertNotIn('axiom', clean)
        self.assertEqual(imports_in(clean), ['A', 'B'])

    def test_strings_and_real_markers(self):
        source = 'def text := "sorry \\\" /- -- admit"\ntheorem test : True := by sorry\n'
        clean = mask_comments_and_strings(source)
        self.assertEqual(clean.count('sorry'), 1)
        self.assertNotIn('admit', clean)

    def test_public_and_multiple_imports(self):
        self.assertEqual(imports_in('public import A.B C.D\nimport E\n'), ['A.B', 'C.D', 'E'])

    def test_unterminated_constructs_fail(self):
        for source in ('/- not closed', '"not closed'):
            with self.assertRaises(ValueError):
                mask_comments_and_strings(source)


if __name__ == '__main__':
    unittest.main()
